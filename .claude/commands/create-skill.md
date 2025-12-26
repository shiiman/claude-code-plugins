# Create Skill

プラグインに新しいスキルを作成します。

## 使い方

```bash
/create-skill
```

## Claude への指示

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにスキルを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **スキル名**（小文字、ハイフン可）
   - 例: `code-reviewer`, `test-generator`

3. **説明**（トリガーフレーズを含む）
   - 例: 「コードをレビュー。『コードレビュー』『コードをチェック』でトリガー」

4. **許可するツール**（オプション）
   - 例: Read, Write, Bash, Glob, Grep

5. **このスキルで何をする？**（詳細な指示）

### ステップ 2: 検証

- スキル名の形式をチェック
- プラグインが存在するか確認
- スキルが既に存在しないか確認

### ステップ 3: スキルディレクトリとファイルを作成

`plugins/{plugin-name}/skills/{skill-name}/SKILL.md` を作成:

```markdown
---
name: {skill-name}
description: {トリガーフレーズを含む説明}
allowed-tools: [{ツール}]
---

# {スキル名}

{説明}

## 手順

{ユーザーからの詳細な指示}
```

### ステップ 4: プラグイン README を更新

`plugins/{plugin-name}/README.md` のスキルセクションにスキルを追加。

### ステップ 5: 報告

作成されたファイルと次のステップを表示:

```text
スキルを作成しました: {skill-name}

ファイル:
- plugins/{plugin-name}/skills/{skill-name}/SKILL.md

更新:
- plugins/{plugin-name}/README.md

トリガー: {説明からのトリガーフレーズ}

次のステップ:
- /create-skill で別のスキルを追加
- /create-command でコマンドを追加
- /create-subagent でサブエージェントを追加
- /create-hook でフックを追加
```
