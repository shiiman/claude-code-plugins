---
name: auth-setup
description: Google OAuth クライアント設定の手順を案内する。「OAuth 設定」「Google 認証の準備」「クライアント ID 作成」「認証手順を教えて」「Google ログイン準備」「OAuth セットアップ」「認証設定したい」などで起動。
allowed-tools: [Read]
---

# Auth Setup

Google OAuth クライアント（デスクトップアプリ）の作成手順を案内します。

## 手順

### 1. Google Cloud Console にアクセス

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを作成または選択

### 2. API を有効化

以下の API を有効化:

- Google Drive API
- Google Docs API
- Google Sheets API
- Google Slides API
- Google Forms API
- Apps Script API
- Google Calendar API
- Gmail API

### 3. OAuth 同意画面を設定

1. 「APIs & Services」→「OAuth consent screen」
2. User Type: 「External」を選択
3. アプリ情報を入力
4. スコープを追加（上記 API のスコープ）
5. テストユーザーに自分のメールアドレスを追加

### 4. OAuth クライアント ID を作成

1. 「APIs & Services」→「Credentials」
2. 「Create Credentials」→「OAuth client ID」
3. Application type: 「Desktop app」
4. 名前を入力して作成
5. JSON をダウンロード

### 5. クライアント設定を配置

```bash
mkdir -p ~/.config/shiiman-google/clients
mv ~/Downloads/client_secret_*.json ~/.config/shiiman-google/clients/default.json
```

### 6. 認証を実行

「Google ログインして」または「認証して」と言って認証を実行してください。

## 注意事項

- クライアント設定ファイル（`default.json`）には秘密情報が含まれています
- Git にコミットしないでください
- 複数アカウントを使う場合は、プロファイル名を指定して認証できます
