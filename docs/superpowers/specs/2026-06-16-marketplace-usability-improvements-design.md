# マーケットプレイス使いやすさ改善（A: ドキュメント整合 / B: トリガー衝突解消 / C: allowed-tools 補完）

- 作成日: 2026-06-16
- 対象リポジトリ: shiiman/claude-code-plugins
- 作業ブランチ: worktree-refactor+workflow-flagless
- 関連: 直近の workflow フラグ廃止（v5.0.0, `daf1bd4`）/ GitHub 系 9 スキルのフラグ廃止（`f8d40cd`）の続き

## 背景

「AI 操作プラグインとして使いづらい」という課題に対し、これまで (1) workflow のフラグ廃止・7→4 統合、(2) review/worktree/NotebookLM/更新系のトリガー衝突解消を実施した。本スペックは、その後の全体監査（構造一貫性・発見性・重複/欠落の 3 観点を並列調査）で**実ファイル検証により確定した**改善点のうち、ユーザーが対象に選んだ 3 バケット（A/B/C）を扱う。

### 監査で除外した誤指摘（対応しない）

実ファイル検証の結果、以下は誤りまたは過剰提案だったため対象外とする。

- 「`shiiman-common:review` の YAML フロントマターが破損」→ 実際は正常な複数行フロー配列。
- 「`context: fork` が GitHub/git/Slack 全スキルで必須」→ 実際は 48 中 10 スキルで、書き込み・重い処理系に**意図的**に付与。欠落は規約違反ではない。
- 「plugin.json に agents/hooks を明示登録すべき」→ Claude Code はディレクトリを自動探索するため不要。
- 同一スキル内の語尾違いトリガー（「Drive を検索」/「Drive で検索」等）→ 意図的な堅牢化。
- セクション構成・argument-hint 形式・frontmatter 順序の全面統一 → 低価値・churn 大（YAGNI のため見送り）。

## ゴール

- **A**: root README.md のワークフロー表に残る旧スキル名を現行構成に修正する。
- **B**: トリガー（description）衝突を「ドメイン固有化」方針で解消する。
- **C**: allowed-tools が欠落している 5 スキルに、実際に使うツールを安全に補完する。

## スコープ外（今回見送り）

- **D（機能ギャップ・新スキル新設）**: `pr-merge` / `issue-close` / `branch-delete` 等。スコープ拡大のため別途。
- **E（体裁の全面標準化）**: セクション構成・argument-hint・frontmatter 順序の統一。YAGNI。

---

## A. ドキュメント整合

### 問題

`README.md`（リポジトリルート）L124-131 の「### ワークフロー」表が、削除済み/旧名のスキルを記載している。

- 旧 `workflow-` プレフィックス付き（v3.0.0 で廃止済み）
- `workflow-single-issue` / `workflow-multi-issue` / `workflow-agent-team-issue`（v5.0.0 で統合・削除済み）

CLAUDE.md と `plugins/shiiman-workflow/README.md` は既に現行 4 スキルへ更新済みで、**root README.md だけが更新漏れ**。プラグイン管理節・開発ツール節は正確。

### 変更

`README.md` の「### ワークフロー」表を、現行 4 スキルに置換する。

| スキル                 | プラグイン       | トリガー例                           | 説明                                          |
| ---------------------- | ---------------- | ------------------------------------ | --------------------------------------------- |
| single                 | shiiman-workflow | 「シングルフロー」「順次実装」       | 1 エージェントで順次実装                      |
| multi                  | shiiman-workflow | 「マルチフロー」「並列で実装」       | MCP マルチエージェント（Owner/Admin/Worker）  |
| agent-team             | shiiman-workflow | 「エージェントチームフロー」         | Agent Team（tmux + TeamCreate）で並列実装     |
| issue-branch-pr-create | shiiman-workflow | 「変更から Issue と PR」「Backward」 | 既存変更から Issue・ブランチ・PR を作る逆方向 |

- 表の直後に「Issue/PR 連携・git・計画書・ブランチ/worktree はフラグ不要で発話・引数から自動判断し、曖昧なときだけ確認する（v5.0.0）」を一文補足する。
- 他セクションは変更しない。

### 検証

