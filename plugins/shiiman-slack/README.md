# shiiman-slack

Slack ワークスペース管理プラグイン

## 概要

公式Slack MCP (`@modelcontextprotocol/server-slack`) と独自Pythonスクリプトを組み合わせて、Slack ワークスペースを操作します。

チャンネル管理、メッセージの送受信・編集・削除、要約、未読確認、メンション確認などの機能を提供します。

## インストール

```bash
/shiiman-plugin:install shiiman-slack
```

## セットアップ

### 1. Slack App の作成

1. [Slack API](https://api.slack.com/apps) で新しいアプリを作成
2. **OAuth & Permissions** で以下の Bot Token Scopes を追加:

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
| `search:read` | メッセージ検索 |

3. **（オプション）User Token Scopes を追加**（ユーザーとして操作する場合）:

| スコープ                 | 用途                                     |
|--------------------------|------------------------------------------|
| `chat:write`             | ユーザーとしてメッセージ投稿・編集・削除 |
| `reactions:write`        | ユーザーとしてリアクション追加           |
| `users.profile:write`    | 自分のプロフィール更新                   |

4. ワークスペースにインストール
5. **Bot User OAuth Token** (`xoxb-...`) をコピー
6. **（オプション）User OAuth Token** (`xoxp-...`) をコピー

### 2. Team ID の取得

#### 通常のワークスペースの場合

1. ブラウザで [Slack Web アプリ](https://app.slack.com) にログイン
2. 任意のチャンネルを開く（通常画面）
3. **アドレスバーの URL** から Team ID を取得:

   ```
   https://app.slack.com/client/T01234567/C98765432
                                ↑ これが Team ID
   ```

   - `T` で始まる文字列が Team ID です

#### Enterprise Grid 環境の場合

Enterprise Grid では URL に `E` で始まる **Organization ID** が表示されることがあります。
`SLACK_TEAM_ID` には `T` で始まる **Team ID（ワークスペース ID）** が必要です。

**確認方法1: URL から取得**

```
https://app.slack.com/client/E01234567/T98765432/C11111111
                             ↑ Org ID   ↑ これが Team ID
```

**確認方法2: Slack API で取得（推奨）**

Bot Token を使って API から取得できます:

```bash
curl -H "Authorization: Bearer xoxb-your-bot-token" https://slack.com/api/team.info
```

レスポンスの `team.id` フィールドが Team ID です:

```json
{
  "ok": true,
  "team": {
    "id": "T01234567",
    "name": "Your Workspace"
  }
}
```

**確認方法3: チャンネル詳細から取得**

1. チャンネル名をクリック
2. 「About」タブを開く
3. 一番下までスクロールして「Channel ID」を確認
4. その上に表示されるワークスペース情報から Team ID を確認

### 3. Claude Code への MCP 設定

#### 方法1: CLI コマンドで設定（推奨）

```bash
# Bot Token のみ
claude mcp add slack -e SLACK_BOT_TOKEN=xoxb-your-bot-token -e SLACK_TEAM_ID=T01234567 -- npx -y @modelcontextprotocol/server-slack

# User Token も設定（ユーザーとして操作する場合）
claude mcp add slack -e SLACK_BOT_TOKEN=xoxb-your-bot-token -e SLACK_TEAM_ID=T01234567 -e SLACK_USER_TOKEN=xoxp-your-user-token -- npx -y @modelcontextprotocol/server-slack
```

#### 方法2: 設定ファイルを直接編集

プロジェクトルートに `.mcp.json` を作成:

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_TEAM_ID": "T01234567",
        "SLACK_USER_TOKEN": "xoxp-your-user-token"
      }
    }
  }
}
```

**注**: `SLACK_USER_TOKEN` はオプションです。ユーザーとして操作する機能（メッセージ送信、編集、削除、リアクション、プロフィール更新）を使用する場合に設定してください。

または、ユーザー全体で使用する場合は `~/.claude.json` に追加します。

**MCP 設定ファイルの場所**:

| スコープ       | ファイル         | 用途                                 |
|----------------|------------------|--------------------------------------|
| プロジェクト   | `.mcp.json`      | プロジェクト固有（Git で共有可能）   |
| ユーザー       | `~/.claude.json` | 全プロジェクト共通                   |

**重要**: Python スクリプトも MCP 設定で設定した環境変数（`SLACK_BOT_TOKEN`、`SLACK_TEAM_ID` など）を使用します。

**環境変数の読み込み方法**:
Python スクリプトは以下の順序で環境変数を取得します:

1. `os.environ`（Claude Code が設定した環境変数）
2. 設定ファイルから直接読み込み（環境変数が設定されていない場合）

**設定ファイルの読み込み順序**（環境変数が設定されていない場合）:

1. `.mcp.json`（プロジェクト MCP 設定、最も優先）
2. `~/.claude.json`（グローバル MCP 設定）

今後追加される環境変数も、MCP 設定の `env` セクションに追加するだけで自動的に利用できます。

### 4. Python依存関係のインストール

```bash
pip install slack-sdk
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
| `/shiiman-slack:user-setup` | デフォルトユーザーIDを設定 |
| `/shiiman-slack:profile-update` | 自分のプロフィールを更新 |

