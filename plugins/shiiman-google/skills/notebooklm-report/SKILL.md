---
name: shiiman-google:notebooklm-report
description: NotebookLM でレポートを作成する。「NotebookLM レポート」「レポート作成」「ブリーフィングドキュメント」「NotebookLM ブリーフィング」「学習ガイド作成」「ブログポスト作成」「NotebookLM 文書」などで起動。notebooklm-mcp を使用。
argument-hint: "[--help]"
---

# NotebookLM Report

NotebookLM のノートブックからレポート（Briefing Doc / Study Guide / Blog Post / Create Your Own）を作成する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-google:notebooklm-report - NotebookLM Report

概要:
  ノートブックのソースからレポートを作成します。

使用方法:
  /shiiman-google:notebooklm-report [オプション]

オプション:
  --help  このヘルプを表示
```

## 使用する MCP ツール

- `mcp__notebooklm-mcp__notebook_create`
- `mcp__notebooklm-mcp__notebook_list`
- `mcp__notebooklm-mcp__note_create`
- `mcp__notebooklm-mcp__source_list`
- `mcp__notebooklm-mcp__studio_create`
- `mcp__notebooklm-mcp__studio_status`
- `mcp__notebooklm-mcp__artifact_download`
- `mcp__notebooklm-mcp__artifact_export`

## ワークフロー

### 1. MCP ツールのロード

ToolSearch で `+notebooklm` を検索し、notebooklm-mcp の MCP ツールをロードする。

ツールが見つからない場合は「notebooklm-mcp MCP サーバーが設定されていません。MCP サーバーの設定を確認してください。」と案内して終了する。

### 2. ノートブックの準備

AskUserQuestion でノートブックの準備方法を選択してもらう:

- **既存のノートブックを使う** — 作成済みのノートブックから選択
- **新規ノートブックを作成** — タイトルと内容を指定して新規作成

#### 2a. 既存ノートブックの場合

```
mcp__notebooklm-mcp__notebook_list()
```

ノートブック一覧を取得し、AskUserQuestion で対象ノートブックの選択を求める。選択されたノートブックの `notebook_id` を保持する。

#### 2b. 新規ノートブックの場合

1. AskUserQuestion でノートブック名を質問する
2. AskUserQuestion でソースとなるテキスト内容を質問する（レポート化したい情報を入力してもらう）
3. ノートブックを作成する:

```
mcp__notebooklm-mcp__notebook_create(title="{ノートブック名}")
```

4. 入力されたテキストをノートとして追加する:

```
mcp__notebooklm-mcp__note_create(
  notebook_id="{notebook_id}",
  content="{テキスト内容}",
  title="{ノートブック名}"
)
```

作成されたノートブックの `notebook_id` を保持する。

### 3. プロンプト方式の選択

AskUserQuestion でプロンプトの入力方式を選択してもらう:

- **テンプレートから選ぶ** — プリセットテンプレートを使用（推奨）
- **カスタムプロンプトを入力** — 自由にプロンプトを入力

#### 3a. テンプレート選択の場合

`assets/prompts/` 配下のテンプレートファイルを Read で読み込み、一覧を提示する。

**テンプレート一覧（グループ 1）:**

| ID            | 名前           | 説明                                             | 推奨 report_format |
| ------------- | -------------- | ------------------------------------------------ | ------------------ |
| `briefing`    | ブリーフィング | ソースの要点・知見・提言をまとめた簡潔なサマリー | Briefing Doc       |
| `study-guide` | 学習ガイド     | 学習者向けに重要概念・用語・復習問題を整理       | Study Guide        |
| `faq`         | FAQ            | ソースの内容をよくある質問と回答の形式で整理     | Create Your Own    |
| `blog-post`   | ブログポスト   | ソースの内容を読みやすいブログ記事に変換         | Blog Post          |

**テンプレート一覧（グループ 2）:**

| ID            | 名前                   | 説明                                           | 推奨 report_format |
| ------------- | ---------------------- | ---------------------------------------------- | ------------------ |
| `executive`   | エグゼクティブサマリー | 意思決定者向けの簡潔な概要・結論・提言         | Briefing Doc       |
| `comparison`  | 比較レポート           | 複数の対象を比較分析してまとめるレポート       | Briefing Doc       |
| `action-plan` | アクションプラン       | ソースから具体的な行動計画・タスクリストを抽出 | Briefing Doc       |
| `pros-cons`   | メリット・デメリット   | 特定のトピックの長所・短所を整理して評価       | Briefing Doc       |

AskUserQuestion で 4 つずつ選択肢を提示する（AskUserQuestion は最大 4 選択肢のため、2 回に分けて表示）。

1 回目: briefing, study-guide, faq, blog-post
2 回目（1 回目で「他のテンプレートを見る」を選んだ場合）: executive, comparison, action-plan, pros-cons

選択されたテンプレートの `.md` ファイルを Read で読み込み:

- frontmatter の `report_format` を推奨値として自動設定
- body 部分を `custom_prompt` として使用

推奨値をユーザーに提示し、「このパラメータで作成しますか？」と確認する。変更したい場合は個別に上書き可能。

#### 3b. カスタムプロンプトの場合

従来どおり AskUserQuestion で自由入力を受け付ける。

### 4. その他パラメータ

テンプレート選択で推奨値が設定されていない場合、または変更したい場合に AskUserQuestion で入力を受ける:

| パラメータ      | 説明                                                                     | デフォルト   |
| --------------- | ------------------------------------------------------------------------ | ------------ |
| `report_format` | フォーマット（Briefing Doc / Study Guide / Blog Post / Create Your Own） | Briefing Doc |
| `source_ids`    | 対象ソース（省略で全ソース）                                             | 全ソース     |

ユーザーが「デフォルトで」「そのままで」と回答した場合はデフォルト値（またはテンプレート推奨値）を使用する。

`source_ids` を指定したい場合は、`mcp__notebooklm-mcp__source_list(notebook_id)` でソース一覧を取得して選択肢を提示する。

### 5. レポート作成

```
mcp__notebooklm-mcp__studio_create(
  notebook_id="{notebook_id}",
  artifact_type="report",
  custom_prompt="{custom_prompt}",
  report_format="{report_format}",  # デフォルト: Briefing Doc
  source_ids=["{source_id1}", "{source_id2}", ...]
)
```

指定されなかったオプションパラメータは省略する。

### 6. ポーリング（完了待ち）

以下の手順でステータスをポーリングする:

1. `mcp__notebooklm-mcp__studio_status(notebook_id="{notebook_id}")` を呼び出す
2. status を確認:
   - **完了** → `artifact_id` を取得してステップ 7 へ
   - **処理中** → Bash `sleep 15` で 15 秒待機してから再度 1 へ
   - **エラー** → ユーザーにエラー内容を報告して終了
3. 最大 6 分（ポーリング 24 回 × 15 秒）まで繰り返す
4. タイムアウトした場合はユーザーに「レポート作成がまだ完了していません。NotebookLM の Web UI で直接確認してください。」と報告する

### 7. ダウンロード/エクスポートの選択

AskUserQuestion でダウンロード方法を選択してもらう:

- **ローカルにダウンロード** — ファイルとしてダウンロード（デフォルト）
- **Google Docs にエクスポート** — Google Docs にエクスポート
- **不要** — ダウンロードしない

### 8. ダウンロード/エクスポート

選択に応じて実行する:

**ローカルダウンロードの場合:**

```
mcp__notebooklm-mcp__artifact_download(
  notebook_id="{notebook_id}",
  artifact_id="{artifact_id}"
)
```

**Google Docs エクスポートの場合:**

```
mcp__notebooklm-mcp__artifact_export(
  notebook_id="{notebook_id}",
  artifact_id="{artifact_id}",
  export_type="docs"
)
```

結果（ファイルパスまたは Google Docs URL）をユーザーに表示する。

## 注意事項

- notebooklm-mcp MCP サーバーが起動していない場合、ToolSearch でツールが見つからない。その場合は MCP サーバーの設定確認を案内する
- 認証エラーの場合は `mcp__notebooklm-mcp__refresh_auth` での再認証を案内する
- ノートブックにソースが存在しない場合、レポート作成が失敗する可能性がある。事前にソースの有無を確認すること
- レポートはテキストベースのため、スライドやインフォグラフィックと異なりダウンロード形式の選択はない（デフォルトで Markdown/テキスト形式）
- Google Docs へのエクスポートにより、後からの編集・共有が容易になる
