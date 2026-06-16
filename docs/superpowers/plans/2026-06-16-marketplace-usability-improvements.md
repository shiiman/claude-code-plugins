# マーケットプレイス使いやすさ改善（A/B/C）実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** root README のワークフロー記述を現行構成に修正し（A）、Gmail/Slack 等のトリガー衝突をドメイン固有化で解消し（B）、allowed-tools 欠落 5 スキルを安全に補完する（C）。

**Architecture:** SKILL.md フロントマター（`description` / `allowed-tools`）と README の Markdown 編集のみ。新規ロジックなし。このリポジトリにスキル定義用のユニットテストは無いため、各タスクの「検証」は grep による文字列確認と `npm run format:check` で行う（TDD のテスト＝検証コマンド）。

**Tech Stack:** Markdown（Prettier, `proseWrap: preserve`）、JSON（plugin.json / marketplace.json）、Bash（grep 検証）。

**実装順序:** A → C → B → バージョン bump → 整形・最終検証・コミット（A/C は機械的で低リスク、B は文言調整、最後にまとめて bump とコミット）。

**作業ディレクトリ（必須）:** `/Users/a12665/Documents/personal/claude-code-plugins/.claude/worktrees/refactor+workflow-flagless`

**前提:** 直近コミット `daf1bd4`（workflow v5.0.0）/ `f8d40cd`（GitHub 系フラグ廃止）/ `ea8a36e`（本設計スペック）の上に積む。

**スペック:** `docs/superpowers/specs/2026-06-16-marketplace-usability-improvements-design.md`

---

## ファイル構成（変更対象）

- Modify: `README.md`（A: ワークフロー表）
- Modify: `plugins/shiiman-go/skills/check/SKILL.md`（C: allowed-tools）
- Modify: `plugins/shiiman-google/skills/notebooklm-deepresearch/SKILL.md`（C: allowed-tools）
- Modify: `plugins/shiiman-google/skills/notebooklm-infographic/SKILL.md`（C: allowed-tools）
- Modify: `plugins/shiiman-google/skills/notebooklm-report/SKILL.md`（C: allowed-tools）
- Modify: `plugins/shiiman-google/skills/notebooklm-slide/SKILL.md`（C: allowed-tools）
- Modify: `plugins/shiiman-google/skills/gmail-unread-check/SKILL.md`（B: description）
- Modify: `plugins/shiiman-google/skills/gmail-unread-mark/SKILL.md`（B: description）
- Modify: `plugins/shiiman-slack/skills/unread-check/SKILL.md`（B: description）
- Modify: `plugins/shiiman-slack/skills/unread-mark/SKILL.md`（B: description）
- Modify: `plugins/shiiman-github/skills/pr-list/SKILL.md`（B: description）
- Modify: `plugins/shiiman-github/skills/issue-list/SKILL.md`（B: description）
- Modify: `plugins/shiiman-github/skills/setup/SKILL.md`（B: description）
- Modify: `plugins/shiiman-go/skills/mod-update/SKILL.md`（B: description）
- Modify: `plugins/shiiman-google/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`（bump 3.4.1→3.4.2）
- Modify: `plugins/shiiman-slack/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`（bump 4.1.1→4.1.2）
- Modify: `plugins/shiiman-github/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`（bump 4.3.0→4.3.1）
- Modify: `plugins/shiiman-go/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`（bump 3.1.0→3.1.1）

---

## Task 1: A — root README のワークフロー表を現行 4 スキルに修正

**Files:**

- Modify: `README.md`（「### ワークフロー」表、現状 L122-131 付近）

- [ ] **Step 1: 現状を確認（テスト＝旧名が存在することを確認）**

Run: `grep -nE "workflow-(single|multi|agent-team)" README.md`
Expected: L126-131 に `workflow-single-issue` 等 6 行がヒットする（修正前の状態）。

- [ ] **Step 2: ワークフロー表を置換**

`README.md` の「### ワークフロー」見出し直後の表（旧 6 行）を以下のブロックに置き換える。`old_string` は現状のブロック全体、`new_string` は下記。

old_string（現状）:

```text
### ワークフロー

| スキル                    | プラグイン       | トリガー例                                              | 説明                                                             |
| ------------------------- | ---------------- | ------------------------------------------------------- | ---------------------------------------------------------------- |
| workflow-single-issue     | shiiman-workflow | 「シングル Issue フロー」「Issue から PR まで」         | Issue 作成から PR 作成まで自動実行するシングルエージェントフロー |
| workflow-multi-issue      | shiiman-workflow | 「マルチ Issue フロー」「並列 Issue 開発」              | MCP マルチエージェントで Issue から PR まで並列実行              |
| workflow-single           | shiiman-workflow | 「シングルフロー」「軽量フロー」                        | Issue/PR なしで計画書からタスク実行する軽量フロー                |
| workflow-multi            | shiiman-workflow | 「マルチフロー」「並列軽量フロー」                      | MCP マルチエージェントで Issue/PR なしに並列実行する軽量フロー   |
| workflow-agent-team-issue | shiiman-workflow | 「Agent Team Issue」「エージェントチーム Issue フロー」 | Agent Team で Issue から PR まで並列実行                         |
| workflow-agent-team       | shiiman-workflow | 「エージェントチームフロー」「Agent Team で実装」       | Agent Team で Issue/PR なしに並列実行する軽量フロー              |
```

new_string（修正後）:

```text
### ワークフロー

フラグ不要。Issue/PR 連携・git・計画書・ブランチ/worktree は発話・引数から自動判断し、曖昧なときだけ確認する（v5.0.0）。実行スタイルでスキルを選ぶ。

| スキル                 | プラグイン       | トリガー例                           | 説明                                                   |
| ---------------------- | ---------------- | ------------------------------------ | ------------------------------------------------------ |
| single                 | shiiman-workflow | 「シングルフロー」「順次実装」       | 1 エージェントで順次実装                               |
| multi                  | shiiman-workflow | 「マルチフロー」「並列で実装」       | MCP マルチエージェント（Owner/Admin/Worker）で並列実装 |
| agent-team             | shiiman-workflow | 「エージェントチームフロー」         | Agent Team（tmux + TeamCreate）で並列実装              |
| issue-branch-pr-create | shiiman-workflow | 「変更から Issue と PR」「Backward」 | 既存変更から Issue・ブランチ・PR を作る逆方向フロー     |
```

（表のパイプ整列は後段の `npm run format` が正規化するため、桁合わせは厳密でなくてよい。）

- [ ] **Step 3: 検証（旧名が消え、新名のみになったことを確認）**

Run: `grep -nE "workflow-(single|multi|agent-team)" README.md`
Expected: 出力なし（旧名が完全に消えている）。

Run: `grep -nE "^\| (single|multi|agent-team|issue-branch-pr-create) +\|" README.md`
Expected: 4 行ヒット。

---

## Task 2: C — allowed-tools 欠落 5 スキルを補完

NotebookLM 4 スキルは現在 allowed-tools 無しで動作している。MCP ツールは全て `mcp__notebooklm-mcp__` 接頭辞のため、ワイルドカード 1 つで全てカバーできる（取りこぼし防止）。非 MCP は Bash / AskUserQuestion のみ使用だが、入力読み取りの可能性を考え Read も保守的に含める。

**Files:**

- Modify: `plugins/shiiman-go/skills/check/SKILL.md`
- Modify: `plugins/shiiman-google/skills/notebooklm-deepresearch/SKILL.md`
- Modify: `plugins/shiiman-google/skills/notebooklm-infographic/SKILL.md`
- Modify: `plugins/shiiman-google/skills/notebooklm-report/SKILL.md`
- Modify: `plugins/shiiman-google/skills/notebooklm-slide/SKILL.md`

- [ ] **Step 1: go:check に allowed-tools を追加**

`plugins/shiiman-go/skills/check/SKILL.md` のフロントマターを編集。

old_string:

```text
name: shiiman-go:check
description: Go プロジェクトの品質を総合チェックする。「Go チェック」「go check」「コード品質チェック」「lint して」「テスト実行」「脆弱性スキャン」「パフォーマンス確認」「コードレビュー」「品質確認」「総合診断」などで起動。テスト・静的解析・脆弱性スキャン・ベンチマーク・コードレビューを並列実行し統合レポートを出力。
argument-hint: "[--help]"
```

new_string:

