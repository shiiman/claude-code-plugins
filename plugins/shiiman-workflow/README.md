# shiiman-workflow

開発ワークフロー自動化プラグイン

## 概要

シングルエージェント/マルチエージェントでの開発フローを提供します。
Issue 管理付き・なしの両方のパターンに対応。

## インストール

```bash
/shiiman-plugin:install shiiman-workflow
```

## 機能比較

| スキル | Issue | ブランチ | PR | エージェント | 用途 |
|--------|-------|----------|-----|--------------|------|
| single-issue-flow | ✅ | ✅ | ✅ | シングル | 標準的な開発フロー |
| single-flow | ❌ | ✅ | ❌ | シングル | 軽量な実装タスク |
| multi-issue-flow | ✅ | ✅ | ✅ | マルチ | 大規模な開発タスク |
| multi-flow | ❌ | ✅ | ❌ | マルチ | 並列実装タスク |
| agent-team-issue-flow | ✅ | ✅ | ✅ | Agent Team | Agent Team で Issue から PR まで |
| agent-team-flow | ❌ | ✅ | ❌ | Agent Team | Agent Team 軽量並列実装 |

## スキル

### single-issue-flow

Issue から PR まで自動実行するシングルエージェントフロー。

**トリガー例**: 「シングル Issue フロー」「Issue から PR まで」「single-issue-flow」

**フロー**:

```
計画書 → Issue → ブランチ → 実装 → レビュー → コミット → PR
```

**実行モード**:

- 引数なし: 既存の計画書から実行
- `--plan`: 計画書を作成してから実行
- `タスク説明`: 計画書なしで直接実行

### single-flow

Issue/PR なしで軽量に実行するフロー。

**トリガー例**: 「シングルフロー」「軽量フロー」「single-flow」

**フロー**:

```
計画書 → ブランチ → 実装 → レビュー → コミットメッセージ出力
```

**特徴**:

- Issue を作成しない
- ブランチを作成する（feature/{slug} 形式）
- PR を作成しない
- コミットメッセージを出力して終了（手動でコミット）

### multi-issue-flow

MCP マルチエージェントで並列実行する開発フロー。

**トリガー例**: 「マルチ Issue フロー」「並列 Issue 開発」「multi-issue-flow」

**前提条件**:

- multi-agent-mcp インストール済み
- tmux インストール済み

**フロー**:

```
計画書 → Issue → MCP初期化 → 並列実行 → 統合 → レビュー → コミット → PR
```

**階層**:

- Owner（呼び出し元）: 全体を統括
- Admin（1）: タスク分配と Worker 管理
- Worker（max 16）: 各サブタスクを並列実行

### multi-flow

MCP マルチエージェントで並列実行する軽量フロー。

**トリガー例**: 「マルチフロー」「並列フロー」「multi-flow」

**前提条件**:

- multi-agent-mcp インストール済み
- tmux インストール済み

**フロー**:

```
計画書 → ブランチ → MCP初期化 → 並列実行 → 統合 → レビュー → コミットメッセージ出力
```

**特徴**:

- Issue を作成しない
- ブランチを作成する（feature/{slug} 形式）
- PR を作成しない
- 複数 Worker が並列実行
- 統合後にコミットメッセージを出力

### agent-team-issue-flow

Agent Team で Issue から PR まで並列実行する開発フロー。

**トリガー例**: 「agent-team-issue-flow」「エージェントチーム Issue フロー」「Agent Team Issue」

**フロー**:

```text
計画書 → Issue → ブランチ → Ghostty/iTerm2 + tmux 起動 → Agent Team 実装 → レビュー → コミット → PR
```

**特徴**:

- `multi-issue-flow` の MCP 使用部分を Agent Team 実行に置き換え
- `claude --dangerously-skip-permissions` で Agent Team 実行
- Ghostty 優先、未導入時は iTerm2 で tmux セッションを起動
- 2 つの Agent Team スキルで共通利用する送信スクリプトは `plugins/shiiman-workflow/scripts/send_claude_tmux_message.sh` を使用

### agent-team-flow

Agent Team で Issue/PR なしに並列実行する軽量フロー。

**トリガー例**: 「agent-team-flow」「エージェントチームフロー」「Agent Team で実装」

**フロー**:

```text
計画書 → ブランチ → Ghostty/iTerm2 + tmux 起動 → Agent Team 実装 → レビュー → コミットメッセージ出力
```

**特徴**:

- `multi-flow` の MCP 使用部分を Agent Team 実行に置き換え
- `claude --dangerously-skip-permissions` で Agent Team 実行
- 問題時は Agent Team に再指示してループ可能
- 2 つの Agent Team スキルで共通利用する送信スクリプトは `plugins/shiiman-workflow/scripts/send_claude_tmux_message.sh` を使用

## 必要条件

### 全スキル共通

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

### マルチエージェントスキル（multi-*）

- multi-agent-mcp がインストール済み
- tmux がインストール済み

### Agent Team スキル（agent-team-*）

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` を有効化
- `CLAUDE_PLUGIN_ROOT` が利用可能なプラグイン実行コンテキストで実行
- `claude` コマンドが利用可能
- tmux がインストール済み
- macOS で Ghostty または iTerm2 が利用可能

## バージョン履歴

- v1.7.1: agent-team-flow / agent-team-issue-flow を仕様準拠に修正（Ghostty/iTerm2 + tmux + Agent Team 実行フローへ統一）
- v1.5.0: SKILL.md を約 60% スリム化。MCP 側で Admin/Worker 指示を自動生成
- v1.4.0: Worker 数をデフォルト 6、最大 16 に変更。MCP 自動機能（ペルソナ、メモリ、7セクション構造）を統合
- v1.0.0: 初期リリース（shiiman-git の dev-flow から移行）
