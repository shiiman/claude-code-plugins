---
name: multi-flow
description: MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。「マルチフロー」「multi-flow」「並列軽量フロー」「マルチエージェント実行」「複数人で実行」「並列フロー」「マルチ軽量」などで起動。複数 Worker でタスクを並列実行しコミットメッセージを出力。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
user-invocable: true
---

# Multi Flow

MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。

## 前提条件

- multi-agent-mcp がインストール済み（**必須**）
- tmux がインストール済み（**必須**）

**確認方法**:

```bash
# tmux が利用可能か確認
which tmux

# multi-agent-mcp がインストール済みか確認
claude mcp list | grep multi-agent-mcp
```

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--workers N`: Worker 数を指定（デフォルト: 6、最大: 16）
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## アーキテクチャ

```
┌───────────────────────────────────────────────────────────────────┐
│                    tmux セッション (main)                          │
├─────────────────┬────────────┬────────────┬────────────┐
│     pane 0      │   pane 1   │   pane 3   │   pane 5   │
│     Admin       │    W1      │    W3      │    W5      │
│     (40%)       ├────────────┼────────────┼────────────┤
│ (タスク分割・   │   pane 2   │   pane 4   │   pane 6   │
│  管理)          │    W2      │    W4      │    W6      │
└─────────────────┴────────────┴────────────┴────────────┘
     左40%              右60% (Workers 1-6, 3列×2行)
```

**階層構造（指揮命令系統）**:

```
┌──────────────────────────────────────┐
│  このセッション = Owner                │  ← 起点 Claude Code（あなた）
│  (tmux ペインなし)                    │
└──────────────────┬───────────────────┘
                   │ create_agent + send_task（計画書）
                   ▼
┌──────────────────────┐
│      Admin           │  ← tmux pane 0 で動作
│  (タスク分割・管理)   │
└──────────┬───────────┘
           │ create_agent + send_task（タスク）
           ▼
┌──────────────────────┐
│     Workers          │  ← tmux pane 1-6 で動作
│  (タスク実行)         │
└──────────┬───────────┘
           │ report_task_completion
           ▼
         Admin → このセッション（Owner）
```

**役割分担**:

| 役割   | 実行者                          | 責務                                                    |
| ------ | ------------------------------- | ------------------------------------------------------- |
| Owner  | 起点 Claude Code（tmux なし）   | 全体指揮、Admin の管理、結果の確認                      |
| Admin  | tmux pane 0                     | タスク分割、Worker 作成・管理、進捗監視、Dashboard 更新 |
| Worker | tmux pane 1-6                   | 割り当てられたタスクの実行、worktree で作業             |

**ロールベースアクセス制御**:

- `update_task_status`, `assign_task_to_agent` → Admin 限定
- `report_task_completion` → Worker 限定（Admin に報告）

## 3つの実行モード

### モード 1: 計画書実行モード（デフォルト）

引数なしで実行。既存の承認済み計画書から直接実行。

```
[既存計画書] → セットアップ → Owner起動 → Owner に指示 → 結果待機 → コミットメッセージ出力
```

### モード 2: 計画書作成モード（--plan）

plan mode を使って計画書を作成・承認してから実行。

```
[ユーザー入力] → plan mode → 計画書作成 → 承認 → セットアップ → Owner起動 → ... → コミットメッセージ出力
```

### モード 3: 直接実行モード（タスク説明あり）

計画書を作らず、タスク説明から直接実行。

```
[タスク説明] → セットアップ → Owner起動 → Owner に指示 → 結果待機 → コミットメッセージ出力
```

## 実行フロー概要

```
【このセッション = Owner（起点 Claude Code）の仕事】
Phase 1: セットアップ + Admin 起動 + 計画書送信 + 結果待機

【Admin の仕事】
Phase 2: タスク分割 + Worker 作成 + タスク送信 + 進捗監視

【Worker の仕事】
Phase 3: タスク実行 + Admin への報告

【このセッション = Owner（起点 Claude Code）の仕事】
Phase 4: 結果確認 + コミットメッセージ出力
```

## モード判定

1. **先頭引数が `--plan` の場合** → モード 2（計画書作成モード）
2. **引数が1つ以上あり、`--plan` / `--help` / `--workers` 以外の文字列の場合** → モード 3（直接実行モード）
3. **引数なしの場合** → モード 1（計画書実行モード）

---

## Phase 1: セットアップ + Admin 起動（このセッション = Owner が実行）

### ステップ 1: ブランチ作成

計画書またはタスク説明から適切なブランチ名を生成します。

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{slug}
git push -u origin feature/{slug}
```

**slug の生成ルール**:

