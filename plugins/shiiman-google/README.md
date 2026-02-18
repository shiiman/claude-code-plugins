# shiiman-google

Google Workspace 操作（認証、Drive 検索、Docs/Sheets/Slides/Forms/Apps Script 編集、Calendar、Gmail 未読管理）を Claude Code から実行するプラグイン。

## インストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add shiiman/claude-code-plugins

# プラグインをインストール
/plugin install shiiman-google@shiiman-claude-code-plugins
```

## 前提条件

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 機能一覧

### 認証・プロファイル

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| google-auth-setup | 「OAuth 設定」「認証準備」 | OAuth クライアント作成手順を案内 |
| google-auth-login | 「Google ログイン」「認証して」 | ブラウザで Google 認証を実行 |
| google-profile-switch | 「アカウント切替」「プロファイル変更」 | 保存済みプロファイルを切り替え |

### Google Drive

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| google-drive-search | 「Drive 検索」「ファイルを探して」 | ファイルを検索 |

### Google Docs / Sheets / Slides / Forms / Apps Script

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| google-docs | 「ドキュメント作成」「ドキュメント更新」 | ドキュメントの新規作成・テキスト追加 |
| google-sheets | 「スプレッドシート作成」「セルを更新」 | スプレッドシートの新規作成・セル更新 |
| google-slides | 「プレゼン作成」「スライド追加」 | プレゼンテーションの新規作成・スライド追加 |
| google-forms | 「フォーム作成」「質問追加」 | フォームの新規作成・質問追加 |
| google-apps-script | 「GAS 作成」「GAS 更新」 | スクリプトの新規作成・コード更新 |

### Google Calendar

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| google-calendar | 「今日の予定」「今週の予定」「今月の予定」 | 期間を指定して予定を取得 |

### Gmail

| スキル | トリガー例 | 説明 |
|--------|-----------|------|
| google-gmail-unread-check | 「未読メール」「Gmail 未読」 | 未読メッセージ一覧を取得 |
| google-gmail-unread-mark | 「既読にして」「全部既読」 | 未読を既読に変更 |

## 使い方

### 1. OAuth クライアント設定

```
「OAuth 設定して」
```

手順に従って Google Cloud Console で OAuth クライアントを作成し、`~/.config/shiiman-google/clients/default.json` に配置。

### 2. 認証

```
「Google ログインして」
```

ブラウザが開き、Google アカウントで認証。トークンは `~/.config/shiiman-google/tokens/` に保存。

### 3. 複数アカウント

```
「別のアカウントでログイン」  # --profile work などを指定
「アカウント切替」            # プロファイル一覧から選択
「全アカウントの未読メール」  # 全プロファイルの未読を一括取得
```

### 4. 各種操作例

```
「今日の予定を教えて」
「未読メールを見せて」
「新しいドキュメントを作成して」
「スプレッドシートの A1 セルを更新して」
「プレゼンにスライドを追加して」
「フォームに質問を追加して」
```

## 参考ドキュメント

- [認証・トークン運用リファレンス](docs/auth-reference.md) — OAuth の保存先・スコープ一覧

## ディレクトリ構成

```
plugins/shiiman-google/
├── .claude-plugin/plugin.json   # プラグインメタデータ
├── docs/                        # 参考ドキュメント
│   └── auth-reference.md        # 認証・トークン運用リファレンス
├── lib/                         # 共有ライブラリ
│   └── google_utils.py          # 共通ユーティリティ（認証・出力・リトライ）
├── scripts/                     # 集約スクリプト
│   ├── google_auth.py           # 認証
│   ├── google_calendar.py       # Calendar
│   ├── google_docs.py           # Docs
│   ├── google_drive.py          # Drive
│   ├── google_forms.py          # Forms
│   ├── google_gmail.py          # Gmail
│   ├── google_sheets.py         # Sheets
│   ├── google_slides.py         # Slides
│   └── google_apps_script.py    # Apps Script
└── skills/                      # 自然言語トリガースキル（12スキル）
    ├── google-auth-setup/
    ├── google-auth-login/
    ├── google-profile-switch/
    ├── google-drive-search/
    ├── google-docs/
    ├── google-sheets/
    ├── google-slides/
    ├── google-forms/
    ├── google-apps-script/
    ├── google-calendar/
    ├── google-gmail-unread-check/
    └── google-gmail-unread-mark/
```

## バージョン履歴

- **v2.0.0** - スキル整理（41→12スキル）、create+update 統合、`google-` プレフィックス統一
- **v1.5.1** - 初期版（41スキル）

## ライセンス

MIT
