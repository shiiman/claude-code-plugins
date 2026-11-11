---
name: shiiman-workflow:multi
description: マルチエージェントで並列実装する開発フロー。「shiiman-workflow:multi」「マルチフロー」「並列で実装」などで起動。依頼された範囲の実装・検証と、許可済みのコミット・Issue・push・PR 作成を重複確認せず行う。
allowed-tools:
  [
    Read,
    Write,
    Edit,
    Bash,
    Glob,
    Grep,
    AskUserQuestion,
    EnterPlanMode,
    TodoWrite,
    Task,
    Skill,
  ]
context: fork
user-invocable: true
argument-hint: "[タスク説明]"
---

# Multi Flow

multi-agent-mcp（Owner/Admin/Worker）で並列実装する開発フロー。

フラグは不要。タスクを伝えれば、git の状態・発話内容から実行条件を自動判断し、曖昧な点だけ確認する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
shiiman-workflow:multi - マルチエージェント開発フロー

概要:
  multi-agent-mcp（Owner/Admin/Worker）で並列実装する。
  実装条件（Issue/PR・計画書・ブランチ・git）はフラグ不要で自動判断し、
  曖昧な点だけ確認する。

使用方法:
  shiiman-workflow:multi [タスク説明]
  shiiman-workflow:multi --help

オプション:
  --help  このヘルプを表示

例:
  shiiman-workflow:multi                            # 既存計画書から並列実装（あれば）
  shiiman-workflow:multi "API を並列リファクタ"      # タスク説明から並列実装
  shiiman-workflow:multi "認証を実装して PR まで"    # 並列実装・コミット・push・PR 作成
  shiiman-workflow:multi --help                     # ヘルプを表示

指定の伝え方（フラグの代わり）:
  - 「計画を立ててから」  → 計画書を作成してから実装
  - 「ブランチで」        → worktree ではなくブランチを作成
  - 「PR まで」           → コミット・通常の push・PR 作成まで実施
  - 「Issue と PR まで」   → Issue 作成も含めて実施
  - 「コミットだけ」      → 検証後にコミットし、push・Issue・PR は作成しない
```

## 前提条件

- multi-agent-mcpが利用可能（**必須**）
- tmux がインストール済み（**必須**）
- `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）

## 環境変数

モデルプロファイルは環境変数で設定（`.env` または `export`）:

```bash
MCP_MODEL_PROFILE_ACTIVE=performance  # standard または performance
```

## ⚠️ caller_agent_id について（重要）

**全ての multi-agent-mcp ツールには `caller_agent_id` パラメータが必須です。**

- `mcp__multi-agent-mcp__create_agent()` の戻り値から自分の ID を取得し、`{owner_id}` として保存
- 以降の multi-agent-mcp ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

## 起動時の自動判断（フラグの代わり）

ユーザーにフラグを入力させない。以下を順に決定する。**発話・タスク説明に明示があればそれを最優先**し、明示がなければ自動判断、それでも曖昧な項目だけ後述の手順で確認する。

| 項目              | 既定       | 判断ルール                                                                                |
| ----------------- | ---------- | ----------------------------------------------------------------------------------------- |
| git / no-git      | 自動       | `git rev-parse --is-inside-work-tree` 成功なら git。失敗なら no-git（ブランチ作成を省略） |
| worktree / branch | worktree   | 「ブランチで」「worktree なし」等の発話があれば branch                                    |
| 計画書の扱い      | 後述の判定 | 「計画を立てて」「plan で」→ 計画書作成。タスク説明あり → 直接。なし → 既存計画書を探索   |

### 許可された完了範囲

現在の依頼と既存の許可から、操作ごとに実行範囲を判断する。

- 実装だけの依頼: 実装・レビュー・検証を行い、コミットや Issue・PR を作るかの追加質問はせず終了する。
- コミットだけの依頼: チェック後に対象変更をコミットする。push や Issue・PR 作成は行わない。
- PR 作成の依頼: 必要な実装・検証・対象変更のコミット・通常の feature branch push を完了して PR を作成する。Issue は依頼されているか、許可済みのワークフローで必要な場合だけ作成する。
- Issue 作成の依頼: 依頼された Issue と明示された後続操作だけを行う。必要に応じて確認済みの既存 Issue を参照する。
- 「push しない」などの明示的な制約を優先する。範囲を黙って広げず、具体的な阻害要因を報告する。