```text
name: shiiman-go:check
description: Go プロジェクトの品質を総合チェックする。「Go チェック」「go check」「コード品質チェック」「lint して」「テスト実行」「脆弱性スキャン」「パフォーマンス確認」「コードレビュー」「品質確認」「総合診断」などで起動。テスト・静的解析・脆弱性スキャン・ベンチマーク・コードレビューを並列実行し統合レポートを出力。
allowed-tools: [Read, Bash, Glob, Grep, Task]
argument-hint: "[--help]"
```

- [ ] **Step 2: NotebookLM 4 スキルに allowed-tools を追加**

4 ファイルそれぞれで、`description:` 行と `argument-hint:` 行の間に `allowed-tools` 行を挿入する。挿入する行は 4 ファイル共通:

```text
allowed-tools: [Read, Bash, AskUserQuestion, mcp__notebooklm-mcp__*]
```

各ファイルの編集（old → new、`{DESC}` 部分は各ファイル既存の description をそのまま使うこと）:

- `notebooklm-deepresearch/SKILL.md`:
  - old:
    ```text
    description: NotebookLM でディープリサーチ（Web 調査）を実行する。「NotebookLM リサーチ」「NotebookLM で調査」「NotebookLM ディープリサーチ」「NotebookLM で調べて」などで起動。notebooklm-mcp を使用。
    argument-hint: "[--help]"
    ```
  - new:
    ```text
    description: NotebookLM でディープリサーチ（Web 調査）を実行する。「NotebookLM リサーチ」「NotebookLM で調査」「NotebookLM ディープリサーチ」「NotebookLM で調べて」などで起動。notebooklm-mcp を使用。
    allowed-tools: [Read, Bash, AskUserQuestion, mcp__notebooklm-mcp__*]
    argument-hint: "[--help]"
    ```
- `notebooklm-infographic/SKILL.md`:
  - old:
    ```text
    description: NotebookLM でインフォグラフィックを作成する。「NotebookLM インフォグラフィック」「NotebookLM で図解」「NotebookLM 視覚化」「NotebookLM でインフォグラフィック」などで起動。notebooklm-mcp を使用。
    argument-hint: "[--help]"
    ```
  - new:
    ```text
    description: NotebookLM でインフォグラフィックを作成する。「NotebookLM インフォグラフィック」「NotebookLM で図解」「NotebookLM 視覚化」「NotebookLM でインフォグラフィック」などで起動。notebooklm-mcp を使用。
    allowed-tools: [Read, Bash, AskUserQuestion, mcp__notebooklm-mcp__*]
    argument-hint: "[--help]"
    ```
- `notebooklm-report/SKILL.md`:
  - old:
    ```text
    description: NotebookLM でレポート・ブリーフィングを作成する。「NotebookLM レポート」「NotebookLM ブリーフィング」「NotebookLM 学習ガイド」「NotebookLM ブログポスト」などで起動。notebooklm-mcp を使用。
    argument-hint: "[--help]"
    ```
  - new:
    ```text
    description: NotebookLM でレポート・ブリーフィングを作成する。「NotebookLM レポート」「NotebookLM ブリーフィング」「NotebookLM 学習ガイド」「NotebookLM ブログポスト」などで起動。notebooklm-mcp を使用。
    allowed-tools: [Read, Bash, AskUserQuestion, mcp__notebooklm-mcp__*]
    argument-hint: "[--help]"
    ```
- `notebooklm-slide/SKILL.md`:
  - old:
    ```text
    description: NotebookLM でスライドデッキを作成する。「NotebookLM スライド」「NotebookLM スライドデッキ」「NotebookLM プレゼン」「NotebookLM デッキ」などで起動。notebooklm-mcp を使用。
    argument-hint: "[--help]"
    ```
  - new:
    ```text
    description: NotebookLM でスライドデッキを作成する。「NotebookLM スライド」「NotebookLM スライドデッキ」「NotebookLM プレゼン」「NotebookLM デッキ」などで起動。notebooklm-mcp を使用。
    allowed-tools: [Read, Bash, AskUserQuestion, mcp__notebooklm-mcp__*]
    argument-hint: "[--help]"
    ```

- [ ] **Step 3: 検証（取りこぼしゼロを確認）**

各 NotebookLM スキルについて、本文で参照される全 MCP ツールが `mcp__notebooklm-mcp__` 接頭辞であること（＝ワイルドカードで全てカバー）を確認:

Run:

```bash
for f in notebooklm-deepresearch notebooklm-infographic notebooklm-report notebooklm-slide; do
  echo "== $f =="
  grep -oE 'mcp__[a-z0-9_-]+__[a-z_]+' "plugins/shiiman-google/skills/$f/SKILL.md" | grep -v '^mcp__notebooklm-mcp__' || echo "  (notebooklm-mcp 以外の MCP ツールなし=OK)"
done
```

Expected: 各スキルで「notebooklm-mcp 以外の MCP ツールなし=OK」と表示される。

Run:

```bash
grep -L "allowed-tools" plugins/shiiman-go/skills/check/SKILL.md plugins/shiiman-google/skills/notebooklm-*/SKILL.md
```

Expected: 出力なし（全ファイルに allowed-tools が存在）。

---

## Task 3: B — トリガー衝突をドメイン固有化（8 スキルの description）

frontmatter の `description` のみ編集（本文の「伝え方」説明は変更しない）。

**Files:**

- Modify: `plugins/shiiman-google/skills/gmail-unread-check/SKILL.md`
- Modify: `plugins/shiiman-slack/skills/unread-check/SKILL.md`
- Modify: `plugins/shiiman-google/skills/gmail-unread-mark/SKILL.md`
- Modify: `plugins/shiiman-slack/skills/unread-mark/SKILL.md`
- Modify: `plugins/shiiman-github/skills/pr-list/SKILL.md`
- Modify: `plugins/shiiman-github/skills/issue-list/SKILL.md`
- Modify: `plugins/shiiman-github/skills/setup/SKILL.md`
- Modify: `plugins/shiiman-go/skills/mod-update/SKILL.md`

- [ ] **Step 1: gmail-unread-check の description（汎用語をメール固有化）**

old:

```text
description: Gmail の未読メッセージ一覧を取得する。「未読メール」「Gmail 未読」「未読一覧」「未読メールを見たい」「未読メッセージ」「メールの未読」「全アカウントの未読」などで起動。
```

new:

```text
description: Gmail の未読メッセージ一覧を取得する。「未読メール」「Gmail 未読」「Gmail の未読一覧」「未読メールを見たい」「メールの未読」「Gmail 未読メッセージ」「全アカウントの未読メール」などで起動。
```

- [ ] **Step 2: slack:unread-check の description（誤誘導語削除＋Slack 固有化）**

old:

```text
description: Slack の未読メッセージを確認する（全チャンネル横断確認対応）。「Slack未読確認」「未読メッセージ」「未読ある？」「Slackの未読」「未読を見せて」「未読チェック」「未読メール確認」「全チャンネルの未読」「未読サマリー」などで起動。Pythonスクリプト `slack_message.py unread` を使用。
```

new:

```text
description: Slack の未読メッセージを確認する（全チャンネル横断確認対応）。「Slack未読確認」「Slack の未読メッセージ」「Slack 未読ある？」「Slackの未読」「Slack 未読を見せて」「Slack 未読チェック」「全チャンネルの未読」「Slack 未読サマリー」などで起動。Pythonスクリプト `slack_message.py unread` を使用。
```

- [ ] **Step 3: gmail-unread-mark の description（汎用語をメール固有化）**

old:

```text
description: Gmail の未読を既読化する。「既読にする」「未読を既読」「メールを既読化」「Gmail 既読化」「未読を消す」「メールを開封扱い」「一括既読」などで起動。
```

new:

```text
description: Gmail の未読を既読化する。「メールを既読にする」「メールの未読を既読」「メールを既読化」「Gmail 既読化」「Gmail の未読を消す」「メールを開封扱い」「メールを一括既読」などで起動。
```

- [ ] **Step 4: slack:unread-mark の description（全トリガーを Slack 固有化）**

old:

```text
description: Slack チャンネルを既読にする（全チャンネル一括既読化対応）。「既読にして」「既読化」「チャンネル既読」「未読を消す」「既読マーク」「全部読んだことにして」「既読にしたい」「全部既読」「一括既読」などで起動。Pythonスクリプト `slack_message.py mark-read` を使用。
```

new:

```text
description: Slack チャンネルを既読にする（全チャンネル一括既読化対応）。「Slack を既読にして」「Slack 既読化」「Slack チャンネル既読」「Slack の未読を消す」「Slack 既読マーク」「Slack を全部読んだことにして」「Slack 全部既読」「Slack を一括既読」などで起動。Pythonスクリプト `slack_message.py mark-read` を使用。
```

