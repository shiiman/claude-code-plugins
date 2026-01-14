# shiiman-slack

Slack ワークスペース管理プラグイン

## 概要

Slack User Token を使用してワークスペースを操作します。

チャンネル管理、メッセージの送受信・編集・削除、要約、未読確認、メンション確認などの機能を提供します。

## インストール

```bash
/shiiman-plugin:installer shiiman-slack
```

## セットアップ

### 1. Slack App の作成

1. [Slack API](https://api.slack.com/apps) で新しいアプリを作成
2. **OAuth & Permissions** で **User Token Scopes** に以下を追加:

| スコープ | 用途 |
|---------|------|
| `channels:read` | パブリックチャンネル一覧 |
| `channels:history` | パブリックチャンネル履歴 |
| `channels:write` | チャンネル既読マーク |
| `groups:read` | プライベートチャンネル一覧 |
| `groups:history` | プライベートチャンネル履歴 |
| `groups:write` | プライベートチャンネル既読マーク |
| `chat:write` | メッセージ送信・編集・削除 |
| `reactions:write` | リアクション追加 |
| `users:read` | ユーザー情報取得 |
| `users.profile:read` | ユーザープロファイル詳細取得 |
| `users.profile:write` | プロフィール更新 |
| `search:read` | メッセージ検索 |

3. ワークスペースにインストール（**Install to Workspace**）
4. 左メニューの **Install App** ページで **User OAuth Token** (`xoxp-...`) をコピー

### 2. トークンの設定

Claude Code で以下のコマンドを実行:

```
/shiiman-slack:user-setup --token xoxp-your-user-token
```

または、Python スクリプトを直接実行:

```bash
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py token-set --token xoxp-your-token
```

設定を確認:

```bash
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py show
```

### 3. Python依存関係のインストール

```bash
pip install slack-sdk
```

### 設定ファイル

設定は `~/.config/shiiman-slack/config.json` に保存されます:

```json
{
  "slack_token": "xoxp-your-user-token",
  "team_id": "T01234567",
  "default_user_id": "U01234567",
  "workspace": {
    "team_id": "T01234567",
    "team_name": "Your Workspace"
  }
}
```

## 機能

### コマンド（8個）

| コマンド | 説明 |
|----------|------|
| `/shiiman-slack:channel-list` | チャンネル一覧を取得 |
| `/shiiman-slack:channel-search` | チャンネルを検索 |
| `/shiiman-slack:message-history` | メッセージ履歴を取得 |
| `/shiiman-slack:message-unread` | 未読メッセージ一覧 |
| `/shiiman-slack:message-mentions` | メンション一覧を取得 |
| `/shiiman-slack:user-profile` | ユーザープロファイル取得 |
| `/shiiman-slack:user-setup` | トークン設定・ユーザー設定 |
| `/shiiman-slack:profile-update` | 自分のプロフィールを更新 |

### スキル（17個）

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| channel-lister | 「Slackチャンネル一覧」 | チャンネル一覧を取得 |
| channel-searcher | 「チャンネル検索」 | チャンネルを検索 |
| message-reader | 「メッセージ確認」 | メッセージ履歴を取得 |
| message-sender | 「Slackに送信」 | メッセージを送信 |
| thread-replier | 「スレッドに返信」 | スレッドに返信 |
| thread-reader | 「スレッドを読む」 | スレッド返信を取得 |
| reaction-adder | 「リアクション追加」 | リアクションを追加 |
| message-editor | 「メッセージ編集」 | メッセージを編集 |
| message-deleter | 「メッセージ削除」 | メッセージを削除 |
| unread-checker | 「Slack未読確認」 | 未読メッセージを確認 |
| mark-reader | 「既読にして」 | チャンネルを既読化 |
| mention-checker | 「メンション確認」 | 自分へのメンションを確認 |
| message-summarizer | 「Slack要約」 | メッセージを要約 |
| thread-user-lister | 「スレッド参加者」 | スレッド参加者一覧 |
| user-profiler | 「ユーザー情報」 | ユーザープロファイル取得 |
| user-setup | 「ユーザー設定」 | トークン・ユーザー設定 |
| profile-updater | 「プロフィール更新」 | 自分のプロフィールを更新 |

### エージェント

| エージェント | 説明 |
|-------------|------|
| channel-manager | チャンネル管理（一覧、検索、情報取得） |
| message-manager | メッセージ管理（送信、編集、削除、履歴） |
| notification-manager | 通知管理（未読確認、メンション、既読化） |

## 使用例

### 初期設定

```
/shiiman-slack:user-setup --token xoxp-your-user-token
```

### チャンネル一覧を取得

```
Slackのチャンネル一覧を見せて
```

### メッセージを読む

```
#general の最新メッセージを確認して
```

### メッセージ送信

```
#general に「お疲れ様です」と送信して
```

### スレッド返信

```
さっきのメッセージにスレッドで返信して
```

### メッセージ編集

```
さっきのメッセージを「訂正: お疲れ様でした」に編集して
```

### メッセージ削除

```
さっきのメッセージを削除して
```

### 未読確認

```
#project-alpha の未読を確認して
```

### 一括既読化

```
#general を既読にして
```

### メンション確認

```
自分へのメンションを見せて
```

### チャンネル要約

```
#project-alpha の今日の会話を要約して
```

### スレッド参加者確認

```
このスレッドの参加者を見せて
```

### チャンネル検索

```
「project」を含むチャンネルを探して
```

### プロフィール更新

```
ステータスを「会議中」に変更して
```

## トラブルシューティング

### トークン未設定エラー

エラー: `Slack トークンが設定されていません`

**対処法:**

```
/shiiman-slack:user-setup --token xoxp-your-token
```

### チャンネルが見つからない

エラー: `channel_not_found`

**対処法:**

- チャンネルIDが正しいか確認
- プライベートチャンネルの場合は参加しているか確認

### 権限エラー

エラー: `missing_scope`

**対処法:**
- Slack App の OAuth スコープを確認
- 必要なスコープを追加後、再インストール

### メッセージ編集・削除ができない

エラー: `cant_update_message` / `cant_delete_message`

**対処法:**

- 自分が投稿したメッセージのみ編集・削除可能です
- 他のユーザーが投稿したメッセージは編集・削除できません

## 技術詳細

### アーキテクチャ

```
Pythonスクリプト (各スキルの scripts/ ディレクトリ)
  ├─ skills/message-sender/scripts/
  │   └─ slack_post.py (post)
  ├─ skills/thread-replier/scripts/
  │   └─ slack_thread.py (reply)
  ├─ skills/reaction-adder/scripts/
  │   └─ slack_reaction.py (add)
  ├─ skills/message-summarizer/scripts/
  │   └─ slack_message.py (summarize)
  ├─ skills/unread-checker/scripts/
  │   └─ slack_message.py (unread, mark-read, edit, delete)
  ├─ skills/mention-checker/scripts/
  │   └─ slack_message.py (mentions, thread-users)
  ├─ skills/channel-lister/scripts/
  │   └─ slack_channel.py (search)
  ├─ skills/user-setup/scripts/
  │   └─ slack_config.py (token-set, auto-detect, set-user, show, clear)
  └─ skills/profile-updater/scripts/
      └─ slack_profile.py (show, update, clear-status)
```

**注**: 各スキルの `scripts/` ディレクトリには共通ユーティリティ `slack_utils.py` も配置されています。

### Pythonスクリプトの使用方法

スクリプト実行例:

```bash
# トークン設定
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py token-set \
  --token xoxp-your-token

# 設定確認
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py show

# メッセージ送信
python plugins/shiiman-slack/skills/message-sender/scripts/slack_post.py post \
  --channel C01234567 \
  --text "お疲れ様です"

# スレッド返信
python plugins/shiiman-slack/skills/thread-replier/scripts/slack_thread.py reply \
  --channel C01234567 \
  --thread-ts 1234567890.123456 \
  --text "了解しました"

# リアクション追加
python plugins/shiiman-slack/skills/reaction-adder/scripts/slack_reaction.py add \
  --channel C01234567 \
  --timestamp 1234567890.123456 \
  --emoji thumbsup

# メッセージ編集
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py edit \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --text "新しいテキスト"

# 未読確認
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py unread \
  --channel C01234567 \
  --max 20 \
  --format json

# メンション確認
python plugins/shiiman-slack/skills/mention-checker/scripts/slack_message.py mentions \
  --max 20 \
  --format table

# チャンネル検索
python plugins/shiiman-slack/skills/channel-lister/scripts/slack_channel.py search \
  --query "project" \
  --format table

# ユーザー設定（トークンから自動検出）
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py auto-detect

# ユーザー設定（手動）
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py set-user \
  --user-id U01234567

# プロフィール更新
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py update \
  --status-text "会議中" \
  --status-emoji ":calendar:"
```

## 必要条件

- Python 3.8 以上
- `slack-sdk` パッケージ
- Slack ワークスペースの管理者権限（App 作成用）

## ライセンス

MIT License

## 作者

shiiman

## リポジトリ

https://github.com/shiiman/claude-code-plugins
