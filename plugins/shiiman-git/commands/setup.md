# Setup

プロジェクトの `.github` ディレクトリに GitHub 設定ファイルを一括生成します。

## 使い方

```bash
/shiiman-git:setup
/shiiman-git:setup --help
/shiiman-git:setup --dry-run
/shiiman-git:setup --force
```

## オプション

| オプション | 説明 |
|------------|------|
| `--help` | このコマンドのヘルプを表示 |
| `--dry-run` | 生成予定のファイル一覧を表示（実行しない） |
| `--force` | 既存ファイルを上書き |

## 生成されるファイル

| ファイル | 説明 |
|----------|------|
| `.github/ISSUE_TEMPLATE/config.yml` | Issue テンプレート設定 |
| `.github/ISSUE_TEMPLATE/bug-report.yml` | バグ報告テンプレート |
| `.github/ISSUE_TEMPLATE/feature-request.yml` | 機能リクエストテンプレート |
| `.github/ISSUE_TEMPLATE/improvement.yml` | 改善提案テンプレート |
| `.github/pull_request_template.md` | PR テンプレート |
| `.github/copilot-instructions.md` | GitHub Copilot 設定 |
| `.github/labels.yml` | ラベル定義 |
| `.github/labeler.yml` | 自動ラベル付けルール |
| `.github/workflows/sync-labels.yml` | ラベル同期 workflow |
| `.github/workflows/labeler.yml` | 自動ラベル付け workflow |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### ステップ 1: 事前確認

1. `.github` ディレクトリの存在確認
2. 既存ファイルの有無をチェック

**既存ファイルがある場合**:

- `--force` なし: 上書きするか確認
- `--force` あり: 確認なしで上書き

### ステップ 2: プロジェクト情報収集

ユーザーに以下を確認:

1. **プロジェクト名**（リポジトリ名から推測、確認）
2. **プロジェクトタイプ**（選択肢を提示）
   - Web アプリ (React/Vue/etc.)
   - バックエンド (Node.js/Go/Python/etc.)
   - ライブラリ/パッケージ
   - CLI ツール
   - その他

### ステップ 3: テンプレート読み込み

`skills/setup-runner/assets/` からテンプレートを読み込み、プロジェクト情報で変数を置換。

**置換する変数**:

| 変数 | 説明 |
|------|------|
| `{{REPO}}` | リポジトリ名 |
| `{{OWNER}}` | リポジトリオーナー |
| `{{PROJECT_TYPE}}` | プロジェクトタイプ |

### ステップ 4: ファイル生成

以下の順序で生成:

1. `.github/` ディレクトリ作成（なければ）
2. `.github/ISSUE_TEMPLATE/` ディレクトリ作成
3. `.github/workflows/` ディレクトリ作成
4. 各テンプレートファイルを生成

### ステップ 5: 完了報告

生成されたファイル一覧と次のステップを表示:

```
## 生成完了

以下のファイルを生成しました:

- .github/ISSUE_TEMPLATE/config.yml
- .github/ISSUE_TEMPLATE/bug-report.yml
- .github/ISSUE_TEMPLATE/feature-request.yml
- .github/ISSUE_TEMPLATE/improvement.yml
- .github/pull_request_template.md
- .github/copilot-instructions.md
- .github/labels.yml
- .github/labeler.yml
- .github/workflows/sync-labels.yml
- .github/workflows/labeler.yml

## 次のステップ

1. 各テンプレートをプロジェクトに合わせてカスタマイズ
2. `git add .github && git commit -m "chore: GitHub 設定ファイルを追加"`
3. GitHub にプッシュしてラベル同期を実行
```

## 重要な注意事項

- ✅ テンプレートは汎用的な内容なので、プロジェクトに合わせて調整が必要
- ✅ ラベル同期 workflow は main ブランチへのプッシュ時に実行される
- ❌ 既存の設定ファイルを無断で上書きしない
