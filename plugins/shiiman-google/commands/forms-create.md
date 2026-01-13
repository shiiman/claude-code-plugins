---
name: forms-create
description: Google Forms フォームを新規作成する
allowed-tools: [Bash]
---

# Forms Create

Google Forms フォームを新規作成します。

## 引数

- `$ARGUMENTS` (必須): フォーム名

## オプション

- `--description <text>`: フォームの説明

## 実行

```bash
python plugins/shiiman-google/skills/forms-list/scripts/google_forms.py create --name "$ARGUMENTS" ${DESCRIPTION:+--description "$DESCRIPTION"}
```

## 使用例

```
/shiiman-google:forms-create アンケート
/shiiman-google:forms-create 満足度調査 --description "サービス改善のためのアンケートです"
```
