---
name: skill-creator
description: プロジェクトの .claude/skills/ に新しいスキルを作成する。「スキル作成」「新しいスキル」「スキルを作って」「スキル追加」「skill 作成」「スキルを追加したい」「新規スキル」などで起動。プロジェクト固有のスキルファイルを生成。
allowed-tools: [Read, Write, Bash, Glob]
---

# Skill Creator

プロジェクトの `.claude/skills/` に新しいスキルを作成します。

## ワークフロー

### 1. コマンド実行

`/shiiman-claude:create-skill` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-claude:create-skill` に委譲します（SSOT として扱う）。

`/shiiman-claude:create-skill` コマンドは以下を行う:

- スキル名と説明を聞く（トリガーフレーズ 7 つ含む）
- 許可ツールを聞く
- スキルファイルを作成

## description の書き方（重要）

**必須要件**:

1. **三人称で記述**: システムプロンプトに注入されるため
2. **7 つのトリガーワード**: ユーザーが使う可能性のある表現を網羅
3. **最大 1024 文字**: 簡潔に

## 重要な注意事項

- ✅ 小文字・ハイフン区切りを使用
- ✅ description に 7 つのトリガーフレーズを含める
- ✅ `.claude/skills/{name}/SKILL.md` に作成
- ❌ アンダースコアやキャメルケースは使用しない