許可済みの操作に `--no-confirm`、計画承認、完了時の再承認を要求しない。後続の仕上げ手順も個別に許可された操作だけを実行し、依頼されていない手順は省略する。重要な範囲変更、破壊的操作、高影響操作が発生する場合は許可を再確認する。

### git の状態判定

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

- 成功 → git モード（ブランチ/worktree を作成、`init_tmux_workspace` は通常設定）
- 失敗 → no-git モード（ブランチ作成を省略、`init_tmux_workspace` に `enable_git=false` を渡す）

### 計画書の扱いの判定

1. 「計画を立ててから」等の依頼がある → **計画作成**: `.claude/plans/` に計画を保存する。実装も依頼されていれば説明後に続行し、計画承認を明示的に求められた場合や重要な未解決の判断がある場合だけ待機する
2. タスク説明がある → **直接実行**: タスク説明をそのまま実装の指針にする
3. タスク説明なし → **既存計画書**: 最新の計画書を読み込む（`ls -t ~/.claude/plans/*.md | head -1`）。見つからなければタスク説明を促して終了

### session_id / slug ルール

- 確認済みの関連 Issue がある場合は、その番号を `session_id` に使う。
- なければ PR 作成の有無によらず、タスクに基づく簡潔な英語 slug を `session_id` に使う。

## Phase 1: セットアップ + Admin 起動

### ステップ A: 許可されている場合だけ Issue を作成

`shiiman-github:issue-create` スキルのワークフローに従い、`--no-confirm` オプションで Issue を作成する。本文は「## 概要 / ## タスク一覧（チェックボックス）/ ## 完了条件」で構成。作成された Issue 番号を `session_id` と後続に使う。

### ステップ 1: ブランチ / worktree 作成

git モードのみ実施（no-git はスキップ）。

- worktree（既定）: `shiiman-github:worktree-create` スキルのワークフローに従う
- ブランチ: `shiiman-github:branch-create` スキルのワークフローに従う
- 確認済みの関連 Issue がある場合だけ Issue 番号を渡し、なければタスクに基づくブランチ名を使う。

### ステップ 2: Owner エージェント作成

```text
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent"]["id"] を {owner_id} として保存
```

### ステップ 3: Owner の役割を取得（🔴 必須）

