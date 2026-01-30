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
- `--workers N`: Worker 数を指定（デフォルト: 3、最大: 6）
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        tmux セッション (main)                            │
├────────────┬────────────┬────────┬────────┬────────┬────────┬────────┤
│   pane 0   │   pane 1   │ pane 2 │ pane 3 │ pane 4 │ pane 5 │ pane 6 │
│   Owner    │   Admin    │   W1   │   W2   │   W3   │   W4   │   W5   │
│            │            │        │        │        │        │   ...  │
│ (VSCode    │ (タスク    │ (実装) │ (実装) │ (実装) │ (実装) │ (実装) │
│  との橋渡し)│  分割・管理)│        │        │        │        │        │
└────────────┴────────────┴────────┴────────┴────────┴────────┴────────┘
      ↑                ↑                  ↑
      │                │                  │
このセッション ────→ 計画書送信 ────→ タスク送信
      │                │                  │
      └────────────────┼──────────────────┘
                       │
                  report_task_completion
                  (Worker → Admin 報告)
```

**階層構造**:

- **Owner** (1体): 全体指揮、VSCode 拡張との橋渡し
- **Admin** (1体): タスク分割、Worker 管理、進捗管理、ダッシュボード更新
- **Worker** (最大6体): 割り当てられたタスクの実行、worktree で作業

**ロールベースアクセス制御**:

- `update_task_status`, `assign_task_to_agent` → Admin 限定
- `report_task_completion` → Worker 限定（Admin に報告）

## 3つの実行モード

### モード 1: 計画書実行モード（デフォルト）

引数なしで実行。既存の承認済み計画書から直接実行。

```
[既存計画書] → ブランチ作成 → MCP初期化 → ターミナル起動 → エージェント作成 → 並列実行 → 統合 → コミットメッセージ出力
```

### モード 2: 計画書作成モード（--plan）

plan mode を使って計画書を作成・承認してから実行。

```
[ユーザー入力] → plan mode → 計画書作成 → 承認 → ブランチ作成 → MCP初期化 → ... → コミットメッセージ出力
```

### モード 3: 直接実行モード（タスク説明あり）

計画書を作らず、タスク説明から直接実行。

```
[タスク説明] → ブランチ作成 → MCP初期化 → ターミナル起動 → エージェント作成 → 並列実行 → 統合 → コミットメッセージ出力
```

## 実行フロー

```
【Phase 1: セットアップ】
ブランチ作成 → MCP初期化 → ターミナル起動+tmux作成 → Owner作成 → Admin作成

【Phase 2: タスク分割】
Admin に計画書送信 → Admin がタスク分割・Dashboard 登録

【Phase 3: Worker 起動・実行】
Worktree作成 → Worker作成 → タスク送信 → Worker実行 → Admin に報告

【Phase 4: 統合・完了】
統合 → クリーンアップ → 自己レビュー → [確認] → コミットメッセージ出力
```

## モード判定

1. **先頭引数が `--plan` の場合** → モード 2（計画書作成モード）
2. **引数が1つ以上あり、`--plan` / `--help` / `--workers` 以外の文字列の場合** → モード 3（直接実行モード）
3. **引数なしの場合** → モード 1（計画書実行モード）

---

## Phase 1: セットアップ

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

**結果**: ターミナルアプリ（Ghostty/iTerm2/Terminal.app）が開き、tmux セッション + ペインレイアウトが構築される。

### ステップ 4: Owner エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "owner"
- `working_dir`: プロジェクトのルートパス

**注意**: init_tmux_workspace で作成済みのセッション内の pane 0 に配置される。

### ステップ 5: Admin エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "admin"
- `working_dir`: プロジェクトのルートパス

**注意**: 同じセッション内の pane 1 に配置される。

---

## Phase 2: タスク分割（Admin の仕事）

### ステップ 6: Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Admin の ID
- `task_content`: 計画書の内容（タスク分割を依頼）
- `session_id`: ブランチの slug（例: "multi-file-refactor"）

**Admin への指示内容（task_content の例）**:

```markdown
以下の計画書に基づいてタスクを分割し、Worker に割り当ててください。

## 計画書
{計画書の内容}

## 実行手順
1. 計画書から並列実行可能なサブタスクを抽出
2. 各サブタスクを Dashboard に登録（create_task）
3. Worker 数に合わせてタスクを分割（1 Worker = 1 タスク）
4. 各 Worker にタスクを割り当て（assign_task_to_agent）
5. 進捗を監視し、完了を待つ

