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
| `search:read` | メッセージ検索 |

3. ワークスペースにインストール
4. **Bot User OAuth Token** (`xoxb-...`) をコピー

### 2. Team ID の取得

1. Slack Webアプリを開く
2. ワークスペース名をクリック → 「設定と管理」→ 「ワークスペースの設定」
3. URLから Team ID を取得: `https://app.slack.com/client/T01234567/...`
   - `T01234567` が Team ID

### 3. Claude Code への設定

`.claude/settings.local.json` に追加:

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_TEAM_ID": "T01234567"
      }
    }
  }
}
```

**重要**: PythonスクリプトもMCP設定で設定した環境変数（`SLACK_BOT_TOKEN`、`SLACK_TEAM_ID`など）を使用します。

**環境変数の読み込み方法**:
Pythonスクリプトは以下の順序で環境変数を取得します:
1. `os.environ`（Claude Codeが設定した環境変数）
2. 設定ファイルから直接読み込み（環境変数が設定されていない場合）

**設定ファイルの読み込み順序**（環境変数が設定されていない場合）:
1. `.claude/settings.local.json`（プロジェクトローカル設定、最も優先）
2. `.claude/settings.json`（プロジェクト設定）
3. `~/.claude/settings.local.json`（グローバルローカル設定）
4. `~/.claude/settings.json`（グローバル設定）

これにより、Claude Codeが環境変数を設定していない場合でも、設定ファイルから直接読み込んで動作します。

今後追加される環境変数も、MCP設定の`env`セクションに追加するだけで自動的に利用できます。

### 4. Python依存関係のインストール

```bash
pip install slack-sdk
```

## 機能

### コマンド（6個）

| コマンド | 説明 |
|----------|------|
| `/shiiman-slack:channel-list` | チャンネル一覧を取得 |
| `/shiiman-slack:channel-search` | チャンネルを検索 |
| `/shiiman-slack:message-history` | メッセージ履歴を取得 |
| `/shiiman-slack:message-unread` | 未読メッセージ一覧 |
| `/shiiman-slack:message-mentions` | メンション一覧を取得 |
| `/shiiman-slack:user-profile` | ユーザープロファイル取得 |

### スキル（15個）

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

公式MCPの `slack_post_message` を使用します。

### スレッド返信

```
さっきのメッセージにスレッドで返信して
```

公式MCPの `slack_reply_to_thread` を使用します。

### メッセージ編集（独自実装）

```
さっきのメッセージを「訂正: お疲れ様でした」に編集して
```

Pythonスクリプト `slack_message.py edit` を使用します。

### メッセージ削除（独自実装）

```
さっきのメッセージを削除して
```

Pythonスクリプト `slack_message.py delete` を使用します。

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
- Bot が投稿したメッセージのみ編集・削除可能です
- 他のユーザーが投稿したメッセージは編集・削除できません

## 技術詳細

### アーキテクチャ

```
公式Slack MCP (@modelcontextprotocol/server-slack)
  ├─ チャンネル一覧
  ├─ メッセージ送信
  ├─ スレッド返信
  ├─ リアクション追加
  ├─ チャンネル履歴取得
  ├─ スレッド返信取得
  └─ ユーザープロファイル取得

独自Pythonスクリプト (各スキルの scripts/ ディレクトリ)
  ├─ skills/message-summarizer/scripts/
  │   ├─ slack_utils.py
  │   └─ slack_message.py (summarize)
  ├─ skills/unread-checker/scripts/
  │   ├─ slack_utils.py
  │   └─ slack_message.py (unread, mark-read, edit, delete)
  ├─ skills/mention-checker/scripts/
  │   ├─ slack_utils.py
  │   └─ slack_message.py (mentions, thread-users)
  └─ skills/channel-lister/scripts/
      ├─ slack_utils.py
      └─ slack_channel.py (search)
```

### Pythonスクリプトの使用方法

環境変数 `SLACK_BOT_TOKEN` を設定:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

スクリプト実行例:

```bash
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

# メッセージ要約
python plugins/shiiman-slack/skills/message-summarizer/scripts/slack_message.py summarize \
  --channel C01234567 \
  --max 50 \
  --format json
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
