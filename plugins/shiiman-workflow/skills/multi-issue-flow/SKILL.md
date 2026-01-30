---
name: multi-issue-flow
description: MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。「マルチ Issue フロー」「multi-issue-flow」「並列 Issue 開発」「マルチエージェント Issue」「複数人で Issue」「並列 Issue フロー」「マルチフロー Issue」などで起動。複数 Worker でタスクを並列実行。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
user-invocable: true
---

# Multi Issue Flow

MCP マルチエージェントで Issue から PR まで並列実行する開発フロー。

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
┌────────────────────────────────────────────────────────────────┐
│                    tmux セッション                              │
├────────────┬────────────┬────────┬────────┬────────┬──────────┤
│   pane 0   │   pane 1   │ pane 2 │ pane 4 │ pane 6 │ ...      │
│  (Owner)   │  (Admin)   ├────────┼────────┼────────┤          │
│    25%     │    25%     │ pane 3 │ pane 5 │ pane 7 │          │
│            │            │        │        │        │          │
│ 全体統括   │ タスク分割 │ Worker │ Worker │ Worker │          │
│ Issue管理  │ 進捗管理   │   1    │   2    │   3    │          │
└────────────┴────────────┴────────┴────────┴────────┴──────────┘
      左半分 50%                右半分 50%（Worker ペイン）
```

**役割**:

- **Owner**: 全体統括、VSCode 拡張との橋渡し、Issue 作成・管理
- **Admin**: タスク分割、Worker 管理、進捗監視、Dashboard 更新
- **Worker**: worktree で実際の作業を行う（最大 6 体）

**フロー**:

```
VSCode 拡張で計画書作成
       ↓
ターミナル起動 → tmux セッション作成
       ↓
Owner ペイン作成 → Admin ペイン作成
       ↓
Admin がタスク分割
       ↓
Worker ペイン作成 → Worker が worktree で作業
       ↓
Worker → Admin に報告 → Admin → Owner に報告
       ↓
Owner が VSCode 拡張に結果を返す
       ↓
feature/{issue番号}（統合ブランチ）
       ↓
[PR] → デフォルトブランチ → [Issue クローズ]
```

## 3つの実行モード

### モード 1: 計画書実行モード（デフォルト）

引数なしで実行。既存の承認済み計画書から直接実行。

```
[既存計画書] → Issue作成 → ターミナル+MCP初期化 → 並列実行 → 統合 → PR作成
```

### モード 2: 計画書作成モード（--plan）

plan mode を使って計画書を作成・承認してから実行。

```
[ユーザー入力] → plan mode → 計画書作成 → 承認 → Issue作成 → ターミナル+MCP初期化 → ... → PR作成
```

### モード 3: 直接実行モード（タスク説明あり）

計画書を作らず、タスク説明から直接実行。

```
[タスク説明] → Issue作成 → ターミナル+MCP初期化 → 並列実行 → 統合 → PR作成
```

## モード判定

1. **先頭引数が `--plan` の場合** → モード 2（計画書作成モード）
2. **引数が1つ以上あり、`--plan` / `--help` / `--workers` 以外の文字列の場合** → モード 3（直接実行モード）
3. **引数なしの場合** → モード 1（計画書実行モード）

---

## Phase 1: セットアップ

### ステップ 1: Issue 作成

`gh issue create` で Issue を作成:

```bash
gh repo view --json owner,name
gh issue create --title "{タイトル}" --body "{本文}" --label "{ラベル}"
```

**Issue 本文フォーマット**（タスク番号付き）:

```markdown
## 概要

{タスクの目的・背景}

## タスク一覧

- [ ] Task 1: {サブタスク1の説明}
- [ ] Task 2: {サブタスク2の説明}
- [ ] Task 3: {サブタスク3の説明}
- [ ] Task 4: {サブタスク4の説明}
- [ ] Task 5: {サブタスク5の説明}

## 完了条件

- 全てのTaskが完了していること
- テストが通過していること
```

### ステップ 2: ベースブランチ作成

```bash
git fetch origin main
git checkout main
git pull origin main
git checkout -b feature/{issue番号}
git push -u origin feature/{issue番号}
```

### ステップ 3: MCP ワークスペース初期化

```
mcp__multi-agent-mcp__init_workspace を呼び出し
```

**パラメータ**:

- `workspace_path`: プロジェクト名（例: "my-project"）

### ステップ 4: ターミナル起動 + tmux セッション作成

```
mcp__multi-agent-mcp__init_tmux_workspace を呼び出し
```

**パラメータ**:

- `working_dir`: プロジェクトのルートパス
- `open_terminal`: true（デフォルト）

**動作**:

1. ターミナルアプリを起動（Ghostty/iTerm2/Terminal.app）
2. tmux セッションを作成
3. ペイン分割（Owner/Admin/Worker 用のレイアウト構築）
4. セッションに attach

**重要**: このステップでターミナルが開き、tmux セッションが作成される。以降のエージェント作成は、このセッション内のペインに配置される。

### ステップ 5: Owner エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "owner"
- `working_dir`: プロジェクトのルートパス

**注意**: init_tmux_workspace で作成済みのセッション内の pane 0 に配置される。

### ステップ 6: Admin エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "admin"
- `working_dir`: プロジェクトのルートパス

**注意**: 同じセッション内の pane 1 に配置される。

---

## Phase 2: タスク分割（Admin の仕事）

### ステップ 7: Owner → Admin に計画書を送信

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Admin の ID
- `task_content`: 計画書の内容（タスク分割を依頼）
- `session_id`: Issue 番号（例: "123"）

**Admin への指示内容（task_content の例）**:

```markdown
Issue #{issue番号} のタスクを分割・管理してください。

