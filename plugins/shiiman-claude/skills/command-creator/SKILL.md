---
name: command-creator
description: プロジェクトの .claude/commands/ に新しいスラッシュコマンドを作成する。「コマンド作成」「新しいコマンド」「コマンドを作って」「コマンド追加」「command 作成」「コマンドを追加したい」「新規コマンド」などで起動。プロジェクト固有のコマンドファイルを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Command Creator

プロジェクトの `.claude/commands/` に新しいスラッシュコマンドを作成します。

## ワークフロー

### 1. コマンド実行

`/shiiman-claude:create-command` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-claude:create-command` に委譲します（SSOT として扱う）。

`/shiiman-claude:create-command` コマンドは以下を行う:

- コマンド名と説明を聞く
- コマンドファイルを作成（--help オプション含む）

## 命名規則

| パターン       | 例                        | 説明                           |
|----------------|---------------------------|--------------------------------|
| リソース操作系 | `pr-create`, `hook-new`   | リソースが先、アクションが後   |
| アクション系   | `check-fact`, `fix-error` | アクションが先、ターゲットが後 |
| 単一語         | `review`, `commit`        | 確立された技術用語             |

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ --help オプションを必ず含める
- ✅ `.claude/commands/` に作成
- ❌ アンダースコアやキャメルケースは使用しない