- タスク内容を簡潔な英語キーワードに変換
- 小文字、ハイフン区切り
- 例: 「複数ファイルのリファクタリング」→ `feature/multi-file-refactor`

**ブランチ名プレフィックス**（タスク内容から判断）:

- 新機能 → `feature/{slug}`
- バグ修正 → `fix/{slug}`
- ドキュメント → `docs/{slug}`
- リファクタリング → `refactor/{slug}`

### ステップ 2: MCP ワークスペース初期化

```
mcp__multi-agent-mcp__init_workspace を呼び出し
```

**パラメータ**:

- `workspace_path`: プロジェクト名（例: "my-project"）

### ステップ 3: ターミナル起動 + tmux セッション作成

```
mcp__multi-agent-mcp__init_tmux_workspace を呼び出し
```

**パラメータ**:

- `working_dir`: プロジェクトのルートパス
- `open_terminal`: true（デフォルト）
- `auto_setup_gtr`: true（デフォルト、gtr自動設定）

**結果**:

- ターミナルアプリ（Ghostty/iTerm2/Terminal.app）が開き、tmux セッション + ペインレイアウトが構築
- gtr (git-worktree-runner) が利用可能な場合、`.gtrconfig` を自動確認・生成

### ステップ 4: Owner エージェント登録（MCP に登録、tmux ペインなし）

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "owner"
- `working_dir`: プロジェクトのルートパス

**注意**: Owner は tmux ペインに配置されない。起点 Claude Code がこの Owner 役割を担う。

**自動処理**: IPC 自動登録 + メトリクス記録開始

### ステップ 5: Admin エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "admin"
- `working_dir`: プロジェクトのルートパス

**注意**: tmux pane 0 に配置される。

**自動処理**: IPC 自動登録 + メトリクス記録開始

### ステップ 6: Admin に計画書を送信

**重要**: ここで Admin に `send_task` を使って計画書を送信。これにより Admin の tmux ペインで `claude` が起動される。

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Admin の ID
- `task_content`: 計画書と指示内容（下記参照）
- `session_id`: ブランチの slug（例: "multi-file-refactor"）

**Admin への指示内容（task_content）**:

```markdown
# タスク分割・Worker 管理指示

あなたは Admin エージェントです。以下の計画書に基づいてタスクを分割し、Worker を管理してください。

## 計画書
{計画書の内容またはタスク説明}

## 作業ブランチ
feature/{slug}

## Worker 数
{指定された Worker 数、デフォルト: 3}

## あなたの役割

1. **タスクを分割**
   - 計画書から並列実行可能なサブタスクを抽出
   - 各サブタスクを Dashboard に登録（`create_task`）

2. **Worker を作成・タスク割り当て**
   - 各 Worker 用の Worktree を作成（`create_worktree`）
   - Worker エージェントを作成（`create_agent(role="worker")`）
   - Worktree を割り当て（`assign_worktree`）
   - タスクを割り当て（`assign_task_to_agent`）
   - タスクを送信（`send_task`）

3. **進捗を監視**
   - `get_dashboard_summary` で進捗確認
   - Worker の完了報告を待つ

4. **完了報告**
   - 全 Worker 完了後、Owner（このセッション）に `send_message` で結果を報告

## 完了条件

- 全 Worker のタスクが completed 状態
- 全ての変更が feature/{slug} にマージ済み
- コンフリクトがないこと
```

### ステップ 7: Admin の完了を待機

**重要**: Admin が自律的に Worker を作成・管理する。このセッション（Owner）は Admin からの完了報告を待つ。

定期的に状態を確認（必要に応じて）:

```
mcp__multi-agent-mcp__get_dashboard_summary を呼び出し（軽量）
```

または Admin からのメッセージを確認:

```
mcp__multi-agent-mcp__read_messages を呼び出し
```

---

## Phase 2: タスク分割 + Worker 管理（Admin が実行）

**以下は Admin が自律的に実行する内容。このセッションは実行しない。**

### Admin のステップ 1: Dashboard にタスク登録

```
mcp__multi-agent-mcp__create_task を呼び出し
```

**パラメータ**:

- `title`: タスクタイトル
- `description`: タスクの詳細説明
- `branch`: 作業ブランチ名（例: `feature/{slug}-1`）

### Admin のステップ 2: Worker 用 Worktree 作成

各 Worker に対して:

```
mcp__multi-agent-mcp__create_worktree を呼び出し
```

**パラメータ**:

- `repo_path`: プロジェクトのルートパス
- `worktree_path`: Worker 用の worktree パス（例: `/tmp/worktrees/worker-1`）
- `branch`: `feature/{slug}-{task番号}`
- `create_branch`: true
- `base_branch`: `feature/{slug}`

### Admin のステップ 3: Worker エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "worker"
- `working_dir`: 作成した worktree パス

