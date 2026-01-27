---
name: report
description: プラグインに関する要望、改善提案、バグ報告を作成する。「バグを報告」「要望を送りたい」「改善提案」「Issue を報告」「フィードバック」「機能リクエスト」「不具合報告」「プラグインの要望」「改善してほしい」「バグがある」「問題を報告」などで起動。
allowed-tools: [Read, Bash, Glob, Grep]
---

# Plugin Report

プラグインに関する要望、改善提案、バグ報告を shiiman/claude-code-plugins リポジトリに Issue として投稿します。

## オプション

| オプション | 説明                     |
|------------|--------------------------|
| `--help`   | このスキルのヘルプを表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. Issue の種類を確認

ユーザーに Issue の種類を選択してもらう:

| 種類                   | ラベル        | 説明                       |
|------------------------|---------------|----------------------------|
| 要望 (Feature Request) | `enhancement` | 新しい機能の追加リクエスト |
| 改善 (Improvement)     | `improvement` | 既存機能の改善提案         |
| バグ (Bug)             | `bug`         | 不具合の報告               |

質問例:
「どの種類の Issue を作成しますか？
1. 要望（新機能の追加）
2. 改善（既存機能の改善）
3. バグ（不具合の報告）」

2. Issue のタイトルを確認

「Issue のタイトルを入力してください（簡潔に）」

3. Issue の詳細を確認

**要望/改善の場合**:
- 概要: 何を実現したいか / 何を改善したいか
- 背景: なぜこの機能/改善が必要か
- 期待動作: どのような動作を期待するか

**バグの場合**:
- 概要: どのような問題が発生したか
- 再現手順: どうすれば再現できるか
- 期待動作: 本来どうあるべきか
- 実際の動作: 現在どうなっているか
- 環境情報: OS、Claude Code バージョン等（可能であれば）

4. 確認と送信

Issue 内容をプレビュー表示してユーザーに確認を求める。承認後、以下のコマンドで Issue を作成:

```bash
gh issue create \
  --repo shiiman/claude-code-plugins \
  --title "{title}" \
  --body "{body}" \
  --label "{label}"
```

5. 結果報告

作成した Issue の URL を表示:

```
✅ Issue を作成しました

#{number}: {title}
URL: https://github.com/shiiman/claude-code-plugins/issues/{number}

ご報告ありがとうございます！
```

### Issue 本文テンプレート

#### 要望 (Feature Request)

```markdown
## 概要

{概要}

## 背景

{背景}

## 期待動作

{期待動作}

---
📝 この Issue は `shiiman-plugin:report` スキルで作成されました
```

#### 改善 (Improvement)

```markdown
## 概要

{概要}

## 背景

{背景}

## 改善案

{期待動作/改善案}

---
📝 この Issue は `shiiman-plugin:report` スキルで作成されました
```

#### バグ (Bug)

```markdown
## 概要

{概要}

## 再現手順

1. {手順1}
2. {手順2}
3. ...

## 期待動作

{期待動作}

## 実際の動作

{実際の動作}

## 環境情報

- OS: {OS}
- Claude Code バージョン: {バージョン}

---
📝 この Issue は `shiiman-plugin:report` スキルで作成されました
```

### 重要な注意事項

- ✅ 報告先は `shiiman/claude-code-plugins` に固定
- ✅ ラベルは種類に応じて自動設定（enhancement / improvement / bug）
- ✅ 送信前に必ずユーザーに内容確認を求める
- ✅ 作成後は Issue URL を表示
- ❌ 個人情報や機密情報を含めない
- ❌ ユーザーの同意なしに Issue を作成しない
