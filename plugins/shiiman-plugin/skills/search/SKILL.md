---
name: search
description: キーワードでプラグインを検索する。「プラグインを検索」「〇〇ができるプラグイン」「〇〇関連のプラグイン」「〇〇を探して」「プラグイン探して」「〇〇のプラグインある？」などで起動。
---

# Plugin Search

キーワードでプラグインを検索します。

## ワークフロー

### 1. キーワードの取得

ユーザーの発話からキーワードを抽出します。

例:
- 「Git 関連のプラグインある？」→ キーワード: "git"
- 「Google 連携できるプラグインを探して」→ キーワード: "google"
- 「コミットのプラグイン」→ キーワード: "コミット", "commit"

キーワードが不明確な場合は、ユーザーに確認を求めます。

### 2. プラグイン情報の検索

以下の情報源からキーワードを検索します:

1. `.claude-plugin/marketplace.json` の `name` と `description`
2. 各プラグインの `README.md`（インストール済みの場合）

```bash
# marketplace.json を読み取り
cat .claude-plugin/marketplace.json

# 各プラグインの README を読み取り
cat plugins/{plugin-name}/README.md
```

### 3. マッチング

- 大文字小文字を区別しない
- 部分一致で検索
- name, description, README の内容すべてを検索対象とする

### 4. 結果の表示

マッチしたプラグインを一覧表示し、主な機能も紹介します。

## 出力フォーマット

### 検索結果がある場合

```
## プラグイン検索結果

検索キーワード: "git"

| プラグイン | 説明 | 状態 |
|-----------|------|------|
| shiiman-git | Git/GitHub ワークフロー管理 | ✅ インストール済み |

### shiiman-git の主な機能

- Issue/PR 管理
- ブランチ作成
- コミット支援
- dev-flow（統合開発フロー）

詳細は `/shiiman-plugin:show shiiman-git` で確認できます。
インストールは `/shiiman-plugin:install shiiman-git` で実行できます。
```

### 検索結果がない場合

```
## プラグイン検索結果

検索キーワード: "xxx"

該当するプラグインが見つかりませんでした。

利用可能なプラグイン一覧は `/shiiman-plugin:list` で確認できます。
```

## 重要な注意事項

- ✅ 大文字小文字を区別しない検索
- ✅ marketplace.json と README.md を検索
- ✅ インストール状態を表示
- ✅ マッチしたプラグインの主な機能を紹介
- ✅ 詳細確認やインストールのコマンドを案内
