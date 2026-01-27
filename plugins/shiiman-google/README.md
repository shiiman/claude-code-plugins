# shiiman-google

Google Workspace 操作（認証、Drive/Docs/Sheets/Slides/Forms/Apps Script、Calendar、Gmail）を Claude Code から実行するプラグイン。

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

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| OAuth セットアップ | 「OAuth 設定」「認証準備」 | OAuth クライアント作成手順を案内 |
| OAuth ログイン | 「Google ログイン」「認証して」 | ブラウザで Google 認証を実行 |
| プロファイル切替 | 「アカウント切替」「プロファイル変更」 | 保存済みプロファイルを切り替え |

### Google Drive

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「Drive 一覧」 | ファイル一覧を取得 |
| 検索 | 「Drive 検索」 | ファイルを検索 |
| 共有 | 「ファイルを共有」 | ファイル共有設定 |
| 共有確認 | 「共有状況確認」 | 共有設定一覧を取得 |

### Google Calendar

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 予定取得 | 「今日の予定」「今週の予定」「今月の予定」 | 期間を指定して予定を取得 |
| 予定追加 | 「予定追加」「カレンダーに追加」 | 予定を追加（色・カレンダー指定可） |
| 予定更新 | 「予定を変更」 | 予定を編集 |
| 予定削除 | 「予定を削除」 | 予定を削除 |

### Gmail

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 未読一覧 | 「未読メール」「全アカウント未読」 | 未読メッセージ一覧を取得 |
| 本文表示 | 「メールを読んで」 | メッセージ本文を表示 |
| 検索 | 「メール検索」 | Gmail検索クエリで検索 |
| 既読化 | 「既読にして」「全部既読」 | 未読を既読に変更 |
| スター付け | 「スターを付けて」 | メッセージにスター付け |
| スター付き一覧 | 「スター付きメール」 | スター付きメッセージ一覧 |
| 送信 | 「メール送信」「メールを送って」 | メールを送信 |
| 下書き | 「下書き作成」「下書きを保存」 | 下書きを作成 |

### Google Docs

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「Docs 一覧」 | ドキュメント一覧を取得 |
| 検索 | 「Docs 検索」 | ドキュメントを検索 |
| 作成 | 「ドキュメント作成」 | 新規ドキュメントを作成 |
| 更新 | 「ドキュメント更新」 | テキストを追加 |
| エクスポート | 「DocsをPDFで」 | PDF/Word等でエクスポート |

### Google Sheets

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「Sheets 一覧」 | スプレッドシート一覧を取得 |
| 検索 | 「Sheets 検索」 | スプレッドシートを検索 |
| 作成 | 「スプレッドシート作成」 | 新規スプレッドシートを作成 |
| 更新 | 「スプレッドシート更新」 | セルを更新 |
| エクスポート | 「SheetsをCSVで」 | CSV/Excel等でエクスポート |

### Google Slides

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「Slides 一覧」 | プレゼンテーション一覧を取得 |
| 検索 | 「Slides 検索」 | プレゼンテーションを検索 |
| 作成 | 「プレゼン作成」 | 新規プレゼンテーションを作成 |
| スライド追加 | 「スライド追加」 | スライドを追加 |
| エクスポート | 「SlidesをPDFで」 | PDF/PowerPoint等でエクスポート |

### Google Forms

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「Forms 一覧」 | フォーム一覧を取得 |
| 検索 | 「Forms 検索」 | フォームを検索 |
| 作成 | 「フォーム作成」 | 新規フォームを作成 |
| 質問追加 | 「質問追加」 | 質問を追加 |
| 回答取得 | 「フォームの回答」 | 回答一覧を取得 |

### Google Apps Script

| 機能 | スキルトリガー | 説明 |
|------|---------------|------|
| 一覧 | 「GAS 一覧」 | スクリプト一覧を取得 |
| 検索 | 「GAS 検索」 | スクリプトを検索 |
| 作成 | 「GAS 作成」 | 新規スクリプトを作成 |
| 更新 | 「GAS 更新」 | コードを更新 |

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
「全部既読にして」            # 全プロファイルの未読を一括既読化
```

### 4. 各種操作例

```
「今日の予定を教えて」
「明日 14:00-15:00 に会議を追加して」
「未読メールを見せて」
「user@example.com にメールを送って」
「新しいドキュメントを作成して」
「スプレッドシートの A1 セルを更新して」
「プレゼンにスライドを追加して」
「フォームに質問を追加して」
```

## ディレクトリ構成

```
plugins/shiiman-google/
├── .claude-plugin/plugin.json   # プラグインメタデータ
└── skills/                      # 自然言語トリガースキル
    ├── auth-login/
    │   └── scripts/             # 認証関連スクリプト
    │       ├── google_utils.py  # 共通ユーティリティ
    │       └── google_auth.py   # 認証
    ├── calendar-list-events/
    │   └── scripts/             # カレンダー関連スクリプト
    │       ├── google_utils.py
    │       └── google_calendar.py
    ├── docs-list/
    │   └── scripts/              # ドキュメント関連スクリプト
    │       ├── google_utils.py
    │       └── google_docs.py
    ├── drive-list/
    │   └── scripts/              # ドライブ関連スクリプト
    │       ├── google_utils.py
    │       └── google_drive.py
    ├── forms-list/
    │   └── scripts/              # フォーム関連スクリプト
    │       ├── google_utils.py
    │       └── google_forms.py
    ├── gmail-list-unread/
    │   └── scripts/              # Gmail関連スクリプト
    │       ├── google_utils.py
    │       └── google_gmail.py
    ├── sheets-list/
    │   └── scripts/              # スプレッドシート関連スクリプト
    │       ├── google_utils.py
    │       └── google_sheets.py
    ├── slides-list/
    │   └── scripts/              # スライド関連スクリプト
    │       ├── google_utils.py
    │       └── google_slides.py
    └── apps-script-list/
        └── scripts/              # Apps Script関連スクリプト
            ├── google_utils.py
            └── google_apps_script.py
```

## ライセンス

MIT