## 計画書

{計画書の内容}

## あなたの役割

1. 計画書を分析し、並列実行可能なサブタスクに分割
2. 各サブタスクを Dashboard に登録
3. Worker の作成と Worktree の割り当て
4. Worker にタスクを送信
5. Worker からの完了報告を受け取り、進捗を管理
6. 全 Worker 完了後、Owner に報告

## タスク分割の指針

- 各サブタスクは独立して実行可能
- ファイル単位または機能単位で分割
- 依存関係があるタスクは順次実行として記録
- Worker 数（最大 6）に合わせてタスクを分割
```

### ステップ 8: Admin がタスク分割・Dashboard 登録

Admin が以下を実行（Admin の自律的な動作）:

**8.1 タスク分割**:

計画書から並列実行可能なサブタスクを抽出:

- 各サブタスクは独立して実行可能
- ファイル単位または機能単位で分割
- 依存関係があるタスクは順次実行として記録

**8.2 Dashboard にタスク登録**:

各サブタスクを Dashboard に登録:

```
mcp__multi-agent-mcp__create_task を呼び出し
```

**パラメータ**:

- `title`: タスクタイトル
- `description`: タスクの詳細説明
- `branch`: 作業ブランチ名（例: `feature/{issue番号}-1`）

**注意**: `create_task` と `assign_task_to_agent` は Admin 限定のツール。

---

## Phase 3: Worker 起動・実行

### ステップ 9: Worktree 作成

各 Worker 用の worktree を作成:

```
mcp__multi-agent-mcp__create_worktree を呼び出し
```

**パラメータ**:

- `repo_path`: プロジェクトのルートパス
- `worktree_path`: Worker 用の worktree パス（例: `/tmp/worktrees/worker-1`）
- `branch`: `feature/{issue番号}-{task番号}`
- `create_branch`: true
- `base_branch`: `feature/{issue番号}`

### ステップ 10: Worker エージェント作成

```
mcp__multi-agent-mcp__create_agent を呼び出し
```

**パラメータ**:

- `role`: "worker"
- `working_dir`: 作成した worktree パス

**注意**: Worker は pane 2 以降に配置される。

### ステップ 11: Worker に Worktree を割り当て

```
mcp__multi-agent-mcp__assign_worktree を呼び出し
```

**パラメータ**:

- `agent_id`: 作成した Worker の ID
- `worktree_path`: 作成した worktree パス
- `branch`: `feature/{issue番号}-{task番号}`

### ステップ 12: Dashboard タスクをエージェントに割り当て

```
mcp__multi-agent-mcp__assign_task_to_agent を呼び出し
```

**パラメータ**:

- `task_id`: ステップ 8.2 で作成したタスク ID
- `agent_id`: Worker の ID
- `branch`: `feature/{issue番号}-{task番号}`
- `worktree_path`: Worker の worktree パス

**注意**: このツールは Admin 限定。

### ステップ 13: Admin → Worker にタスク送信

```
mcp__multi-agent-mcp__send_task を呼び出し
```

**パラメータ**:

- `agent_id`: Worker の ID
- `task_content`: タスク内容（Markdown 形式）
- `session_id`: Issue 番号（例: "123"）

**Worker への指示内容（task_content の例）**:

```markdown
Issue #{issue番号} の Task {task番号} を実装してください。

## タスク内容

{サブタスクの説明}

## 作業ブランチ

feature/{issue番号}-{task番号}（既に作成済み）

## 完了後の手順

1. 実装完了後、自己レビュー
2. コミット・プッシュ
3. feature/{issue番号} へマージ
4. **mcp__multi-agent-mcp__report_task_completion で Admin に報告**

## 報告時のパラメータ

