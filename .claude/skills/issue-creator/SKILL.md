---
name: issue-creator
description: 計画から複数の GitHub Issue をまとめて作成する。「Issue 作成」「Issue を作って」「Issue 作成して」「計画から Issue」「Issue 追加」「Issue を追加したい」「まとめて Issue」などで起動。計画を Issue に分解して一括作成。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Issue Creator

計画から複数の GitHub Issue をまとめて作成します。

## ワークフロー

### 1. 計画の確認

ユーザーに計画を確認。計画ファイルがある場合は Read ツールで参照。

### 2. Issue 一覧の抽出

計画から作成すべき Issue を特定：

- プラグイン作成
- コマンド追加
- スキル追加
- サブエージェント追加
- フック追加

**例**: 計画が「プラグインとコマンド 1 つ」のみの場合、2 つだけ作成。

### 3. Issue 作成

`gh issue create` コマンドで計画に含まれる Issue のみを作成。

**Issue タイプと対応するラベル**:

| タイプ           | タイトルプレフィックス | ラベル                |
|------------------|------------------------|-----------------------|
| プラグイン       | `[Plugin]`             | enhancement, plugin   |
| コマンド         | `[Command]`            | enhancement, command  |
| スキル           | `[Skill]`              | enhancement, skill    |
| サブエージェント | `[Subagent]`           | enhancement, subagent |
| フック           | `[Hook]`               | enhancement, hook     |

**コマンドリファレンス**（必要なものだけ使用）:

```bash
# プラグイン作成
gh issue create \
  --title "[Plugin] shiiman-{name}" \
  --body "## プラグイン名
{name}

## 説明
{description}" \
  --label "enhancement,plugin"

# コマンド追加
gh issue create \
  --title "[Command] shiiman-{plugin}:{command}" \
  --body "## 対象プラグイン
shiiman-{plugin}

## コマンド名
{command}

## 説明
{description}" \
  --label "enhancement,command"

# スキル追加
gh issue create \
  --title "[Skill] shiiman-{plugin}:{skill}" \
  --body "## 対象プラグイン
shiiman-{plugin}

## スキル名
{skill}

## 説明
{description}" \
  --label "enhancement,skill"

# サブエージェント追加
gh issue create \
  --title "[Subagent] shiiman-{plugin}:{subagent}" \
  --body "## 対象プラグイン
shiiman-{plugin}

## サブエージェント名
{subagent}

## 説明
{description}" \
  --label "enhancement,subagent"

# フック追加
gh issue create \
  --title "[Hook] shiiman-{plugin}:{event}:{matcher}" \
  --body "## 対象プラグイン
shiiman-{plugin}

## イベント
{event}

## マッチャー
{matcher}

## 説明
{description}" \
  --label "enhancement,hook"
```

### 4. 結果報告

作成された Issue の一覧（番号と URL）を報告。

## 重要な注意事項

- ✅ 計画に含まれる項目のみを Issue として作成
- ✅ 適切なラベルを付与
- ❌ 不要な Issue を含めない
- ❌ 計画にない Issue を作成しない
