---
name: create-command
description: プロジェクトの .claude/commands/ に新しいスラッシュコマンドを作成する。「コマンド作成」「新しいコマンド」「コマンドを作って」「コマンド追加」「command 作成」「コマンドを追加したい」「新規コマンド」などで起動。プロジェクト固有のコマンドファイルを生成。
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
---

# Create Command

プロジェクトの `.claude/commands/` に新しいスラッシュコマンドを作成します。

## 引数

- `$ARGUMENTS`: `--help` でヘルプを表示

## 実行手順

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 情報収集

ユーザーに以下を聞く:

1. **コマンド名**（小文字、ハイフン可）
   - 例: `lint`, `format-code`

2. **説明**（1 文）

3. **このコマンドで何をする？**（詳細な指示）

### ステップ 2: 検証

- コマンド名の形式をチェック（小文字、ハイフンのみ）
- `.claude/commands/` ディレクトリが存在するか確認（なければ作成）
- コマンドが既に存在しないか確認

### 命名規則

| パターン       | 例                        | 説明                           |
|----------------|---------------------------|--------------------------------|
| リソース操作系 | `pr-create`, `hook-new`   | リソースが先、アクションが後   |
| アクション系   | `check-fact`, `fix-error` | アクションが先、ターゲットが後 |
| 単一語         | `review`, `commit`        | 確立された技術用語             |

### ステップ 3: コマンドファイルを作成

`.claude/commands/{command-name}.md` を作成。

**テンプレート構造**:

```markdown
# {コマンド名}

{説明}

## 使い方

/{command-name}
/{command-name} --help

## オプション

| オプション | 説明                       |
|------------|----------------------------|
| `--help`   | このコマンドのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

{ユーザーからの詳細な指示}
```

### ステップ 4: 報告

作成されたファイルと次のステップを表示:

```text
コマンドを作成しました: /{command-name}

ファイル:
- .claude/commands/{command-name}.md

次のステップ:
- /shiiman-claude:create-command で別のコマンドを追加
- /shiiman-claude:create-skill でスキルを追加
- /shiiman-claude:create-subagent でサブエージェントを追加
- /shiiman-claude:create-hook でフックを追加
```

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ --help オプションを必ず含める
- ✅ `.claude/commands/` に作成
- ❌ アンダースコアやキャメルケースは使用しない