**注意**: pane 1〜6 に順次配置される。

### Admin のステップ 4: Worker に Worktree を割り当て

```
mcp__multi-agent-mcp__assign_worktree を呼び出し
```

**パラメータ**:

- `agent_id`: 作成した Worker の ID
- `worktree_path`: 作成した worktree パス
- `branch`: `feature/{slug}-{task番号}`

### Admin のステップ 5: Dashboard タスクをエージェントに割り当て

```
mcp__multi-agent-mcp__assign_task_to_agent を呼び出し
```

**パラメータ**:

- `task_id`: ステップ 1 で作成したタスク ID
- `agent_id`: Worker の ID
- `branch`: `feature/{slug}-{task番号}`
- `worktree_path`: Worker の worktree パス

### Admin のステップ 6: Worker にタスクを送信

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Worker の ID
- `task_content`: タスク内容（Markdown 形式）
- `session_id`: ブランチの slug

**Worker への指示内容（task_content の例）**:

**注意**: `send_task` は `auto_enhance=True`（デフォルト）で呼び出すと、以下を自動で統合します:

- **7セクション構造**: What/Why/Who/Constraints/Current State/Decisions/Notes
- **ペルソナ**: タスク内容に応じて最適なペルソナを自動選択
- **メモリ検索**: プロジェクト + グローバルメモリから関連情報を自動取得
- **Self-Check**: コンパクション復帰用の情報

また、`report_task_completion` は以下を自動で実行します:

- **メモリ保存**: タスク結果を自動でメモリに保存
- **メトリクス更新**: 完了統計を自動で記録

```markdown
# Task {task番号} 実装指示

以下のタスクを実装してください。

## タスク内容
{サブタスクの説明}

## 作業ブランチ
feature/{slug}-{task番号}（既に作成済み）

## 作業ディレクトリ
{worktree_path}

## 作業中の注意

- **質問がある場合**: `mcp__multi-agent-mcp__send_message` で Admin に質問
- **重要な決定をした場合**: `mcp__multi-agent-mcp__save_to_memory` で記録

## 完了後の手順

1. 実装完了後、自己レビュー
2. コミット・プッシュ
3. feature/{slug} へマージ
4. **Admin に完了報告**: `mcp__multi-agent-mcp__report_task_completion`
   - task_id, status, message, caller_agent_id を指定
   - メモリ保存・メトリクス更新は自動実行
```

### Admin のステップ 7: 並列実行監視（監視ループ）

Admin は以下の監視ループを実行します。

#### 7.1 定期ヘルスチェック（30秒ごと目安）

```
mcp__multi-agent-mcp__healthcheck_all を呼び出し
```

**チェック内容**:

- 各 Worker の応答状態
- tmux ペインが生きているか
- 最終活動時刻からの経過時間

**応答なしの Worker の復旧**:

```
mcp__multi-agent-mcp__attempt_recovery を呼び出し
```

**パラメータ**:

- `agent_id`: 応答なしの Worker ID

#### 7.2 IPC メッセージ確認

Worker からの質問・報告を確認:

```
mcp__multi-agent-mcp__get_unread_count を呼び出し
```

未読がある場合:

```
mcp__multi-agent-mcp__read_messages を呼び出し
```

**パラメータ**:

- `agent_id`: Admin の ID
- `mark_as_read`: true

**Worker からのメッセージタイプ**:

- `question`: 質問 → 回答を `send_message` で返信
- `report`: 進捗報告 → Dashboard 更新
- `error`: エラー報告 → 復旧対応

#### 7.3 進捗管理

定期的にステータスを確認:

```
mcp__multi-agent-mcp__get_dashboard_summary を呼び出し（軽量）
```

**監視項目**:

- 各 Worker の状態（idle/busy/completed/failed）
- 完了したタスク数
- エラーの有無

完了タスクの状態更新:

```
mcp__multi-agent-mcp__update_task_status を呼び出し
```

**パラメータ**:

- `task_id`: タスク ID
- `status`: "completed" または "failed"
- `caller_agent_id`: Admin の ID

#### 7.4 全 Worker 完了後の処理

全 Worker が完了したら:

1. 変更を feature/{slug} にマージ確認
2. コンフリクトがあれば解決指示
3. Owner に `send_message` で完了報告

```
mcp__multi-agent-mcp__send_message を呼び出し
```

**パラメータ**:

- `from_agent_id`: Admin の ID
- `to_agent_id`: Owner の ID
- `message`: "全 Worker のタスクが完了しました。結果: ..."
- `message_type`: "report"

---

## Phase 3: タスク実行 + 完了報告（Worker が実行）

**以下は Worker が自律的に実行する内容。**

### Worker のステップ 1: タスク実行

