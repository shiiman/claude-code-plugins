# スキル作成ガイド

## 概要

スキルは自然言語パターンに基づいて自動的にトリガーされます。

## 配置場所

```text
plugins/{plugin-name}/skills/{skill-name}/SKILL.md
```

## ファイル形式 (SKILL.md)

```markdown
---
name: skill-name
description: 「プラグイン作成」「新しいプラグイン」などのトリガーフレーズを含む説明
allowed-tools: [Read, Write, Bash]
---

# スキル名

このスキルの説明。

## 手順

このスキルがトリガーされたときに Claude が実行する手順。
```

## フロントマターフィールド

| フィールド | 必須 | 説明 |
|------------|------|------|
| name | はい | スキル識別子（小文字、ハイフン） |
| description | はい | トリガーフレーズを含む説明 |
| allowed-tools | いいえ | スキルが使用できるツール |

## 例

ファイル: `plugins/common/skills/plugin-creator/SKILL.md`

```markdown
---
name: plugin-creator
description: 新しいプラグインを作成。「プラグイン作成」「新しいプラグイン」などでトリガー。
allowed-tools: [Read, Write, Bash]
---

# Plugin Creator

必要な構造を持つ新しい Claude Code プラグインを作成します。

## 手順

1. プラグイン名を聞く
2. 説明を聞く
3. ディレクトリ構造を作成
4. plugin.json を生成
5. marketplace.json を更新
```