- [ ] **Step 5: pr-list の description（「自分の」→「自分の PR」）**

old:

```text
「マージ済みも」「自分の」などの絞り込みは発話から判断する。
```

new:

```text
「マージ済みも」「自分の PR」などの絞り込みは発話から判断する。
```

- [ ] **Step 6: issue-list の description（「自分の」→「自分の Issue」）**

old:

```text
「クローズ済みも」「自分の」などの絞り込みは発話から判断する。
```

new:

```text
「クローズ済みも」「自分の Issue」などの絞り込みは発話から判断する。
```

- [ ] **Step 7: setup の description（「確認だけ」→ GitHub 文脈の語）**

old:

```text
.github ディレクトリに必要な設定ファイルを一括生成。「確認だけ」と伝えれば生成予定の一覧表示のみ行う。
```

new:

```text
.github ディレクトリに必要な設定ファイルを一括生成。「何が作られるか確認」と伝えれば生成予定の一覧表示のみ行う。
```

- [ ] **Step 8: mod-update の description（「確認だけ」→ Go 文脈の語）**

old:

```text
更新後は check で品質チェックを自動実行。「確認だけ」と伝えれば更新せず一覧表示のみ行う。
```

new:

```text
更新後は check で品質チェックを自動実行。「更新可能か確認」と伝えれば更新せず一覧表示のみ行う。
```

- [ ] **Step 9: 検証（ドメイン非明示の汎用衝突フレーズが description から消えたことを確認）**

Run:

```bash
# Gmail/Slack の description に「未読メール確認」が残っていないか
grep -n "未読メール確認" plugins/shiiman-slack/skills/unread-check/SKILL.md && echo "NG: 残存" || echo "OK: 削除済み"

# description 行に単独の汎用フレーズが無いか（description 行のみ対象）
grep -h "^description:" plugins/shiiman-google/skills/gmail-unread-check/SKILL.md plugins/shiiman-slack/skills/unread-check/SKILL.md plugins/shiiman-google/skills/gmail-unread-mark/SKILL.md plugins/shiiman-slack/skills/unread-mark/SKILL.md | grep -E "「未読メッセージ」|「未読を消す」|「一括既読」|「既読にする」" && echo "NG: 汎用語残存" || echo "OK: 汎用語なし"

# setup/mod-update/pr-list/issue-list の description 行に単独「確認だけ」「自分の」が無いか
grep -h "^description:" plugins/shiiman-github/skills/setup/SKILL.md plugins/shiiman-go/skills/mod-update/SKILL.md | grep "「確認だけ」" && echo "NG: 確認だけ残存" || echo "OK"
grep -h "^description:" plugins/shiiman-github/skills/pr-list/SKILL.md plugins/shiiman-github/skills/issue-list/SKILL.md | grep "「自分の」" && echo "NG: 自分の残存" || echo "OK"
```

Expected: 全て「OK」と表示される。

---

## Task 4: バージョン bump（4 プラグイン × plugin.json + marketplace.json）

全て PATCH。plugin.json と marketplace.json を一致させる。

**Files:**

- Modify: `plugins/shiiman-google/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json`
- Modify: `plugins/shiiman-slack/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json`
- Modify: `plugins/shiiman-github/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json`
- Modify: `plugins/shiiman-go/.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json`

- [ ] **Step 1: plugin.json の version を更新**

各 plugin.json の `"version"` 行（3 行目）を更新:

- `plugins/shiiman-google/.claude-plugin/plugin.json`: `"version": "3.4.1",` → `"version": "3.4.2",`
- `plugins/shiiman-slack/.claude-plugin/plugin.json`: `"version": "4.1.1",` → `"version": "4.1.2",`
- `plugins/shiiman-github/.claude-plugin/plugin.json`: `"version": "4.3.0",` → `"version": "4.3.1",`
- `plugins/shiiman-go/.claude-plugin/plugin.json`: `"version": "3.1.0",` → `"version": "3.1.1",`

- [ ] **Step 2: marketplace.json の version を更新**

`.claude-plugin/marketplace.json` 内の各プラグインブロックの version を更新する。version 値は他プラグインと重複しうるため、直前の `"name"` 行を含めて一意に置換すること。