- 修正後、`README.md` に `workflow-single-issue` / `workflow-multi-issue` / `workflow-agent-team-issue` / 旧 `workflow-` プレフィックスが残っていないこと（grep）。
- `single` / `multi` / `agent-team` / `issue-branch-pr-create` の 4 つのみが記載されていること。

---

## B. トリガー衝突の解消（方針: ドメイン固有化）

### 原則

**全トリガーフレーズにドメイン語（メール/Gmail・Slack・GitHub・Go）を含める。どのドメインも名指さない汎用フレーズは削除または限定する。** これは review/worktree/NotebookLM で既に適用した原則の踏襲。これにより、別ドメインのスキルへ誤起動するリスクを構造的に防ぐ。

### B-1. Gmail ⇄ Slack（クロスプラグイン衝突・重大度 高）

確定した衝突: 「未読メッセージ」「未読を消す」「一括既読」が Gmail/Slack 双方に存在。さらに `slack:unread-check` が「未読メール確認」という Gmail 誤誘導トリガーを保持。

対象 4 スキルの description トリガー語を以下方針で書き換える（最終文言は実装時に微調整可だが、**汎用語の除去とドメイン語の付与は必須**）。

- `plugins/shiiman-google/skills/gmail-unread-check`
  - 除去/限定: 「未読メッセージ」「未読一覧」「全アカウントの未読」（ドメイン非明示）
  - 目標トリガー例: 「未読メール」「Gmail 未読」「Gmail の未読一覧」「未読メールを見たい」「メールの未読」「全アカウントの未読メール」
- `plugins/shiiman-slack/skills/unread-check`
  - 除去: 「未読メール確認」（Gmail 誤誘導）、ドメイン非明示の「未読メッセージ」「未読を見せて」等
  - 目標トリガー例: 「Slack 未読確認」「Slack の未読メッセージ」「Slack の未読」「Slack 未読チェック」「全チャンネルの未読」「Slack 未読サマリー」
- `plugins/shiiman-google/skills/gmail-unread-mark`
  - 除去/限定: 「既読にする」「未読を消す」「一括既読」（ドメイン非明示）
  - 目標トリガー例: 「メールを既読にする」「メールの未読を既読」「Gmail 既読化」「Gmail の未読を消す」「メールを一括既読」
- `plugins/shiiman-slack/skills/unread-mark`
  - 限定: 「既読にして」「未読を消す」「一括既読」等にすべて Slack を付与
  - 目標トリガー例: 「Slack を既読にして」「Slack 既読化」「Slack チャンネル既読」「Slack の未読を消す」「Slack を全部既読」「Slack を一括既読」

### B-2. 自己起因の衝突（前コミットで混入・重大度 中〜低）

- `plugins/shiiman-github/skills/setup` と `plugins/shiiman-go/skills/mod-update`
  - 問題: 双方の description に確認モードを示す「確認だけ」が単独フレーズで入っている。
  - 変更: 「確認だけ」を単独トリガーにしない。ドメイン明示の確認フレーズに置き換える。
    - setup: 「何が作られるか確認」など GitHub 設定文脈の語に。
    - mod-update: 「更新可能か確認」「更新せず確認」など Go モジュール文脈の語に。
- `plugins/shiiman-github/skills/pr-list` と `plugins/shiiman-github/skills/issue-list`
  - 問題: 双方の description に絞り込み語「自分の」が単独で入っている。
  - 変更: pr-list は「自分の PR」、issue-list は「自分の Issue」に限定する。

### 検証

- 修正後、Gmail/Slack の 4 スキル description に**ドメイン語を含まない**未読/既読トリガー（「未読メッセージ」「未読を消す」「一括既読」「既読にする」単独等）が残っていないこと。
- `slack:unread-check` に「未読メール確認」が無いこと。
- setup/mod-update に単独の「確認だけ」、pr-list/issue-list に単独の「自分の」が無いこと。
- 各 description が自然な日本語で、過剰に長くなっていないこと（目視）。

---

## C. allowed-tools 補完（方針: 安全側で正確に）

### 問題

以下 5 スキルに allowed-tools フィールドが無い。他スキルは全て宣言済みのため不整合。

