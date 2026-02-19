# shiiman-slack

Slack 通知管理プラグイン

## 概要

Slack User Token を使用して通知管理を行います。

未読確認、既読化、メンション確認・返信、プロフィール更新の機能を提供します。

## インストール

```bash
claude plugin install shiiman-slack@shiiman-claude-code-plugins
```

## セットアップ

### 1. Slack App の作成

1. [Slack API](https://api.slack.com/apps) で新しいアプリを作成
2. **OAuth & Permissions** で **User Token Scopes** に以下を追加:

| スコープ              | 用途                             |
| --------------------- | -------------------------------- |
| `channels:read`       | パブリックチャンネル一覧         |
| `channels:history`    | パブリックチャンネル履歴         |
| `channels:write`      | チャンネル既読マーク             |
| `groups:read`         | プライベートチャンネル一覧       |
| `groups:history`      | プライベートチャンネル履歴       |
| `groups:write`        | プライベートチャンネル既読マーク |
| `chat:write`          | スレッド返信                     |
| `users:read`          | ユーザー情報取得                 |
| `users.profile:read`  | ユーザープロファイル詳細取得     |
| `users.profile:write` | プロフィール更新                 |
| `search:read`         | メッセージ検索                   |

3. ワークスペースにインストール（**Install to Workspace**）
4. 左メニューの **Install App** ページで **User OAuth Token** (`xoxp-...`) をコピー

### 2. トークンの設定

> **セキュリティ注意**: トークンを Claude Code の会話内で入力すると、会話履歴に残り Anthropic API に送信されます。以下のいずれかの方法でターミナルから直接設定してください。

#### 方法1: Python スクリプトで設定（推奨）

ターミナルで以下を実行:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-set --token xoxp-your-token
```

設定を確認:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py show
```

#### 方法2: 設定ファイルを直接作成

```bash
mkdir -p ~/.config/shiiman-slack
```

`~/.config/shiiman-slack/config.json` を作成:

```json
{
  "slack_token": "xoxp-your-user-token"
}
```

### 3. Python依存関係のインストール

```bash
pip install slack-sdk
```

## 機能

### スキル（6個）

| スキル                       | トリガー例           | 説明                           |
| ---------------------------- | -------------------- | ------------------------------ |
| shiiman-slack:user-setup     | 「ユーザー設定」     | トークン・ユーザー設定         |
| shiiman-slack:unread-check   | 「Slack未読確認」    | 未読メッセージを確認           |
| shiiman-slack:unread-mark    | 「既読にして」       | チャンネルを既読化             |
| shiiman-slack:mention-check  | 「メンション確認」   | 自分へのメンションを確認       |
| shiiman-slack:mention-reply  | 「スレッドに返信」   | メンションに対してスレッド返信 |
| shiiman-slack:profile-update | 「プロフィール更新」 | 自分のプロフィールを更新       |

### エージェント

| エージェント         | 説明                                     |
| -------------------- | ---------------------------------------- |
| notification-manager | 通知管理（未読確認、メンション、既読化） |

## 使用例

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

### メンションに返信

```
さっきのメンションにスレッドで返信して
```

### プロフィール更新

```
ステータスを「会議中」に変更して
```

## トラブルシューティング

### トークン未設定エラー

エラー: `Slack トークンが設定されていません`

**対処法:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py token-set --token xoxp-your-token
```

### 権限エラー

エラー: `missing_scope`

**対処法:**

- Slack App の OAuth スコープを確認
- 必要なスコープを追加後、再インストール

## 技術詳細

### アーキテクチャ

```
plugins/shiiman-slack/
  ├─ lib/
  │   └─ slack_utils.py (共通ユーティリティ: 認証・出力・エラーハンドリング)
  ├─ scripts/
  │   ├─ slack_message.py (unread, mark-read, mentions)
  │   └─ slack_config.py (token-set, token-show, token-clear, auto-detect, set-user, show, clear)
  └─ skills/
      ├─ mention-reply/scripts/slack_thread.py (reply)
      └─ profile-update/scripts/slack_profile.py (show, update, clear-status)
```

## 必要条件

- Python 3.8 以上
- `slack-sdk` パッケージ
- Slack ワークスペースの管理者権限（App 作成用）

## バージョン履歴

- v4.0.0: スキル名を `slack-xxx` → `shiiman-slack:xxx` 形式にリネーム
- v3.0.0: スキルを 17 → 6 に整理。不要スキル（MCP ラッパー、低使用頻度機能）を削除し、全スキルを `slack-` プレフィックスでリネーム
