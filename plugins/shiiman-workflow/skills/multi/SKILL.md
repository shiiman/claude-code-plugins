---
name: shiiman-workflow:multi
description: MCP マルチエージェント（Owner/Admin/Worker）で並列実装する開発フロー。「マルチフロー」「workflow-multi」「マルチエージェントで実装」「並列で実装」「複数人で実装」「並列開発」などで起動。Issue/PR まで作るかは発話・引数から判断し、曖昧なら確認する。
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

multi-agent-mcp の Owner/Admin/Worker で並列実装する開発フロー。

フラグは不要。タスクを伝えれば、git の状態・発話内容から実行条件を自動判断し、曖昧な点だけ確認する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-workflow:multi - MCP マルチエージェント開発フロー

概要:
  multi-agent-mcp の Owner/Admin/Worker で並列実装する。
  実装条件（Issue/PR・計画書・ブランチ・git）はフラグ不要で自動判断し、
  曖昧な点だけ AskUserQuestion で確認する。

使用方法:
  /shiiman-workflow:multi [タスク説明]
  /shiiman-workflow:multi --help

オプション:
  --help  このヘルプを表示

例:
  /shiiman-workflow:multi                            # 既存計画書から並列実装（あれば）
  /shiiman-workflow:multi "API を並列リファクタ"      # タスク説明から並列実装
  /shiiman-workflow:multi "認証を実装して PR まで"    # Issue/PR 連携ありで並列実装
  /shiiman-workflow:multi --help                     # ヘルプを表示

指定の伝え方（フラグの代わり）:
  - 「計画を立ててから」  → plan mode で計画書を作成してから実装
  - 「ブランチで」        → worktree ではなくブランチを作成
  - 「Issue / PR まで」   → Issue 作成・PR 作成まで実施
  - 「コミットだけ」      → Issue/PR を作らずコミットメッセージ出力で終了
```

## 前提条件

- multi-agent-mcp がインストール済み（**必須**）
- tmux がインストール済み（**必須**）
- `gh` コマンドが利用可能
- `gh auth status` が成功する（GitHub CLI 認証済み）

## 環境変数

モデルプロファイルは環境変数で設定（`.env` または `export`）:

```bash
MCP_MODEL_PROFILE_ACTIVE=performance  # standard または performance
```

## ⚠️ caller_agent_id について（重要）

**全ての MCP ツールには `caller_agent_id` パラメータが必須です。**

- `create_agent()` の戻り値から自分の ID を取得し、`{owner_id}` として保存
- 以降の全ツール呼び出しで `caller_agent_id="{owner_id}"` を指定

## 起動時の自動判断（フラグの代わり）

ユーザーにフラグを入力させない。以下を順に決定する。**引数・発話に明示があればそれを最優先**し、明示がなければ自動判断、それでも曖昧な項目だけ後述の手順で確認する。

| 項目              | 既定       | 判断ルール                                                                                                      |
| ----------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
| git / no-git      | 自動       | `git rev-parse --is-inside-work-tree` 成功なら git。失敗なら no-git（ブランチ作成を省略）                       |
| worktree / branch | worktree   | 「ブランチで」「worktree なし」等の発話があれば branch                                                          |
| 計画書の扱い      | 後述の判定 | 「計画を立てて」「plan で」→ plan mode。引数にタスク説明あり → 直接。なし → 既存計画書を探索                    |
| Issue/PR 連携     | **要確認** | 「Issue」「PR」「プルリク」等あり → 連携あり。「コミットだけ」「Issue 不要」等 → 連携なし。どちらも無ければ確認 |

### Issue/PR 連携の確認

発話・引数から判断できない場合のみ、`AskUserQuestion` で 1 回だけ確認する。

```text
question: "どこまで実施しますか？"
options:
  - 軽量（コミットメッセージ出力のみ）: Issue/PR を作らず、変更とコミットメッセージの提示で終了
  - Issue/PR まで作成: Issue 作成 → 並列実装 → コミット → PR 作成まで実施
```

### git の状態判定

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1
```

- 成功 → git モード（ブランチ/worktree を作成、`init_tmux_workspace` は通常設定）
- 失敗 → no-git モード（ブランチ作成を省略、`init_tmux_workspace` に `enable_git=false` を渡す）

### 計画書の扱いの判定

1. 「計画を立ててから」等の依頼がある → **plan mode**: `EnterPlanMode` で計画書を作成・承認してから実装フェーズへ
2. 引数にタスク説明がある → **直接実行**: タスク説明をそのまま実装の指針にする
3. 引数なし → **既存計画書**: 最新の計画書を読み込む（`ls -t ~/.claude/plans/*.md | head -1`）。見つからなければタスク説明を促して終了

### session_id / slug ルール