- shiiman-google ブロック: `"name": "shiiman-google",` を含むブロック内の `"version": "3.4.1",` → `"version": "3.4.2",`
- shiiman-slack ブロック: `"version": "4.1.1",` → `"version": "4.1.2",`
- shiiman-github ブロック: `"version": "4.3.0",` → `"version": "4.3.1",`
- shiiman-go ブロック: `"version": "3.1.0",` → `"version": "3.1.1",`

（github 4.3.0 / google 3.4.1 / slack 4.1.1 は marketplace.json 内で一意。go の 3.1.0 は一意。重複が無いことを Step 3 で確認する。）

- [ ] **Step 3: 検証（plugin.json と marketplace.json の一致）**

Run:

```bash
for p in google slack github go; do
  pj=$(grep -m1 '"version"' "plugins/shiiman-$p/.claude-plugin/plugin.json" | tr -dc '0-9.')
  mp=$(grep -A3 "\"name\": \"shiiman-$p\"" .claude-plugin/marketplace.json | grep version | tr -dc '0-9.')
  printf "%-8s plugin=%s marketplace=%s %s\n" "$p" "$pj" "$mp" "$([ "$pj" = "$mp" ] && echo OK || echo MISMATCH)"
done
```

Expected: google=3.4.2, slack=4.1.2, github=4.3.1, go=3.1.1, 全て OK。

---

## Task 5: 整形・最終検証・コミット

- [ ] **Step 1: Markdown を整形**

Run: `npm run format`
Expected: エラーなく完了（表のパイプ整列などが正規化される）。

- [ ] **Step 2: 整形チェック**

Run: `npm run format:check`
Expected: `All matched files use Prettier code style!`

- [ ] **Step 3: 全体最終検証（A/B/C をまとめて確認）**

Run:

```bash
# A
grep -cE "workflow-(single|multi|agent-team)" README.md   # => 0
# B（汎用衝突語の不在）
grep -h "^description:" plugins/shiiman-slack/skills/unread-check/SKILL.md | grep -c "未読メール確認"  # => 0
# C（allowed-tools 欠落なし）
grep -L "allowed-tools" plugins/*/skills/*/SKILL.md | wc -l  # => 0
```

Expected: README の旧名 0 件、未読メール確認 0 件、allowed-tools 欠落 0 件。

- [ ] **Step 4: 変更内容をユーザーに提示し、コミット可否を確認**

このリポジトリのルール（コミットはユーザー明示依頼時のみ）に従い、`git status` と差分要約を提示してコミット可否を確認する。承認後に以下でコミット（`--no-verify` 禁止）:

```bash
git add -A
git commit -m "$(cat <<'EOF'
fix: トリガー衝突解消・allowed-tools 補完・README 整合 (google v3.4.2 / slack v4.1.2 / github v4.3.1 / go v3.1.1)

- A: root README のワークフロー表を現行4スキル（single/multi/agent-team/issue-branch-pr-create）に修正
- B: Gmail⇄Slack の未読/既読、setup/mod-update・pr-list/issue-list のトリガーをドメイン固有化
- C: go:check と NotebookLM 4スキルの allowed-tools 欠落を補完（NotebookLM は mcp__notebooklm-mcp__* で全カバー）
- plugin.json と marketplace.json のバージョンを一致更新（全て PATCH）
EOF
)"
```

（バージョン bump がプラグインをまたぐため単一コミットとする。プラグインごとに分割したい場合は B/C をプラグイン単位で分けてもよい。）

---

## 自己レビュー結果（writing-plans Self-Review）

- **スペック網羅**: A（Task 1）/ B（Task 3 の 8 ステップ）/ C（Task 2）/ バージョン bump（Task 4）/ 整形・検証（Task 5）を全てカバー。スペックの検証項目（grep 照合・format:check・version 一致）を各タスクに反映済み。
- **プレースホルダ走査**: TBD/TODO なし。全 description の old/new 文字列、allowed-tools の正確な値、bump の正確なバージョンを明記。「実装時に判断」系の曖昧ステップなし（C の MCP は接頭辞統一を確認済みのためワイルドカードで確定）。
- **型/名称整合**: スキル名・ファイルパス・バージョン番号はスペックおよび現行ファイルと一致。NotebookLM 4 スキルへ追加する allowed-tools 行は 4 ファイル共通の一文で統一。
