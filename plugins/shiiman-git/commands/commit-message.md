# Commit Message

コミットメッセージの命名規則を設定・表示します。

## 使い方

```bash
/shiiman-git:commit-message
/shiiman-git:commit-message --set
/shiiman-git:commit-message --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--help` | このコマンドのヘルプを表示 |
| `--set` | 命名規則を対話的に設定 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

#### `--set` オプションがある場合:

1. プロジェクトの `.claude/settings.json` を読み込み
2. 以下を順番に聞く:

**コミットメッセージ形式**:

| 形式 | 例 |
|------|-----|
| Conventional Commits | `feat: 新機能を追加` |
| 日本語形式 | `新機能: ユーザー認証を追加` |
| カスタム | ユーザー定義 |

**使用するプレフィックス**（Conventional Commits の場合）:

- `feat` - 新機能
- `fix` - バグ修正
- `docs` - ドキュメント
- `refactor` - リファクタリング
- `chore` - その他
- `test` - テスト
- `style` - スタイル修正
- `perf` - パフォーマンス改善

**Issue 参照形式**:

| 形式 | 例 |
|------|-----|
| 末尾括弧 | `feat: 機能追加 (#123)` |
| 先頭 | `#123 feat: 機能追加` |
| なし | Issue 参照しない |

3. 設定を `.claude/settings.json` の `git.commitMessage` に保存

#### オプションなしの場合:

- 現在の設定を表示
- 設定がない場合はデフォルト設定を表示

### 設定ファイル形式

`.claude/settings.json`:

```json
{
  "git": {
    "commitMessage": {
      "format": "conventional",
      "prefixes": ["feat", "fix", "docs", "refactor", "chore", "test"],
      "issueReference": true,
      "issueFormat": "(#N)"
    }
  }
}
```

### 出力フォーマット

```
## コミットメッセージ設定

形式: Conventional Commits
プレフィックス: feat, fix, docs, refactor, chore, test
Issue 参照: あり (末尾括弧形式)

### 例

feat: ユーザー認証機能を追加 (#123)
fix: ログイン時のエラーを修正 (#124)
docs: README を更新
```

## 重要な注意事項

- ✅ プロジェクトごとに設定を保存
- ✅ チームで統一したルールを設定可能
- ❌ 設定なしでもコミットは可能（推奨設定を表示するのみ）