- Issue/PR 連携あり → `session_id` に Issue 番号を使用
- 連携なし → タスク内容から簡潔な英語 slug を生成（生成できなければ `no-git-task`）

## Phase 1: セットアップ + Admin 起動

### ステップ A: Issue 作成（Issue/PR 連携ありのときのみ）

Skill ツールで `shiiman-github:issue-create --no-confirm` を呼び出す。本文は「## 概要 / ## タスク一覧（チェックボックス）/ ## 完了条件」で構成。作成された Issue 番号を `session_id` と後続に使う。

### ステップ 1: ブランチ / worktree 作成

git モードのみ実施（no-git はスキップ）。

- worktree（既定）: Skill ツールで `shiiman-github:worktree-create` を呼び出す
- ブランチ: Skill ツールで `shiiman-github:branch-create` を呼び出す
- Issue/PR 連携ありの場合は Issue 番号を引数に渡す

### ステップ 2: Owner エージェント作成

```text
owner_result = mcp__multi-agent-mcp__create_agent(role="owner", working_dir="パス")
# owner_result["agent"]["id"] を {owner_id} として保存
```

### ステップ 3: Owner の役割を取得（🔴 必須）

```text
mcp__multi-agent-mcp__get_role_guide(role="owner", caller_agent_id="{owner_id}")
```

### ステップ 4: MCP ワークスペース初期化

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

macOS 通知で Admin からの完了報告が届く。ユーザーから「完了通知来てるか確認して」と指示されたら Phase 5 へ。

```text
mcp__multi-agent-mcp__get_dashboard_summary(caller_agent_id="{owner_id}")
mcp__multi-agent-mcp__read_messages(agent_id="{owner_id}", caller_agent_id="{owner_id}")
```

## Phase 2-4: Admin/Worker の自律実行

**MCP が自動制御。Owner は待機のみ。**

## Phase 5: 結果確認 + ユーザー承認

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

### ステップ 2: ユーザー確認（🔴 必須）

**⚠️ クリーンアップの前に必ずユーザー確認を行う。**

```text
AskUserQuestion:
  question: "実装内容を承認しますか？"
  options:
    - OK（承認）: 後続処理へ進む
    - NG（修正依頼）: 修正内容を指定して Admin に再指示
    - 保留: 手動で確認してから判断
```

### NG（修正依頼）の場合

```text
mcp__multi-agent-mcp__send_message(
    sender_id="{owner_id}", receiver_id="{admin_id}",
    message_type="request", content="修正依頼: {ユーザーの修正内容}",
    caller_agent_id="{owner_id}"
)
```

→ Phase 2-4 に戻り、Admin が修正タスクを実行。

### OK（承認）の場合

1. Admin に承認通知:

   ```text
   mcp__multi-agent-mcp__send_message(
       sender_id="{owner_id}", receiver_id="{admin_id}",
       message_type="task_approved", content="ユーザー確認完了。実装を承認します。",
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

### Issue/PR 連携あり

1. Issue の全チェックボックスを完了に更新
2. コミット: Skill ツールで `shiiman-git:add-commit --no-confirm` を呼び出す
3. プッシュ案内（自動実行しない）: `git push -u origin feature/{session_id}`
4. PR 作成: Skill ツールで `shiiman-github:pr-create --no-confirm` を呼び出す。本文は「## 概要 / ## 並列実行サマリー（Worker×Task の表）/ ## 関連 Issue（`Closes #{issue番号}`）/ ## テスト計画」
5. 完了報告（Issue 番号・ブランチ/worktree・PR 番号/URL・worktree クリーンアップ案内）

### Issue/PR 連携なし（軽量）

**コミット・プッシュ・PR 作成は行わない。** 推奨コミットメッセージを出力して終了する。

```text
## 実装完了

### 作成されたブランチ / worktree（git モード時のみ）
- {ブランチ名} / パス: {worktree のパス}（worktree モード時のみ）

### 推奨コミットメッセージ
{Conventional Commits 形式（`.claude/settings.json` の git.commitMessage 設定があればそれに従う）}

### 次のステップ
git push -u origin feature/{session_id}
必要に応じて gh pr create

### worktree クリーンアップ（worktree モード時のみ）
PR マージ後、`/shiiman-git:worktree` で gtr rm または gtr clean を実行してください。
```

## 重要な注意事項

- ✅ ユーザーにフラグを入力させない（git・worktree/branch・計画書・Issue/PR を自動判断、曖昧なら確認）
- ✅ 全 MCP ツールに `caller_agent_id` を渡す
- ✅ no-git モードでは `enable_git=false` と `branch_name` 省略を徹底
- ✅ クリーンアップ前に必ずユーザー確認を行う
- ✅ コミットメッセージは `.claude/settings.json` の設定に従う（なければ Conventional Commits）
- ❌ Issue/PR 連携なしのときは自動でコミット・プッシュ・PR を作らない
