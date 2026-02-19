---
name: skill-create
description: プラグインに新しいスキルを作成する。「スキル作成」「新しいスキル」「スキルを作って」「スキル追加」「skill 作成」「スキルを追加したい」「新規スキル」などで起動。自然言語トリガーで起動するスキルを生成。
allowed-tools: [Read, Write, Bash, Glob]
argument-hint: "[--help]"
---

# Create Skill

プラグインに新しいスキルを作成します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/skill-create - Create Skill

概要:
  プラグインに新しいスキルを作成します。

使用方法:
  /skill-create [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. 情報収集

ユーザーに以下を聞く:

1. **対象プラグイン** - どのプラグインにスキルを追加するか
   - `plugins/` ディレクトリから既存プラグインを一覧表示

2. **スキル名**（小文字、ハイフン可、最大 64 文字）
   - 例: `review-code`, `create-test`

3. **説明**（トリガーフレーズを 7 つ含む、最大 1024 文字）
   - 形式: `{機能説明}。「トリガー1」「トリガー2」...「トリガー7」でトリガー。{詳細説明}。`
   - 例: `コードをレビュー。「レビューして」「コードチェック」...でトリガー。`

4. **許可するツール**（オプション）
   - 例: Read, Write, Bash, Glob, Grep, Edit

5. **このスキルで何をする？**（詳細な指示）

### 2. 検証

- スキル名の形式をチェック（小文字、ハイフン、数字のみ）
- プラグインが存在するか確認
- スキルが既に存在しないか確認
- description にトリガーフレーズが 7 つ含まれているか確認
- frontmatter に `argument-hint: "[--help]"` があることを確認
- 本文に `## Help` セクションがあり、`$ARGUMENTS` の `--help` 分岐を記載していることを確認

### description の書き方（重要）

**必須要件**:

1. **三人称で記述**: システムプロンプトに注入されるため
2. **7 つのトリガーワード**: ユーザーが使う可能性のある表現を網羅
3. **最大 1024 文字**: 簡潔に

**トリガーワードの選び方**:

- フォーマル: 「〜を実行してください」「〜を作成して」
- カジュアル: 「〜やって」「〜して」
- 具体的: 「PR を作って」「エラーを直して」
- 疑問形: 「〜できる？」「〜は？」

### 3. スキルディレクトリとファイルを作成

`plugins/{plugin-name}/skills/{skill-name}/SKILL.md` を作成:

````markdown
---
name: {plugin-name}:{skill-name}
description: { トリガーフレーズを7つ含む説明 }
allowed-tools: [{ ツール }]
argument-hint: "[--help]"
---

# {スキル名}

{説明}

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/{skill-name} - {スキル名}

概要:
  {1行要約}

使用方法:
  /{skill-name} [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. {ステップ1}

{詳細}

### 2. {ステップ2}

{詳細}

## 重要な注意事項

- ✅ 推奨する動作
- ❌ 禁止する動作
````

### 3.1 scripts パス規約を適用

scripts を使う Skill の場合は、以下の規約を適用する:

- 標準配置: `plugins/{plugin-name}/skills/{skill-name}/scripts/{script-file}`
- 標準参照: `${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/scripts/{script-file}`
- 共通処理のみ配置: `plugins/{plugin-name}/scripts/{script-file}`
- 共通参照: `${CLAUDE_PLUGIN_ROOT}/scripts/{script-file}`
- 共通化基準（運用）: 2 つ以上の `SKILL.md` から参照される script は plugin ルートへ配置

### 4. プラグイン README を更新

`plugins/{plugin-name}/README.md` のスキルセクションにスキルを追加。

### 5. 報告

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

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ description に 7 つのトリガーワードを含める
- ✅ 独自実装パターンで完全な手順を記載
- ✅ scripts は原則 `skills/{skill}/scripts/`、共通処理のみ `scripts/` を使用
- ✅ すべての Skill に `argument-hint: "[--help]"` と `## Help` セクションを必ず含める
- ❌ トリガーワードが不足している description は避ける
