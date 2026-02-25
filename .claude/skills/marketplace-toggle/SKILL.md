---
name: marketplace-toggle
description: マーケットプレイスのソースを dev（directory）/ prd（git）に切り替える。「マーケットプレイス切替」「marketplace toggle」「dev モード」「prd モード」「ローカル開発モード」「開発モード切替」「マーケットプレイス dev」などで起動。
allowed-tools: [Read, Bash, AskUserQuestion]
argument-hint: "[dev|prd|status] [--help]"
user-invocable: true
---

# Marketplace Toggle

マーケットプレイスの installLocation をシンボリックリンク（dev）/ git clone（prd）に切り替える。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/marketplace-toggle - Marketplace Toggle

概要:
  マーケットプレイスの installLocation を切り替えます。
  - dev: installLocation をプロジェクトディレクトリへの symlink に差し替え
  - prd: installLocation を元の git clone に復元
  切り替え後は Claude Code の再起動が必要です。

使用方法:
  /marketplace-toggle [dev|prd|status] [オプション]

サブコマンド:
  dev     symlink に切り替え（開発用）
  prd     git clone に復元（本番用）
  status  現在のモードを表示（デフォルト）

オプション:
  --help  このヘルプを表示

例:
  /marketplace-toggle dev      # ローカル開発モードに切り替え
  /marketplace-toggle prd      # git モードに戻す
  /marketplace-toggle status   # 現在のモードを確認
  /marketplace-toggle          # status と同じ
```

## 仕組み

Claude Code はプラグインを以下の流れで読み込む:

```
known_marketplaces.json
  └─ installLocation（git clone またはシンボリックリンク）
       └─ marketplace.json + plugins/*/
            └─ /plugin install 時に cache/ にコピー
                 └─ installed_plugins.json の installPath から読み込み
```

`source` フィールドを変更しても `installLocation` は更新されないため、installLocation 自体を差し替える必要がある。

## 定数

- **installLocation**: `~/.claude/plugins/marketplaces/shiiman-claude-code-plugins`
- **git clone バックアップ**: `~/.claude/plugins/marketplaces/shiiman-claude-code-plugins.git-backup`
- **プロジェクトディレクトリ**: `/Users/a12665/Documents/personal/claude-code-plugins`

## ワークフロー

### 1. サブコマンド判定

`$ARGUMENTS` から判定:

- `dev` → ステップ 3（dev 切り替え）
- `prd` → ステップ 4（prd 切り替え）
- `status` または引数なし → ステップ 2（状態表示）
- 引数がない場合は発話内容から判定（「開発モード」→ dev、「本番モード」→ prd）

### 2. 現在の状態を表示

```bash
readlink ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins 2>/dev/null || echo "NOT_SYMLINK"
```

- シンボリックリンク → `現在: dev モード（symlink → {リンク先}）`
- 通常ディレクトリ → `現在: prd モード（git clone）`

status の場合はここで終了。

### 3. dev モードに切り替え

#### 3-1. 事前チェック

```bash
# すでに symlink なら何もしない
if [ -L ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins ]; then
  echo "すでに dev モードです"
  exit 0
fi
```

#### 3-2. git clone をバックアップ

```bash
mv ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins.git-backup
```

#### 3-3. シンボリックリンク作成

```bash
ln -s /Users/a12665/Documents/personal/claude-code-plugins ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins
```

#### 3-4. 確認

```bash
readlink ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins
```

切り替え後、以下を表示:

```
✅ dev モードに切り替えました
  installLocation → symlink → /Users/a12665/Documents/personal/claude-code-plugins

次のステップ:
  Claude Code を再起動してください。ローカルの変更が反映されます。
```

### 4. prd モードに切り替え

#### 4-1. 事前チェック

```bash
# symlink でなければ何もしない
if [ ! -L ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins ]; then
  echo "すでに prd モードです"
  exit 0
fi

# バックアップが存在するか確認
if [ ! -d ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins.git-backup ]; then
  echo "エラー: git clone のバックアップが見つかりません"
  exit 1
fi
```

#### 4-2. symlink を削除

```bash
rm ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins
```

#### 4-3. git clone を復元

```bash
mv ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins.git-backup ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins
```

#### 4-4. git pull で最新化

```bash
git -C ~/.claude/plugins/marketplaces/shiiman-claude-code-plugins pull
```

切り替え後、以下を表示:

```
✅ prd モードに切り替えました
  installLocation → git clone（git pull 済み）

次のステップ:
  Claude Code を再起動してください。git リモートの最新版が反映されます。
```

## 注意事項

- 切り替え後は **Claude Code の再起動が必要**
- dev モードではプロジェクトディレクトリの変更が直接反映される（cache 更新不要）
- prd モードでは git リモートの最新コミットが使用される
- git clone バックアップ（`.git-backup`）は prd 復元時に必要。手動で削除しないこと
