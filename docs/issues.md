# Issue 作成ガイド

## 概要

このリポジトリでは、Issue はローカルのスキルコマンドではなく、GitHub の Issue Template から作成します。

## 前提

- GitHub 上でこのリポジトリを開けること
- `New issue` 画面にアクセスできること

## 利用するテンプレート

`.github/ISSUE_TEMPLATE/` 配下のテンプレートを利用します。

| テンプレート | 用途 | 付与ラベル |
|-------------|------|-----------|
| `plugin-creation.yml` | 新しいプラグイン作成 | `enhancement`, `plugin` |
| `skill-creation.yml` | 既存プラグインへのスキル追加 | `enhancement`, `skill` |
| `subagent-creation.yml` | 既存プラグインへのサブエージェント追加 | `enhancement`, `subagent` |
| `hook-creation.yml` | 既存プラグインへのフック追加 | `enhancement`, `hook` |
| `other-request.yml` | その他の機能追加・改善提案・質問 | `question` |

### 設定ファイル

`config.yml` では `blank_issues_enabled: false` が設定されているため、テンプレートを選択して起票する運用です。

## 起票手順（GitHub UI）

1. GitHub の `Issues` タブを開く
2. `New issue` をクリック
3. 用途に合うテンプレートを選択
4. 必須項目を入力して `Submit new issue` で作成

## テンプレート別の入力ポイント

### プラグイン作成 (`plugin-creation.yml`)

- プラグイン名: 小文字・ハイフン区切り
- 説明: 1-2文で目的を記載

### スキル追加 (`skill-creation.yml`)

- 対象プラグイン: `shiiman-xxx` 形式
- スキル名: 小文字・ハイフン区切り
- 説明: 目的とトリガーフレーズ

### サブエージェント追加 (`subagent-creation.yml`)

- 対象プラグイン: `shiiman-xxx` 形式
- サブエージェント名: 小文字・ハイフン区切り
- 説明: 目的と使用ツール

### フック追加 (`hook-creation.yml`)

- 対象プラグイン: `shiiman-xxx` 形式
- イベント: `PreToolUse` / `PostToolUse` など
- マッチャー: `PreToolUse` / `PostToolUse` の場合は指定
- フックタイプ: `command` または `prompt`
- 説明: 実行目的と内容

## 起票後の進め方

- 実装は通常の開発フローで進める
- 必要に応じてグローバルスキルまたは `shiiman-git` 側のスキルで GitHub 操作（PR作成など）を行う
