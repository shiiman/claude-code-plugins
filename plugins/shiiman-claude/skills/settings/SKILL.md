---
name: shiiman-claude:settings
description: Claude Code 設定の表示・更新・ローカル更新を統合管理する。「Claude 設定管理」「設定を表示」「settings を更新」「local settings を更新」「権限設定を変更」「設定ファイル管理」「claude settings」などで起動。引数があれば優先し、なければ発話内容から view/update/local-update を判定。
allowed-tools: [Read, Write, Bash, Glob]
argument-hint: "[view|update|local-update] [--help]"
---

# Claude Settings Manage

Claude Code の設定ファイル表示と更新を一つのスキルで管理します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-claude:settings - Claude 設定管理

概要:
  Claude Code 設定の表示・更新・ローカル更新を統合管理する。
  引数があれば優先し、なければ発話内容から操作を判定。

使用方法:
  /shiiman-claude:settings [操作] [オプション]

操作:
  view          設定を表示
  update        .claude/settings.json を更新
  local-update  .claude/settings.local.json を更新

オプション:
  --help        このヘルプを表示

例:
  /shiiman-claude:settings              # 発話内容から操作を判定
  /shiiman-claude:settings view         # 設定を表示
  /shiiman-claude:settings update       # settings.json を更新
  /shiiman-claude:settings local-update # settings.local.json を更新
```

## 実行手順

### 1. 操作種別の決定

- 引数が指定されていれば引数を優先
- 引数がない場合は発話内容から以下を判定:
  - 表示系: view
  - 更新系: update
  - ローカル更新系: local-update

### 2. 操作の実行

#### view

1. `.claude/settings.json` を読み込む
2. `.claude/settings.local.json` が存在する場合は読み込む
3. 設定内容をセクション別に整形表示

#### update

1. `.claude/settings.json` の存在確認（なければ作成フローへ）
2. 変更内容を確認（permissions / allowedTools / env / hooks / その他）
3. 既存設定を保持したマージ更新を実施
4. 更新結果を報告

#### local-update

1. `.claude/settings.local.json` の存在確認（なければ作成フローへ）
2. 変更内容を確認（個人用 permissions / allowedTools / env / その他）
3. 既存設定を保持したマージ更新を実施
4. 更新結果を報告

## ファイル未存在時の作成

- `.claude` ディレクトリがない場合は `mkdir -p .claude`
- それぞれテンプレートから新規作成可能

### settings.json 基本テンプレート

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "allowedTools": []
}
```

### settings.local.json 基本テンプレート

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

## 出力フォーマット

```markdown
## Claude Settings 管理

### 実行モード

- view / update / local-update

### 結果

- 対象ファイル: .claude/settings.json or .claude/settings.local.json
- 変更点: 箇条書きで要約
- ステータス: 成功 / 失敗
```

## 重要な注意事項

- ✅ settings.json / settings.local.json の役割を区別する
- ✅ 既存設定を保持したマージ更新を行う
- ✅ 機密情報は表示時にマスクする
- ✅ ファイルがなければテンプレートで作成できる
- ❌ 設定ファイル全体を無条件上書きしない
