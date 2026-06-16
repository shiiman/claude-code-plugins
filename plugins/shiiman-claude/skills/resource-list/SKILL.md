---
name: shiiman-claude:resource-list
description: プロジェクトの Claude Code リソース一覧を表示する。「Claude リソース一覧」「スキル一覧」「エージェント一覧」「フック一覧」「プロジェクトリソース確認」「何があるか確認」「リソースを見せて」などで起動。表示対象（スキル/エージェント/フック）は発話から判断する。
allowed-tools: [Read, Glob]
argument-hint: "[--help]"
---

# Claude Resource List

プロジェクトの Claude Code リソース一覧を表示します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-claude:resource-list - Claude リソース一覧

概要:
  プロジェクトの Claude Code リソース（スキル・エージェント・フック）を一覧表示する。

使用方法:
  /shiiman-claude:resource-list

オプション:
  --help  このヘルプを表示

表示対象の伝え方（フラグの代わり）:
  「スキル」「スキル一覧」      → スキルのみ表示
  「エージェント」「agent」     → エージェントのみ表示
  「フック」「hook」            → フックのみ表示
  指定なし                     → すべて表示

例:
  /shiiman-claude:resource-list   # すべてのリソースを表示
  「スキル一覧を見せて」           # スキルのみ表示
  「エージェント一覧」             # エージェントのみ表示
```

## 実行手順

### 1. 表示対象を決定（フラグの代わり）

発話内容から `skills` / `agents` / `hooks` / `all` を判定する。明示がなければ `all`（すべて表示）とする。読み取り専用のため確認は不要。

### 2. リソースを収集

- **スキル**: `.claude/skills/` 配下の `SKILL.md` を持つディレクトリ
- **エージェント**: `.claude/agents/` 配下の `.md` ファイル
- **フック**: `.claude/settings.json` と `.claude/settings.local.json` の `hooks` セクション

### 3. 一覧を整形して表示

- スキル: 名前と説明
- エージェント: 名前と説明
- フック: イベント別の件数サマリ

## 出力フォーマット

```markdown
## Claude リソース一覧

### スキル (N)

| スキル | 説明 |
| ------ | ---- |

### エージェント (N)

| エージェント | 説明 |
| ------------ | ---- |

### フック (N)

| イベント | 件数 |
| -------- | ---- |
```

## 重要な注意事項

- ✅ 存在しないディレクトリやファイルはスキップ
- ✅ リソースが0件のときは「なし」と明示
- ✅ hooks はサマリ表示とする
- ❌ 詳細編集は行わない（一覧のみ）
