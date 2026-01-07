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

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | `/shiiman-google:drive-list` | 「Drive 一覧」 | ファイル一覧を取得 |
| 検索 | `/shiiman-google:drive-search` | 「Drive 検索」 | ファイルを検索 |
| 移動 | `/shiiman-google:drive-move` | - | ファイルをフォルダに移動 |
| フォルダ作成 | `/shiiman-google:drive-create-folder` | - | フォルダを新規作成 |
| **共有** | `/shiiman-google:drive-share` | 「ファイルを共有」 | ファイル共有設定（v1.2.0） |
| **共有解除** | `/shiiman-google:drive-unshare` | - | 共有を解除（v1.2.0） |
| **共有確認** | `/shiiman-google:drive-permissions` | 「共有状況確認」 | 共有設定一覧を取得（v1.2.0） |

### Google Calendar

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 予定取得 | - | 「今日の予定」「今週の予定」「今月の予定」 | 期間を指定して予定を取得 |
| 予定追加 | `/shiiman-google:calendar-add` | 「予定追加」「カレンダーに追加」 | 予定を追加（色・カレンダー指定可） |
| **予定詳細** | `/shiiman-google:calendar-get` | - | イベント詳細を取得（v1.2.0） |
| **予定更新** | `/shiiman-google:calendar-update` | 「予定を変更」 | 予定を編集（v1.2.0） |
| **予定削除** | `/shiiman-google:calendar-delete` | 「予定を削除」 | 予定を削除（v1.2.0） |

### Gmail

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 未読一覧 | `/shiiman-google:gmail-read` | 「未読メール」「全アカウント未読」 | 未読メッセージ一覧を取得 |
| 本文表示 | `/shiiman-google:gmail-read` | 「メールを読んで」 | メッセージ本文を表示 |
| 既読化 | `/shiiman-google:gmail-mark-read` | 「既読にして」「全部既読」 | 未読を既読に変更 |
| スター付け | `/shiiman-google:gmail-star` | 「スターを付けて」 | メッセージにスター付け |
| スター付き一覧 | - | 「スター付きメール」 | スター付きメッセージ一覧 |
| 送信 | `/shiiman-google:gmail-send` | 「メール送信」「メールを送って」 | メールを送信 |
| 下書き | `/shiiman-google:gmail-draft` | 「下書き作成」「下書きを保存」 | 下書きを作成 |
| **検索** | `/shiiman-google:gmail-search` | 「メール検索」 | Gmail検索クエリで検索（v1.2.0） |

### Google Docs

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | - | 「Docs 一覧」 | ドキュメント一覧を取得 |
| 検索 | `/shiiman-google:docs-search` | 「Docs 検索」 | ドキュメントを検索 |
| 作成 | `/shiiman-google:docs-create` | 「ドキュメント作成」 | 新規ドキュメントを作成 |
| 取得 | `/shiiman-google:docs-get` | - | ドキュメント内容を取得 |
| 更新 | `/shiiman-google:docs-update` | 「ドキュメント更新」 | テキストを追加 |
| **エクスポート** | `/shiiman-google:docs-export` | 「DocsをPDFで」 | PDF/Word等でエクスポート（v1.2.0） |

### Google Sheets

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | - | 「Sheets 一覧」 | スプレッドシート一覧を取得 |
| 検索 | `/shiiman-google:sheets-search` | 「Sheets 検索」 | スプレッドシートを検索 |
| 作成 | `/shiiman-google:sheets-create` | 「スプレッドシート作成」 | 新規スプレッドシートを作成 |
| 取得 | `/shiiman-google:sheets-get` | - | セルデータを取得 |
| 更新 | `/shiiman-google:sheets-update` | 「スプレッドシート更新」 | セルを更新 |
| **エクスポート** | `/shiiman-google:sheets-export` | 「SheetsをCSVで」 | CSV/Excel等でエクスポート（v1.2.0） |

### Google Slides

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | - | 「Slides 一覧」 | プレゼンテーション一覧を取得 |
| 検索 | `/shiiman-google:slides-search` | 「Slides 検索」 | プレゼンテーションを検索 |
| 作成 | `/shiiman-google:slides-create` | 「プレゼン作成」 | 新規プレゼンテーションを作成 |
| 取得 | `/shiiman-google:slides-get` | - | スライド情報を取得 |
| スライド追加 | `/shiiman-google:slides-add-slide` | 「スライド追加」 | スライドを追加 |
| **エクスポート** | `/shiiman-google:slides-export` | 「SlidesをPDFで」 | PDF/PowerPoint等でエクスポート（v1.2.0） |

### Google Forms

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | - | 「Forms 一覧」 | フォーム一覧を取得 |
| 検索 | `/shiiman-google:forms-search` | 「Forms 検索」 | フォームを検索 |
| 作成 | `/shiiman-google:forms-create` | 「フォーム作成」 | 新規フォームを作成 |
| 取得 | `/shiiman-google:forms-get` | - | フォーム情報を取得 |
| 質問追加 | `/shiiman-google:forms-add-question` | 「質問追加」 | 質問を追加 |
| **回答取得** | `/shiiman-google:forms-responses` | 「フォームの回答」 | 回答一覧を取得（v1.2.0） |

### Google Apps Script

| 機能 | コマンド | スキルトリガー | 説明 |
|------|----------|---------------|------|
| 一覧 | - | 「GAS 一覧」 | スクリプト一覧を取得 |
| 検索 | `/shiiman-google:apps-script-search` | 「GAS 検索」 | スクリプトを検索 |
| 作成 | `/shiiman-google:apps-script-create` | 「GAS 作成」 | 新規スクリプトを作成 |
| 取得 | `/shiiman-google:apps-script-get` | - | スクリプト内容を取得 |
| 更新 | `/shiiman-google:apps-script-update` | 「GAS 更新」 | コードを更新 |

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
├── scripts/                     # Python スクリプト
│   ├── google_utils.py          # 共通ユーティリティ
│   ├── google_auth.py           # 認証
│   ├── google_drive.py          # Drive API
│   ├── google_gmail.py          # Gmail API
│   ├── google_calendar.py       # Calendar API
│   ├── google_docs.py           # Docs API
│   ├── google_sheets.py         # Sheets API
│   ├── google_slides.py         # Slides API
│   ├── google_forms.py          # Forms API
│   └── google_apps_script.py    # Apps Script API
├── commands/                    # スラッシュコマンド
└── skills/                      # 自然言語トリガースキル
```

## ライセンス

MIT
