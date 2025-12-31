---
name: issue-creator
description: 計画から GitHub Issue を作成する。「Issue 作成」「Issue を作って」「Issue 作成して」「計画から Issue」「Issue 追加」「Issue を追加したい」「Issue 作りたい」などで起動。1つの計画を1つの Issue にまとめて作成。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Issue Creator

計画から GitHub Issue を作成します。1つの計画は1つの Issue にまとめます。

## ワークフロー

### 1. 計画の確認

ユーザーに計画を確認。計画ファイルがある場合は Read ツールで参照。

### 2. Issue 内容の整理

計画から以下の情報を抽出：

- プラグイン名
- 説明（概要）
- 含まれるコマンド一覧
- 含まれるスキル一覧
- 含まれるサブエージェント一覧
- 含まれるフック一覧
- 各タスクの完了状態

### 3. ラベルの決定

計画に含まれる要素すべてにラベルを付与：

| 要素 | ラベル |
|------|--------|
| 基本 | `enhancement` |
| プラグイン | `plugin` |
| コマンド | `command` |
| スキル | `skill` |
| サブエージェント | `subagent` |
| フック | `hook` |

**例**: プラグイン + コマンド + スキルを含む場合
→ `enhancement,plugin,command,skill`

### 4. Issue 作成

`gh issue create` コマンドで **1つの Issue** を作成。

**コマンドテンプレート**:

```bash
gh issue create \
  --title "[Plugin] shiiman-{plugin-name}" \
  --body "## 概要
{description}

## プラグイン名
shiiman-{plugin-name}

## コマンド
| 状態 | コマンド | 説明 |
|:----:|----------|------|
| ✅ | {command1} | {description1} |
|    | {command2} | {description2} |

## スキル
| 状態 | スキル | 説明 | 実装パターン |
|:----:|--------|------|--------------|
| ✅ | {skill1} | {description1} | SSOT |
|    | {skill2} | {description2} | 独自実装 |

## サブエージェント
（なし）

## フック
（なし）
" \
  --label "enhancement,plugin,command,skill"
```

**状態の表現**:

- `✅` - 実装済み（計画の status が completed）
- 空欄 - 未実装（計画の status が pending/in_progress）

**セクションの省略**:

- コマンドがない場合: 「## コマンド」セクションを省略
- スキルがない場合: 「## スキル」セクションを省略
- サブエージェントがない場合: 「## サブエージェント」を「（なし）」
- フックがない場合: 「## フック」を「（なし）」

### 5. 結果報告

作成された Issue の番号と URL を報告。

### 6. コミットコメントの提案

Issue 作成後、以下のフォーマットでコミットコメントを表示：

```
推奨コミットコメント:
feat: {変更内容の要約} (#Issue番号)
```

**例**:

```
推奨コミットコメント:
feat: shiiman-claude プラグインに設定スキルを追加 (#17)
```

### 7. PR 作成の促し

Issue 作成後、ユーザーに PR 作成を促す：

```
Issue を作成しました。PR を作成しますか？
「PR 作成」または「PR を作って」と言ってください。
```

## 重要な注意事項

- ✅ 1つの計画は1つの Issue にまとめる
- ✅ 含まれる要素すべてのラベルを付与
- ✅ タスクの完了状態を表の先頭列に ✅ または空欄で表現
- ✅ 計画の全体像が分かるように構造化して記載
- ❌ 計画を複数の Issue に分割しない
- ❌ 計画にない内容を含めない