```text
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

### ステップ 4: ワークスペース初期化

```text
mcp__multi-agent-mcp__init_tmux_workspace(
    working_dir="プロジェクトのルートパス",
    open_terminal=true,
    auto_setup_gtr=true,
    session_id="{session_id}",
    caller_agent_id="{owner_id}"
    # no-git モードのときのみ、以下を追加:
    # enable_git=false,
)
```

**no-git モードでは `enable_git=false` を必ず追加で渡す（git モードでは省略してよい）。**

### ステップ 5: Admin エージェント作成

```text
admin_result = mcp__multi-agent-mcp__create_agent(
    role="admin", working_dir="パス", caller_agent_id="{owner_id}"
)
# admin_result["agent"]["id"] を {admin_id} として保存
```

### ステップ 6: Admin に計画書を送信

```text
mcp__multi-agent-mcp__send_task(
    agent_id="{admin_id}",
    task_content="計画書またはタスク説明",
    session_id="{session_id}",
    branch_name="feature/{session_id}",  # git モードのみ。no-git では渡さない
    caller_agent_id="{owner_id}"
)
```

**no-git モードでは `branch_name` を渡さない。**

### ステップ 7: Admin の完了を待機

利用可能なエージェントの状態確認・待機ツールで完了を監視し、完了したら Phase 5 へ進む。続行のためにユーザーから状態確認を依頼されるのを待たない。

```text
mcp__multi-agent-mcp__get_dashboard_summary(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__read_messages(agent_id="{owner_id}", caller_agent_id="{owner_id}")
```

## Phase 2-4: Admin/Worker の自律実行

**自動制御。Owner は待機のみ。**

## Phase 5: 結果を検証して続行

### ステップ 1: 完了報告と変更内容を表示

```text
mcp__multi-agent-mcp__read_messages(agent_id="{owner_id}", caller_agent_id="{owner_id}")
```

git モード:

```bash
git status --short --branch
git diff
git diff --cached
```

no-git モード: Admin の最終報告（実装サマリー・変更ファイル・テスト結果・残課題）を表示。

### ステップ 2: 結果と許可の確認

実際の差分と検証結果を確認し、範囲内の対応すべき指摘を修正する。実装と後続操作が許可済みなら自動で続行する。重要な未解決の判断や未許可の影響についてだけ質問し、形式的な「OK」を待たない。

クリーンアップツールが削除する対象を確認する。今回のタスクが所有するエージェントと一時リソースだけを片付け、worktree・変更・有用なユーザーの作業は保持する。ツールで範囲を保証できなければ削除せず報告する。

### 検証後の処理

1. Admin に検証完了と許可済みの後続操作への移行を通知する。

   ```text
   mcp__multi-agent-mcp__send_message(
       sender_id="{owner_id}", receiver_id="{admin_id}",
       message_type="task_approved", content="検証完了。許可済みの範囲で後続処理へ進みます。",
       caller_agent_id="{owner_id}"
   )
   ```

2. クリーンアップ:

   ```text
   mcp__multi-agent-mcp__check_all_tasks_completed(caller_agent_id="{owner_id}")
   mcp__multi-agent-mcp__cleanup_on_completion(caller_agent_id="{owner_id}")
   ```

3. セキュリティチェック: 機密ファイル（`.env*` / `*.pem` / `credentials.json`）を検出したら警告

   ```bash
   git status   # git モード
   find . -maxdepth 3 \( -name ".env*" -o -name "*.pem" -o -name "credentials.json" \)  # no-git モード
   ```

4. 「仕上げ」へ進む

## 仕上げ

### 許可された仕上げ操作

1. 更新が許可された Issue のうち、実際に完了したタスクだけをチェックする。未完了タスクを完了にしない。
2. コミット: `shiiman-git:add-commit` スキルのワークフローに従い、`--no-confirm` オプションでコミットする
3. push または PR 作成が許可されていれば、remote・送信先・対象コミットを確認して実際の feature branch を通常の push で公開する。この許可だけで force-push、デフォルトブランチへの push、無関係な作業の公開は行わない。
4. PR 作成: `shiiman-github:pr-create` スキルのワークフローに従い、`--no-confirm` オプションで PR を作成する。日本語で概要・並列タスクの結果・検証結果を記載する。`Closes #N` は確認済みの関連 Issue がある場合だけ含め、なければ Issue 欄を省略する。
5. 実際の変更・チェック・完了した操作を報告する。Issue・PR の番号と URL は存在する場合だけ含め、未実行の操作を完了と主張しない。

### Issue/PR 連携なし（軽量）

実装だけの依頼では、変更と検証結果を報告して終了し、コミット・push・Issue・PR 作成は行わない。コミットだけの明示的な依頼では、検証して対象変更をコミットし、結果を報告する。任意の後続操作を追加で質問しない。

```text
## 実装完了

### 作成されたブランチ / worktree（git モード時のみ）
- {ブランチ名} / パス: {worktree のパス}（worktree モード時のみ）

### 推奨コミットメッセージ
{リポジトリとグローバル指示に従う Conventional Commits メッセージ}

### 検証結果
{実行したチェック・結果・残課題}

### worktree クリーンアップ（worktree モード時のみ）
PR マージ後、`/shiiman-git:worktree` で gtr rm または gtr clean を実行してください。
```

## 重要な注意事項

- ✅ ユーザーにフラグを入力させない（git・worktree/branch・計画書・Issue/PR を自動判断、曖昧なら確認）
- ✅ multi-agent-mcp のツールにだけ `caller_agent_id` を渡す
- ✅ no-git モードでは `enable_git=false` と `branch_name` 省略を徹底
- クリーンアップの範囲と作業の保護を確認し、形式的な完了承認は追加しない。
- コミットの規約はリポジトリとグローバル指示に従い、未対応の設定キーを仮定しない。
- 外部操作や Git の仕上げ操作は、それぞれ許可された範囲内だけで実行する。