- 指示されたタスクを実装
- コミット・プッシュ
- feature/{slug} へマージ

### Worker のステップ 2: Admin に完了報告

```
mcp__multi-agent-mcp__report_task_completion を呼び出し
```

**パラメータ**:

- `task_id`: 完了したタスクのID
- `status`: "completed" または "failed"
- `message`: 作業内容の要約
- `caller_agent_id`: Worker の ID

---

## Phase 4: 結果確認 + コミットメッセージ出力（このセッション = Owner が実行）

### ステップ 1: 結果統合確認

全 Worker の完了後:

1. 各 Worker の変更が `feature/{slug}` にマージされていることを確認
2. コンフリクトがあれば解決
3. 統合ブランチの動作確認

```bash
git checkout feature/{slug}
git pull origin feature/{slug}
```

### ステップ 2: クリーンアップ

**2.1 全タスク完了チェック**:

```
mcp__multi-agent-mcp__check_all_tasks_completed を呼び出し
```

**2.2 ワークスペースのクリーンアップ（ターミナル自動終了）**:

```
mcp__multi-agent-mcp__cleanup_on_completion を呼び出し
```

**動作**:

- 全タスク完了時にワークスペースをクリーンアップ
- ターミナルウィンドウを自動的に閉じる

### ステップ 3: セキュリティチェック＆自己レビュー

**セキュリティチェック**:

```bash
git status
```

以下のパターンを検出したら警告:

- `.env*` - 環境変数
- `*.pem`, `*.key` - 秘密鍵
- `credentials.json` - 認証情報

**自己レビュー**:

```bash
git diff main...feature/{slug}
```

### ステップ 4: ユーザー確認

**重要**: ここでユーザーに確認を求める。

```
## 変更内容の確認

### 並列実行結果
- Worker 1: {Task 1} ✅ 完了
- Worker 2: {Task 2} ✅ 完了
- Worker 3: {Task 3} ✅ 完了

### 変更サマリー
{git diff --stat main...feature/{slug} の出力}

### 自己レビュー結果
{レビューで確認した内容のサマリー}

### 推奨コミットメッセージ
{自動生成されたメッセージ}

この内容でよろしいですか？
```

### ステップ 5: コミットメッセージ出力

**重要: このフローではコミット・プッシュ・PR作成を行いません。**

ユーザー確認後、推奨コミットメッセージを出力して終了:

```
## 実装完了

### 作成されたブランチ
- ベース: feature/{slug}
- 作業: feature/{slug}-1, feature/{slug}-2, ...

### 並列実行結果
- 総Worker数: {N}
- 完了タスク: {M}

### 変更サマリー
{git diff --stat main...feature/{slug} の出力}

### 推奨コミットメッセージ

以下のコミットメッセージを推奨します:

```text
{Conventional Commits 形式のメッセージ}

並列実行サマリー:

- Worker 1: {Task 1 の内容}
- Worker 2: {Task 2 の内容}
- Worker 3: {Task 3 の内容}
```

**コミットメッセージ形式**:

1. まず `.claude/settings.json` の `git.commitMessage` 設定を確認
2. 設定がある場合はその形式に従う
3. 設定がない場合は Conventional Commits（日本語）を使用

### 次のステップ（手動）

1. 変更をステージ: `git add .`
2. コミット: `git commit -m "{上記メッセージ}"`
3. プッシュ: `git push origin feature/{slug}`
4. 必要に応じて PR 作成: `gh pr create`

```

## 重要な注意事項

### このセッション（= Owner）がやること

- ✅ ブランチ作成
- ✅ MCP ワークスペース初期化
- ✅ tmux セッション作成
- ✅ Owner エージェント登録（MCP に登録、tmux ペインなし）
- ✅ Admin エージェント作成
- ✅ Admin に `send_task` で計画書を送信
- ✅ Admin の完了を待機
- ✅ 結果確認・クリーンアップ
- ✅ コミットメッセージ出力

### このセッション（= Owner）がやらないこと

- ❌ Worker を直接作成（Admin の仕事）
- ❌ タスク分割（Admin の仕事）
- ❌ Worker にタスクを直接送信（Admin の仕事）
- ❌ Issue 作成
- ❌ 自動コミット・プッシュ
- ❌ PR 作成
- ❌ main ブランチで直接作業

### MCP ツール使用ルール

- ✅ MCP ツールは `mcp__multi-agent-mcp__*` 形式で呼び出し
- ✅ Worker 数は最大 16
- ✅ 各 Worker は git worktree で独立したディレクトリで作業
- ✅ Dashboard でタスク進捗を管理
- ✅ `send_task` でファイル経由のタスク送信（長い指示に対応）
- ✅ `report_task_completion` で Worker が Admin に報告