## 分割の指針
- 各サブタスクは独立して実行可能
- ファイル単位または機能単位で分割
- 依存関係があるタスクは順次実行として記録
```

### ステップ 7: Admin がタスク分割・Dashboard 登録

Admin は以下を実行:

**7.1 Dashboard にタスク登録**:

```
mcp__multi-agent-mcp__create_task を呼び出し
```

**パラメータ**:

- `title`: タスクタイトル
- `description`: タスクの詳細説明
- `branch`: 作業ブランチ名（例: `feature/{slug}-1`）

---

## Phase 3: Worker 起動・実行

### ステップ 8: Worker 用 Worktree 作成

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

### ステップ 9: Worker エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "worker"
- `working_dir`: 作成した worktree パス

**注意**: pane 2〜7 に順次配置される。

### ステップ 10: Worker に Worktree を割り当て

```
mcp__multi-agent-mcp__assign_worktree を呼び出し
```

**パラメータ**:

- `agent_id`: 作成した Worker の ID
- `worktree_path`: 作成した worktree パス
- `branch`: `feature/{slug}-{task番号}`

### ステップ 11: Dashboard タスクをエージェントに割り当て

```
mcp__multi-agent-mcp__assign_task_to_agent を呼び出し
```

**パラメータ**:

- `task_id`: ステップ 7.1 で作成したタスク ID
- `agent_id`: Worker の ID
- `branch`: `feature/{slug}-{task番号}`
- `worktree_path`: Worker の worktree パス

**注意**: このツールは Admin 限定です。

### ステップ 12: Worker にタスクを送信

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Worker の ID
- `task_content`: タスク内容（Markdown 形式）
- `session_id`: ブランチの slug（例: "multi-file-refactor"）

**Worker への指示内容（task_content の例）**:

```markdown
Task {task番号} を実装してください。

## タスク内容
{サブタスクの説明}

## 作業ブランチ
feature/{slug}-{task番号}（既に作成済み）

## 完了後の手順
1. 実装完了後、自己レビュー
2. コミット・プッシュ
3. feature/{slug} へマージ
4. **mcp__multi-agent-mcp__report_task_completion で Admin に報告**

## 報告時のパラメータ
- task_id: {タスクID}
- status: "completed" または "failed"
- message: 作業内容の要約
- caller_agent_id: あなたの Worker ID
```

### ステップ 13: 並列実行監視

定期的にステータスを確認:

```
mcp__multi-agent-mcp__get_dashboard_summary を呼び出し（軽量）
```

詳細が必要な場合:

```
mcp__multi-agent-mcp__get_dashboard を呼び出し
```

**監視項目**:

- 各 Worker の状態（idle/busy/completed/failed）
- 完了したタスク数
- エラーの有無

**ヘルスチェック**:

```
mcp__multi-agent-mcp__healthcheck_all を呼び出し
```

**エラー時の対応**:

Worker がエラーで停止した場合:

```
mcp__multi-agent-mcp__attempt_recovery を呼び出し
```

**パラメータ**:

- `agent_id`: 異常な Worker の ID

復旧不可能な場合はユーザーに報告し、タスクを別の Worker に再割り当て。

### ステップ 14: Worker の完了報告（Worker が実行）

Worker は作業完了後、Admin に報告:

```
mcp__multi-agent-mcp__report_task_completion を呼び出し
```

**パラメータ**:

- `task_id`: 完了したタスクのID
- `status`: "completed" または "failed"
- `message`: 作業内容の要約
- `caller_agent_id`: Worker の ID

**注意**: このツールは Worker 限定です。Admin が受け取って Dashboard を更新します。

---

## Phase 4: 統合・完了

### ステップ 15: 結果統合

全 Worker の完了後:

1. 各 Worker の変更が `feature/{slug}` にマージされていることを確認
2. コンフリクトがあれば解決
3. 統合ブランチの動作確認

```bash
git checkout feature/{slug}
git pull origin feature/{slug}
```

### ステップ 16: クリーンアップ

**16.1 Worktree の削除**:

各 Worker の worktree を削除:

```
mcp__multi-agent-mcp__remove_worktree を呼び出し
```

**パラメータ**:

- `repo_path`: プロジェクトのルートパス
- `worktree_path`: Worker の worktree パス
- `force`: true（必要に応じて）

**16.2 全タスク完了チェック**:

```
mcp__multi-agent-mcp__check_all_tasks_completed を呼び出し
```

**確認項目**:

- 全タスクが completed 状態であることを確認
- 未完了タスクがある場合は警告を表示

**16.3 ワークスペースのクリーンアップ（ターミナル自動終了）**:

```
mcp__multi-agent-mcp__cleanup_on_completion を呼び出し
```

**動作**:

- 全タスク完了時にワークスペースをクリーンアップ
- ターミナルウィンドウを自動的に閉じる

### ステップ 17: セキュリティチェック＆自己レビュー

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

### ステップ 18: ユーザー確認

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

### ステップ 19: コミットメッセージ出力

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
- 実行時間: {概算}

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

- ✅ MCP ツールは `mcp__multi-agent-mcp__*` 形式で呼び出し
- ✅ Worker 数は最大 6
- ✅ 各 Worker は git worktree で独立したディレクトリで作業
- ✅ ブランチを作成する（feature/{slug} 形式）
- ✅ Dashboard でタスク進捗を管理
- ✅ `send_task` でファイル経由のタスク送信（長い指示に対応）
- ✅ `report_task_completion` で Worker が Admin に報告
- ✅ 統合後に必ず自己レビュー
- ✅ コミットメッセージを出力する
- ❌ Issue を作成しない
- ❌ 自動でコミット・プッシュしない
- ❌ PR を作成しない
- ❌ Worker 間で直接ファイルを共有しない
- ❌ MCP 初期化前にタスクを開始しない
- ❌ main ブランチで直接作業しない
