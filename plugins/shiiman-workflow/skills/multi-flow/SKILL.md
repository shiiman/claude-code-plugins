---
name: multi-flow
description: MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。「マルチフロー」「multi-flow」「並列軽量フロー」「マルチエージェント実行」「複数人で実行」「並列フロー」「マルチ軽量」などで起動。複数 Worker でタスクを並列実行しコミットメッセージを出力。
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, EnterPlanMode, TodoWrite, Task]
context: fork
---

# Multi Flow

MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー。

## 前提条件

- multi-agent-mcp がインストール済み
- tmux がインストール済み

**確認方法**:

```bash
# MCP が利用可能か確認
which tmux
```

## 引数

- `--plan`: plan mode で計画書を新規作成してから実行
- `--workers N`: Worker 数を指定（デフォルト: 3、最大: 5）
- `--help`: ヘルプを表示
- `[タスク説明]`: 計画書なしで直接実行（簡単なタスク用）

## アーキテクチャ

```
Owner（このセッション）
    ↓ 全体統括・タスク分解
Admin（1）─ タスク分配・進捗監視・ダッシュボード更新
    ↓
┌───┬───┬───┬───┬───┐
W1  W2  W3  W4  W5   ← Worker（並列実行）
└───┴───┴───┴───┴───┘
    ↓ 各Workerが実装完了後、feature/{slug}へマージ
         feature/{slug}（統合ブランチ）
              ↓ 全Task完了後
         コミットメッセージ出力
```

## 3つの実行モード

### モード 1: 計画書実行モード（デフォルト）

引数なしで実行。既存の承認済み計画書から直接実行。

```
[既存計画書] → ブランチ作成 → MCP初期化 → 並列実行 → 統合 → コミットメッセージ出力
```

### モード 2: 計画書作成モード（--plan）

plan mode を使って計画書を作成・承認してから実行。

```
[ユーザー入力] → plan mode → 計画書作成 → 承認 → ブランチ作成 → MCP初期化 → ... → コミットメッセージ出力
```

### モード 3: 直接実行モード（タスク説明あり）

計画書を作らず、タスク説明から直接実行。

```
[タスク説明] → ブランチ作成 → MCP初期化 → 並列実行 → 統合 → コミットメッセージ出力
```

## 実行フロー

```
ブランチ作成 → MCP初期化 → タスク分割 → Worker並列実行 → 統合 → 自己レビュー → [確認] → コミットメッセージ出力
```

## モード判定

1. **先頭引数が `--plan` の場合** → モード 2（計画書作成モード）
2. **引数が1つ以上あり、`--plan` / `--help` / `--workers` 以外の文字列の場合** → モード 3（直接実行モード）
3. **引数なしの場合** → モード 1（計画書実行モード）

## 共通ステップ（全モード共通）

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
mcp__multi-agent__init_workspace を呼び出し
```

**パラメータ**:

- `workspace_path`: プロジェクト名（例: "my-project"）

### ステップ 3: タスク分割

計画書/タスク説明から並列実行可能なサブタスクを抽出:

- 各サブタスクは独立して実行可能
- ファイル単位または機能単位で分割
- 依存関係があるタスクは順次実行として記録

**分割の目安**:

- Worker 数に合わせてタスクを分割
- 1つのタスクは 1 Worker が担当
- タスク間の依存関係を最小化

### ステップ 4: Admin エージェント作成

```
mcp__multi-agent__create_agent を呼び出し
```

**パラメータ**:

- `role`: "admin"
- `working_dir`: プロジェクトのルートパス

### ステップ 5: Worker エージェント作成・タスク配布

各 Worker に対して:

```
mcp__multi-agent__create_agent を呼び出し
```

**パラメータ**:

- `role`: "worker"
- `working_dir`: Worker 用の worktree パス

**タスク送信**:

```
mcp__multi-agent__send_command を呼び出し
```

**Worker への指示内容**:

```
Task {task番号} を実装してください。

## タスク内容
{サブタスクの説明}

## 作業ブランチ
feature/{slug} から feature/{slug}-{task番号} を作成

## 完了後の手順
1. 実装完了後、自己レビュー
2. コミット・プッシュ
3. feature/{slug} へマージ
```

### ステップ 6: 並列実行監視

定期的にステータスを確認:

```
mcp__multi-agent__get_dashboard を呼び出し
```

**監視項目**:

- 各 Worker の状態（idle/busy/completed/failed）
- 完了したタスク数
- エラーの有無

**エラー時の対応**:

- Worker がエラーで停止した場合は、タスクを別の Worker に再割り当て
- 復旧不可能な場合はユーザーに報告

### ステップ 7: 結果統合

全 Worker の完了後:

1. 各 Worker の変更が `feature/{slug}` にマージされていることを確認
2. コンフリクトがあれば解決
3. 統合ブランチの動作確認

```bash
git checkout feature/{slug}
git pull origin feature/{slug}
```

### ステップ 8: クリーンアップ

```
mcp__multi-agent__cleanup_workspace を呼び出し
```

### ステップ 9: セキュリティチェック＆自己レビュー

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

### ステップ 10: ユーザー確認

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

### ステップ 11: コミットメッセージ出力

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

```
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

- ✅ MCP ツールは `mcp__multi-agent__*` 形式で呼び出し
- ✅ Worker 数は最大 5
- ✅ 各 Worker は git worktree で独立したディレクトリで作業
- ✅ ブランチを作成する（feature/{slug} 形式）
- ✅ 統合後に必ず自己レビュー
- ✅ コミットメッセージを出力する
- ❌ Issue を作成しない
- ❌ 自動でコミット・プッシュしない
- ❌ PR を作成しない
- ❌ Worker 間で直接ファイルを共有しない
- ❌ MCP 初期化前にタスクを開始しない
- ❌ main ブランチで直接作業しない