### スキル（17個）

| スキル | トリガー例 | 説明 |
|--------|------------|------|
| channel-lister | 「Slackチャンネル一覧」 | チャンネル一覧を取得 |
| channel-searcher | 「チャンネル検索」 | チャンネルを検索 |
| message-reader | 「メッセージ確認」 | メッセージ履歴を取得 |
| message-sender | 「Slackに送信」 | メッセージを送信（User Token時はユーザーとして） |
| thread-replier | 「スレッドに返信」 | スレッドに返信（User Token時はユーザーとして） |
| thread-reader | 「スレッドを読む」 | スレッド返信を取得 |
| reaction-adder | 「リアクション追加」 | リアクションを追加（User Token時はユーザーとして） |
| message-editor | 「メッセージ編集」 | メッセージを編集（User Token時は自分の投稿も可） |
| message-deleter | 「メッセージ削除」 | メッセージを削除（User Token時は自分の投稿も可） |
| unread-checker | 「Slack未読確認」 | 未読メッセージを確認 |
| mark-reader | 「既読にして」 | チャンネルを既読化 |
| mention-checker | 「メンション確認」 | 自分へのメンションを確認 |
| message-summarizer | 「Slack要約」 | メッセージを要約 |
| thread-user-lister | 「スレッド参加者」 | スレッド参加者一覧 |
| user-profiler | 「ユーザー情報」 | ユーザープロファイル取得 |
| user-setup | 「ユーザー設定」 | デフォルトユーザーIDを設定 |
| profile-updater | 「プロフィール更新」 | 自分のプロフィールを更新（User Token必須） |

### エージェント

| エージェント | 説明 |
|-------------|------|
| channel-manager | チャンネル管理（一覧、検索、情報取得） |
| message-manager | メッセージ管理（送信、編集、削除、履歴） |
| notification-manager | 通知管理（未読確認、メンション、既読化） |

## 使用例

### チャンネル一覧を取得

```
Slackのチャンネル一覧を見せて
```

公式MCPの `slack_list_channels` を使用します。

### メッセージを読む

```
#general の最新メッセージを確認して
```

公式MCPの `slack_get_channel_history` を使用します。

### メッセージ送信

```
#general に「お疲れ様です」と送信して
```

Pythonスクリプト `slack_post.py post` を使用します。

- User Token が設定されている場合: ユーザーとして投稿
- User Token がない場合: Bot として投稿（確認後）

### スレッド返信

```
さっきのメッセージにスレッドで返信して
```

Pythonスクリプト `slack_thread.py reply` を使用します。

- User Token が設定されている場合: ユーザーとして返信
- User Token がない場合: Bot として返信（確認後）

### メッセージ編集（独自実装）

```
さっきのメッセージを「訂正: お疲れ様でした」に編集して
```

Pythonスクリプト `slack_message.py edit` を使用します。

- User Token が設定されている場合: 自分の投稿を編集可能
- User Token がない場合: Bot 投稿のみ編集可能

### メッセージ削除（独自実装）

```
さっきのメッセージを削除して
```

Pythonスクリプト `slack_message.py delete` を使用します。

- User Token が設定されている場合: 自分の投稿を削除可能
- User Token がない場合: Bot 投稿のみ削除可能

### 未読確認（独自実装）

```
#project-alpha の未読を確認して
```

Pythonスクリプト `slack_message.py unread` を使用します。

### 一括既読化（独自実装）

```
#general を既読にして
```

Pythonスクリプト `slack_message.py mark-read` を使用します。

### メンション確認（独自実装）

```
自分へのメンションを見せて
```

Pythonスクリプト `slack_message.py mentions` を使用します。

