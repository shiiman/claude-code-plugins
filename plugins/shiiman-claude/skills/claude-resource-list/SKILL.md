---
name: claude-resource-list
description: プロジェクトの Claude Code リソース一覧を表示する。「Claude リソース一覧」「スキル一覧」「エージェント一覧」「フック一覧」「プロジェクトリソース確認」「何があるか確認」「リソースを見せて」などで起動。
allowed-tools: [Read, Glob]
argument-hint: "[--skills|--agents|--hooks|--help]"
---

# Claude Resource List

プロジェクトの Claude Code リソース一覧を表示します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/claude-resource-list - Claude リソース一覧

概要:
  プロジェクトの Claude Code リソース（スキル・エージェント・フック）を一覧表示する。

使用方法:
  /claude-resource-list [オプション]

オプション:
  --skills  スキルのみ表示
  --agents  エージェントのみ表示
  --hooks   フックのみ表示
  --help    このヘルプを表示

例:
  /claude-resource-list              # すべてのリソースを表示
  /claude-resource-list --skills     # スキルのみ表示
  /claude-resource-list --agents     # エージェントのみ表示
```

## 実行手順

### 1. 表示対象を決定

- 引数が指定されていれば引数を優先
- 引数がない場合は発話内容から `skills` / `agents` / `hooks` / `all` を判定

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
|--------|------|

### エージェント (N)
| エージェント | 説明 |
|--------------|------|

### フック (N)
| イベント | 件数 |
|----------|------|
```

## 重要な注意事項

- ✅ 存在しないディレクトリやファイルはスキップ
- ✅ リソースが0件のときは「なし」と明示
- ✅ hooks はサマリ表示とする
- ❌ 詳細編集は行わない（一覧のみ）