- `plugins/shiiman-go/skills/check`
- `plugins/shiiman-google/skills/notebooklm-deepresearch`
- `plugins/shiiman-google/skills/notebooklm-infographic`
- `plugins/shiiman-google/skills/notebooklm-report`
- `plugins/shiiman-google/skills/notebooklm-slide`

### 重要なリスク

NotebookLM 4 スキルは現在 allowed-tools 無しで**動作している**（省略時は広い権限を継承していると考えられる）。限定リストを付ける際に、本文に現れる MCP ツールを 1 つでも取りこぼすと、**かえって機能を壊す**。したがって取りこぼし防止を最優先する。

### 変更

- `go:check`: `allowed-tools: [Read, Bash, Glob, Grep, Task]`
  - 本文はプロジェクト構造検出（Bash/Read/Glob）＋ 5 チェックを Task サブエージェント（subagent_type: Bash / general-purpose）で並列実行。
- NotebookLM 4 スキル: `[Read, Bash, AskUserQuestion]` ＋ notebooklm-mcp の全使用ツール。
  - **第一候補**: ワイルドカード `mcp__notebooklm-mcp__*` を使用。
  - **ワイルドカードが許可されない形式の場合**: 各スキル本文で参照される `mcp__notebooklm-mcp__*` を全て列挙する。現時点で観測されたツール（union、実装時に各スキルごとに再確認）:
    - `notebook_create` / `notebook_list` / `note_create`
    - `source_list` / `source_add`
    - `studio_create` / `studio_status`
    - `artifact_download` / `artifact_export`
    - `research_start` / `research_poll` / `research_import`（deepresearch のみ）
    - `refresh_auth`

### 検証（必須）

- 付与後、各 NotebookLM スキルについて本文を `grep -oE 'mcp__notebooklm-mcp__[a-z_]+'` で抽出し、**抽出された全ツールが allowed-tools に含まれること**を照合する（ワイルドカード採用時はワイルドカードがカバーすることを確認）。
- 各スキル本文で使う非 MCP ツール（Read/Bash/AskUserQuestion、go:check は Task 等）が allowed-tools に含まれること。
- 既存のフラグ廃止作業と同様、`npm run format` 実行後に `npm run format:check` が通ること。

---

## バージョン bump

いずれも修正/ドキュメント更新の範囲のため **PATCH**。plugin.json と marketplace.json の両方を一致させて更新する。

| プラグイン     | 現行  | 新    | 理由                                                      |
| -------------- | ----- | ----- | --------------------------------------------------------- |
| shiiman-google | 3.4.1 | 3.4.2 | gmail×2・notebooklm×4 の description / allowed-tools 修正 |
| shiiman-slack  | 4.1.1 | 4.1.2 | unread×2 の description 修正                              |
| shiiman-github | 4.3.0 | 4.3.1 | pr-list / issue-list / setup の description 微修正        |
| shiiman-go     | 3.1.0 | 3.1.1 | mod-update description・check の allowed-tools 補完       |

- root README.md / CLAUDE.md はプラグイン横断ドキュメントのためバージョン対象外。

## 成功基準

- A: root README.md に旧ワークフロースキル名が残らず、現行 4 スキルが正しく記載される。
- B: Gmail/Slack の未読/既読、および setup/mod-update・pr-list/issue-list のトリガーがドメイン固有化され、ドメイン非明示の汎用衝突フレーズが解消される。
- C: 5 スキルに allowed-tools が付与され、本文で使う全ツール（MCP 含む）を漏れなくカバーする（grep 照合で確認）。
- `npm run format:check` が通る。plugin.json と marketplace.json のバージョンが一致する。
- 変更は CLAUDE.md のルール（Conventional Commits 日本語・`--no-verify` 禁止・コミットはユーザー明示依頼時のみ）に従う。

## 留意事項 / リスク

- C の NotebookLM allowed-tools は取りこぼすと機能破壊につながるため、grep 照合検証を必ず実施する。ワイルドカード可否が不明な場合は安全側（全列挙）に倒す。
- B の文言は自然さと一意性のバランスを取る。過剰な冗長化を避けつつ、ドメイン非明示の汎用語だけは確実に除去する。
- 実装は A → C → B の順を推奨（A/C は機械的で低リスク、B は文言調整で見直しが入りやすいため最後に）。