- task_id: {タスクID}
- summary: 実装内容のサマリー
- files_changed: 変更したファイル一覧
```

### ステップ 14: Worker が実行、完了後 Admin に報告

Worker が以下を実行（Worker の自律的な動作）:

1. タスクを実装
2. 自己レビュー
3. コミット・プッシュ
4. feature/{issue番号} へマージ
5. Admin に完了報告:

```
mcp__multi-agent-mcp__report_task_completion を呼び出し
```

**パラメータ**:

- `task_id`: 割り当てられたタスク ID
- `summary`: 実装内容のサマリー
- `files_changed`: 変更したファイル一覧

**注意**: `report_task_completion` は Worker 限定のツール。

### ステップ 15: 並列実行監視

Admin が定期的にステータスを確認:

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

---

## Phase 4: 統合・完了

### ステップ 16: Admin が Worker の成果を統合

全 Worker の完了後:

1. 各 Worker の変更が `feature/{issue番号}` にマージされていることを確認
2. コンフリクトがあれば解決
3. 統合ブランチの動作確認

```bash
git checkout feature/{issue番号}
git pull origin feature/{issue番号}
```

### ステップ 17: Admin → Owner に完了報告

Admin が Owner に完了を報告:

```
mcp__multi-agent-mcp__send_message を呼び出し
```

**パラメータ**:

- `to_agent_id`: Owner の ID
- `message`: 完了報告（実行結果のサマリー）

### ステップ 18: クリーンアップ

**18.1 Worktree の削除**:

各 Worker の worktree を削除:

```
mcp__multi-agent-mcp__remove_worktree を呼び出し
```

**パラメータ**:

- `repo_path`: プロジェクトのルートパス
- `worktree_path`: Worker の worktree パス
- `force`: true（必要に応じて）

**18.2 全タスク完了チェック**:

```
mcp__multi-agent-mcp__check_all_tasks_completed を呼び出し
```

**確認項目**:

- 全タスクが completed 状態であることを確認
- 未完了タスクがある場合は警告を表示

**18.3 ワークスペースのクリーンアップ（ターミナル自動終了）**:

```
mcp__multi-agent-mcp__cleanup_on_completion を呼び出し
```

**動作**:

- 全タスク完了時にワークスペースをクリーンアップ
- ターミナルウィンドウを自動的に閉じる

### ステップ 19: Owner が VSCode 拡張に結果を返す

Owner がこのセッション（VSCode 拡張の Claude Code）に結果を報告。

### ステップ 20: セキュリティチェック＆自己レビュー

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
git diff main...feature/{issue番号}
```

### ステップ 21: ユーザー確認

**重要**: ここでユーザーに確認を求める。

```
## 変更内容の確認

### 並列実行結果

- Worker 1: {Task 1} ✅ 完了
- Worker 2: {Task 2} ✅ 完了
- Worker 3: {Task 3} ✅ 完了

### 変更サマリー

{git diff --stat main...feature/{issue番号} の出力}

### 自己レビュー結果

{レビューで確認した内容のサマリー}

### コミットメッセージ

{自動生成されたメッセージ}

この内容でコミット・プッシュ・PR作成を実行してよろしいですか？
```

### ステップ 22: Issue チェックボックス完了更新

ユーザー確認後、Issue の全てのチェックボックスを完了状態に更新します。

### ステップ 23: コミット（必要な場合）

統合ブランチに追加の変更がある場合:

```bash
git add .
git commit -m "{コミットメッセージ}"
```

### ステップ 24: プッシュ

```bash
git push origin feature/{issue番号}
```

### ステップ 25: PR 作成

```bash
gh pr create --title "{PRタイトル}" --body "{PR本文}"
```

**PR 本文**:

```markdown
## 概要

{変更内容の説明}

## 変更内容

- {変更点1}
- {変更点2}

## 並列実行サマリー

| Worker | Task | 状態 |
|--------|------|------|
| Worker 1 | Task 1 | ✅ 完了 |
| Worker 2 | Task 2 | ✅ 完了 |
| Worker 3 | Task 3 | ✅ 完了 |

## 関連 Issue

Closes #{issue番号}

## テスト計画

- [ ] {テスト項目}
```

### ステップ 26: 完了報告

```
## 開発フロー完了

### 作成された Issue

- #{issue番号}: {タイトル}

### 作成されたブランチ

- ベース: feature/{issue番号}
- 作業: feature/{issue番号}-1, feature/{issue番号}-2, ...

### 並列実行結果

- 総Worker数: {N}
- 完了タスク: {M}

### 作成された PR

- PR #{pr番号}: {タイトル}
- URL: {pr_url}

PR がマージされると Issue #{issue番号} は自動的にクローズされます。
```

---

## 重要な注意事項

### MCP ツールの使い方

- ✅ MCP ツールは `mcp__multi-agent-mcp__*` 形式で呼び出し
- ✅ `init_tmux_workspace` でターミナル起動 → tmux セッション作成
- ✅ Worker 数は最大 6
- ✅ 各 Worker は git worktree で独立したディレクトリで作業
- ✅ Dashboard でタスク進捗を管理
- ✅ `send_task` でファイル経由のタスク送信（長い指示に対応）

### ロールベースアクセス制御

- ✅ `update_task_status`, `assign_task_to_agent` → Admin 限定
- ✅ `report_task_completion` → Worker 限定（Admin に報告）

### 正しい実行順序

1. ✅ `init_workspace` → `init_tmux_workspace` → `create_agent("owner")` → `create_agent("admin")`
2. ✅ ターミナル起動が先、エージェント作成は後
3. ✅ Worker は Admin が作成・管理
4. ✅ Worker 完了後は `report_task_completion` で Admin に報告

### 禁止事項

- ❌ Worker 間で直接ファイルを共有しない
- ❌ MCP 初期化前にタスクを開始しない
- ❌ ユーザー確認なしでコミット・プッシュしない
- ❌ main ブランチに直接コミットしない
- ❌ ターミナル起動前にエージェントを作成しない