### チャンネル要約（独自実装）

```
#project-alpha の今日の会話を要約して
```

Pythonスクリプト `slack_message.py summarize` でメッセージを取得し、LLMで要約します。

### スレッド参加者確認（独自実装）

```
このスレッドの参加者を見せて
```

Pythonスクリプト `slack_message.py thread-users` を使用します。

### チャンネル検索（独自実装）

```
「project」を含むチャンネルを探して
```

Pythonスクリプト `slack_channel.py search` を使用します。

### ユーザー設定（独自実装）

```
自分のユーザーIDをU01234567に設定して
```

Pythonスクリプト `slack_config.py set-user` を使用します。設定したユーザーIDは各スキルで自動的に使用されます。

### プロフィール更新（独自実装）

```
ステータスを「会議中」に変更して
```

Pythonスクリプト `slack_profile.py update` を使用します。

- User Token 必須
- 表示名、ステータステキスト、ステータス絵文字などを更新可能

## トラブルシューティング

### `SLACK_BOT_TOKEN` エラー

エラー: `SLACK_BOT_TOKEN 環境変数が設定されていません`

**対処法:**
- Claude Code の MCP 設定で `env.SLACK_BOT_TOKEN` が正しく設定されているか確認

### チャンネルが見つからない

エラー: `channel_not_found`

**対処法:**
- Bot がチャンネルに招待されているか確認
- プライベートチャンネルの場合は Bot を招待: `/invite @your-bot-name`

### 権限エラー

エラー: `missing_scope`

**対処法:**
- Slack App の OAuth スコープを確認
- 必要なスコープを追加後、再インストール

### メッセージ編集・削除ができない

エラー: `cant_update_message` / `cant_delete_message`

**対処法:**

- User Token がない場合: Bot が投稿したメッセージのみ編集・削除可能です
- User Token がある場合: 自分が投稿したメッセージのみ編集・削除可能です
- 他のユーザーが投稿したメッセージは編集・削除できません

## 技術詳細

### アーキテクチャ

```
公式Slack MCP (@modelcontextprotocol/server-slack)
  ├─ チャンネル一覧
  ├─ チャンネル履歴取得
  ├─ スレッド返信取得
  └─ ユーザープロファイル取得

独自Pythonスクリプト (各スキルの scripts/ ディレクトリ)
  ├─ skills/message-sender/scripts/
  │   └─ slack_post.py (post) ※User Token対応
  ├─ skills/thread-replier/scripts/
  │   └─ slack_thread.py (reply) ※User Token対応
  ├─ skills/reaction-adder/scripts/
  │   └─ slack_reaction.py (add) ※User Token対応
  ├─ skills/message-summarizer/scripts/
  │   └─ slack_message.py (summarize)
  ├─ skills/unread-checker/scripts/
  │   └─ slack_message.py (unread, mark-read, edit, delete) ※edit/deleteはUser Token対応
  ├─ skills/mention-checker/scripts/
  │   └─ slack_message.py (mentions, thread-users)
  ├─ skills/channel-lister/scripts/
  │   └─ slack_channel.py (search)
  ├─ skills/user-setup/scripts/
  │   └─ slack_config.py (set-user, show, clear)
  └─ skills/profile-updater/scripts/
      └─ slack_profile.py (show, update, clear-status) ※User Token必須
```

**注**: 各スキルの `scripts/` ディレクトリには共通ユーティリティ `slack_utils.py` も配置されています。

### Pythonスクリプトの使用方法

環境変数を設定:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_USER_TOKEN="xoxp-your-user-token"  # オプション
```

スクリプト実行例:

```bash
# メッセージ送信（User Tokenがあればユーザーとして投稿）
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

# メッセージ編集（User Tokenがあれば自分の投稿を編集可能）
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

# ユーザー設定
python plugins/shiiman-slack/skills/user-setup/scripts/slack_config.py set-user \
  --user-id U01234567

# プロフィール更新（User Token必須）
python plugins/shiiman-slack/skills/profile-updater/scripts/slack_profile.py update \
  --status-text "会議中" \
  --status-emoji ":calendar:"
```

## 必要条件

- Node.js 18.0 以上（公式MCP用）
- Python 3.8 以上（独自スクリプト用）
- `slack-sdk` パッケージ
- Slack ワークスペースの管理者権限（App 作成用）

## ライセンス

MIT License

## 作者

shiiman

## リポジトリ

https://github.com/shiiman/claude-code-plugins
