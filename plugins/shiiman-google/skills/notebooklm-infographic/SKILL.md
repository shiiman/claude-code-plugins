---
name: shiiman-google:notebooklm-infographic
description: NotebookLM でインフォグラフィックを作成する。「インフォグラフィック作成」「インフォグラフィック」「NotebookLM 図解」「ノートブック インフォグラフィック」「図を作って」「ビジュアル化」「NotebookLM 視覚化」などで起動。notebooklm-mcp を使用。
argument-hint: "[--help]"
---

# NotebookLM Infographic

NotebookLM のノートブックからインフォグラフィックを作成する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-google:notebooklm-infographic - NotebookLM Infographic

概要:
  ノートブックのソースからインフォグラフィックを作成します。

使用方法:
  /shiiman-google:notebooklm-infographic [オプション]

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
2. AskUserQuestion でソースとなるテキスト内容を質問する（インフォグラフィック化したい情報を入力してもらう）
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

| ID           | 名前                   | 説明                                   | 推奨 orientation | 推奨 detail_level |
| ------------ | ---------------------- | -------------------------------------- | ---------------- | ----------------- |
| `summary`    | 要約・概要             | ソース全体の要点を図解にまとめる       | landscape        | standard          |
| `comparison` | 比較・対比             | 複数の対象を並べて特徴・メリデメを比較 | landscape        | detailed          |
| `timeline`   | タイムライン・プロセス | 時系列の流れやステップを順序立てて図解 | landscape        | standard          |
| `statistics` | 統計・データ           | 数値データやトレンドをビジュアル化     | portrait         | detailed          |

**テンプレート一覧（グループ 2）:**

| ID           | 名前               | 説明                                   | 推奨 orientation | 推奨 detail_level |
| ------------ | ------------------ | -------------------------------------- | ---------------- | ----------------- |
| `list`       | リスト・ランキング | 項目を順位や重要度順に整理して一覧化   | portrait         | standard          |
| `flowchart`  | フローチャート     | 意思決定やプロセスの分岐を視覚化       | landscape        | detailed          |
| `hierarchy`  | 階層・構造         | 組織図・分類・ピラミッド等の階層を図解 | portrait         | standard          |
| `geographic` | 地理・マップ       | 地域ごとのデータや位置関係を地図で表現 | landscape        | detailed          |

AskUserQuestion で 4 つずつ選択肢を提示する（AskUserQuestion は最大 4 選択肢のため、2 回に分けて表示）。

1 回目: summary, comparison, timeline, statistics
2 回目（1 回目で「他のテンプレートを見る」を選んだ場合）: list, flowchart, hierarchy, geographic

選択されたテンプレートの `.md` ファイルを Read で読み込み:

- frontmatter の `orientation` と `detail_level` を推奨値として自動設定
- body 部分を `custom_prompt` として使用

推奨値をユーザーに提示し、「このパラメータで作成しますか？」と確認する。変更したい場合は個別に上書き可能。

#### 3b. カスタムプロンプトの場合

従来どおり AskUserQuestion で自由入力を受け付ける。

### 4. その他パラメータ

テンプレート選択で推奨値が設定されていない場合、または変更したい場合に AskUserQuestion で入力を受ける:

| パラメータ     | 説明                                    | デフォルト |
| -------------- | --------------------------------------- | ---------- |
| `orientation`  | 向き（landscape / portrait / square）   | landscape  |
| `detail_level` | 詳細度（concise / standard / detailed） | standard   |
| `source_ids`   | 対象ソース（省略で全ソース）            | 全ソース   |

ユーザーが「デフォルトで」「そのままで」と回答した場合はデフォルト値（またはテンプレート推奨値）を使用する。

`source_ids` を指定したい場合は、`mcp__notebooklm-mcp__source_list(notebook_id)` でソース一覧を取得して選択肢を提示する。

### 5. インフォグラフィック作成

```
mcp__notebooklm-mcp__studio_create(
  notebook_id="{notebook_id}",
  artifact_type="infographic",
  custom_prompt="{custom_prompt}",
  orientation="{orientation}",
  detail_level="{detail_level}",
  source_ids=["{source_id1}", "{source_id2}", ...]
)
```

指定されなかったオプションパラメータは省略する。

### 6. 初回待機

インフォグラフィック生成のため、まず 1 分待機する。

```bash
sleep 60
```

### 7. ポーリング（完了待ち）

以下の手順でステータスをポーリングする:

1. `mcp__notebooklm-mcp__studio_status(notebook_id="{notebook_id}")` を呼び出す
2. status を確認:
   - **完了** → `artifact_id` を取得してステップ 8 へ
   - **処理中** → Bash `sleep 30` で 30 秒待機してから再度 1 へ
   - **エラー** → ユーザーにエラー内容を報告して終了
3. 最大 6 分（初回 1 分 + ポーリング 10 回 × 30 秒）まで繰り返す
4. タイムアウトした場合はユーザーに「インフォグラフィック作成がまだ完了していません。NotebookLM の Web UI で直接確認してください。」と報告する

### 8. ダウンロード確認

AskUserQuestion でダウンロードするか確認する。

### 9. ダウンロード

ユーザーが「はい」の場合:

```
mcp__notebooklm-mcp__artifact_download(
  notebook_id="{notebook_id}",
  artifact_id="{artifact_id}"
)
```

結果（ファイルパス）をユーザーに表示する。

## 注意事項

- notebooklm-mcp MCP サーバーが起動していない場合、ToolSearch でツールが見つからない。その場合は MCP サーバーの設定確認を案内する
- 認証エラーの場合は `mcp__notebooklm-mcp__refresh_auth` での再認証を案内する
- ノートブックにソースが存在しない場合、インフォグラフィック作成が失敗する可能性がある。事前にソースの有無を確認すること
