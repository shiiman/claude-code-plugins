# コマンド作成ガイド

このガイドでは、Claude Code プラグイン用のコマンドを作成する方法を説明します。

## 概要

コマンドは Markdown ファイル (`.md`) として定義され、`plugins/{plugin-name}/commands/` ディレクトリに配置されます。

**Skills との使い分け**: 複雑なワークフロー、複数の関連ファイル（テンプレート、参照資料など）を含むリソースが必要な場合は、コマンドではなく Skills の利用を検討してください。詳細は [Skill 作成ガイド](skill.md) を参照してください。

## 配置場所

```text
plugins/{plugin-name}/commands/{command-name}.md
```

## コマンドファイルの構造

### 基本テンプレート

```markdown
# コマンド名

このコマンドの説明。

## 使い方

/{command-name}
/{command-name} --help

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

このコマンドが呼び出されたときに Claude が実行する手順。
```

### ポイント

- 最初の `#` 見出しがコマンド名として表示される
- 簡潔に（200-500 文字程度）
- 具体的な使用例を含める
- コードブロックを活用

## --help オプション

すべてのコマンドには `--help` オプションを含めてください。

- **使い方セクション**: `/{command-name} --help` を記載
- **オプションセクション**: `--help` オプションをテーブルに追加
- **Claude への指示**: `--help` 時の動作（ファイル内容を要約して表示）を記載

## 命名規則

### 基本ルール

- 小文字とハイフンを使用: `my-command.md`
- コマンド名はファイル名から（`.md` を除く）
- **プラグイン名をプレフィックスに含めない**: `list.md` ✅ / `plugin-list.md` ❌

### ファイル名の注意点

コマンドファイル名にプラグイン名やリソース名のプレフィックスは不要です。プラグイン名は呼び出し時に自動的に付与されます。

```bash
# ✅ 良い例
plugins/shiiman-plugin/commands/list.md      # → /shiiman-plugin:list
plugins/shiiman-plugin/commands/show.md      # → /shiiman-plugin:show
plugins/shiiman-plugin/commands/install.md   # → /shiiman-plugin:install

# ❌ 悪い例（冗長）
plugins/shiiman-plugin/commands/plugin-list.md
plugins/shiiman-plugin/commands/plugin-show.md
```

### コマンド特有のパターン

コマンドでは以下のパターンが一般的です：

#### 1. リソース操作系: `{resource}-{action}`

リソースに対する操作を表現する場合。

```bash
component-new         # コンポーネント作成
hook-new              # フック作成
pr-create             # PR 作成
pr-review             # PR レビュー
```

**特徴**:

- リソース（component/hook/pr）が先、アクションが後
- 同じリソースに対する操作が並んで整理される

#### 2. アクション系: `{action}-{target}`

アクションが主で、ターゲットが補足的な場合。

```bash
check-fact            # 事実をチェック
check-prompt          # プロンプトをチェック
explain-code          # コードを説明
fix-error             # エラーを修正
analyze-dependencies  # 依存関係を分析
```

**特徴**:

- アクション（check/explain/analyze）が先、ターゲットが後
- 同じアクションを複数のターゲットに適用

#### 3. 単一語: 確立された技術用語

追加の修飾が不要な場合は単一語を使用。

```bash
review                # レビュー
refactor              # リファクタリング
plan                  # 計画作成
commit                # コミット
```

**特徴**:

- 業界標準用語
- 短く覚えやすい
- 説明不要の明確さ

**重要**: 同じリソースに対するコマンドは命名パターンを統一してください（例: `pr-create`, `pr-review`, `pr-fix`）。

## コマンド呼び出し形式

### プラグイン付き

```bash
/shiiman-common:commit
/shiiman-react:component-new
```

### グローバルコマンド

common プラグインの場合のみ、プラグイン名を省略可能：

```bash
/review
/refactor
/commit
```

## 実装ガイドライン

### 1. 簡潔な説明

```markdown
# ✅ 良い例

## Component New

新しい React コンポーネントをベストプラクティスに従って作成します。

# ❌ 悪い例

## Component New

このコマンドは React コンポーネントを作成するためのものです。
様々な機能があります。便利です。
```

### 2. 具体的な使用例

````markdown
# ✅ 良い例

```bash
# 関数コンポーネントを作成
/react:component-new Button

# TypeScript + Storybook 対応
/react:component-new Card --typescript --storybook
```

# ❌ 悪い例

```bash
# コンポーネント作成
/react:component-new
```
````

### 3. オプションの明記

```markdown
# ✅ 良い例

### オプション

| オプション    | 説明                         |
|---------------|------------------------------|
| `--help`      | このコマンドのヘルプを表示   |
| `--typescript`| TypeScript で生成            |
| `--test`      | テストファイルも生成         |
| `--storybook` | Storybook ストーリーも生成   |

# ❌ 悪い例

### オプション

いくつかオプションがあります。
```

## ベストプラクティス

### 単一責任の原則

```bash
# ✅ 良い設計
component-new      # コンポーネント作成のみ
component-test     # テスト生成のみ

# ❌ 悪い設計
component-all      # 作成・テスト・ドキュメントすべて
```

### ユーザーフレンドリー

```bash
# ✅ 良い命名
hook-new           # 明確
component-generate # 明確

# ❌ 悪い命名
hk-n               # 省略しすぎ
create-component-with-test-and-storybook  # 長すぎ
```

### 一貫性

```bash
# ✅ プラグイン内で統一
component-new
hook-new
context-new

# ❌ 不統一
component-new
create-hook
generateContext
```

## 実装例

ファイル: `plugins/shiiman-common/commands/hello.md`

```markdown
# Hello

ユーザーに挨拶します。

## 使い方

/hello [名前]
/hello --help

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

1. 名前が指定されていれば「こんにちは、{名前}さん！」と挨拶
2. そうでなければ「こんにちは！」と挨拶
```

## コマンド名の例

### 技術スタック別

**React**:

- `component-new`
- `hook-new`
- `context-new`
- `test-component`

**Go**:

- `struct-new`
- `interface-generate`
- `test-generate`

### 共通機能

- `code-review`
- `refactor`
- `explain-code`
- `fix-error`
- `commit`
- `pr-create`

## トラブルシューティング

### コマンド名が既に存在する

```bash
# エラー: Command 'hook-new' already exists in plugin 'shiiman-react'

# 解決策
ls plugins/shiiman-react/commands/  # 既存コマンドを確認
# 別の名前を検討（例: hook-create, custom-hook-new）
```

### 命名規則違反

```bash
# エラー: Invalid command name 'HookNew'

# 解決策
# 小文字・ハイフン区切りに修正
hook-new  # ✅
```

## 参考資料

公式ドキュメント:

- [Claude Code Plugins 公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
