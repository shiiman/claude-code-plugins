---
name: shiiman-google:notebooklm-slide
description: NotebookLM でスライドデッキを作成する。「NotebookLM スライド」「NotebookLM スライドデッキ」「NotebookLM プレゼン」「NotebookLM デッキ」などで起動。notebooklm-mcp を使用。
argument-hint: "[--help]"
---

# NotebookLM Slide Deck

NotebookLM のノートブックからスライドデッキを作成する。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-google:notebooklm-slide - NotebookLM Slide Deck

概要:
  ノートブックのソースからスライドデッキを作成します。

使用方法:
  /shiiman-google:notebooklm-slide [オプション]

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
2. AskUserQuestion でソースとなるテキスト内容を質問する（スライド化したい情報を入力してもらう）
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

| ID           | 名前                       | 説明                                         | 推奨 deck_format | 推奨 deck_length |
| ------------ | -------------------------- | -------------------------------------------- | ---------------- | ---------------- |
| `summary`    | 要約・概要                 | ソース全体の要点をスライドにまとめる         | presenter_slides | default          |
| `comparison` | 比較・対比                 | 複数の対象を並べて特徴・メリデメを比較       | detailed_deck    | default          |
| `timeline`   | タイムライン・ロードマップ | 時系列の流れやマイルストーンをスライドで表現 | presenter_slides | default          |
| `report`     | 報告・レポート             | 調査結果やステータスを報告するスライド       | detailed_deck    | default          |

**テンプレート一覧（グループ 2）:**

| ID         | 名前           | 説明                                         | 推奨 deck_format | 推奨 deck_length |
| ---------- | -------------- | -------------------------------------------- | ---------------- | ---------------- |
| `pitch`    | ピッチ・提案   | 企画提案やビジネスプレゼン向けスライド       | presenter_slides | short            |
| `training` | 研修・教育     | トレーニングや学習用のスライド               | detailed_deck    | default          |
| `analysis` | 分析・考察     | データ分析や深堀り考察をまとめるスライド     | detailed_deck    | default          |
| `guide`    | ガイド・手順書 | ステップバイステップの手順を説明するスライド | presenter_slides | default          |

AskUserQuestion で 4 つずつ選択肢を提示する（AskUserQuestion は最大 4 選択肢のため、2 回に分けて表示）。

1 回目: summary, comparison, timeline, report
2 回目（1 回目で「他のテンプレートを見る」を選んだ場合）: pitch, training, analysis, guide

選択されたテンプレートの `.md` ファイルを Read で読み込み:

- frontmatter の `deck_format` と `deck_length` を推奨値として自動設定
- body 部分を `custom_prompt` として使用

推奨値をユーザーに提示し、「このパラメータで作成しますか？」と確認する。変更したい場合は個別に上書き可能。

#### 3b. カスタムプロンプトの場合

従来どおり AskUserQuestion で自由入力を受け付ける。

### 4. その他パラメータ

テンプレート選択で推奨値が設定されていない場合、または変更したい場合に AskUserQuestion で入力を受ける:

| パラメータ    | 説明                                             | デフォルト       |
| ------------- | ------------------------------------------------ | ---------------- |
| `deck_format` | フォーマット（presenter_slides / detailed_deck） | presenter_slides |
| `deck_length` | 長さ（short / default）                          | default          |
| `source_ids`  | 対象ソース（省略で全ソース）                     | 全ソース         |

ユーザーが「デフォルトで」「そのままで」と回答した場合はデフォルト値（またはテンプレート推奨値）を使用する。

`source_ids` を指定したい場合は、`mcp__notebooklm-mcp__source_list(notebook_id)` でソース一覧を取得して選択肢を提示する。

### 5. スライドデッキ作成

```
mcp__notebooklm-mcp__studio_create(
  notebook_id="{notebook_id}",
  artifact_type="slide_deck",
  custom_prompt="{custom_prompt}",
  deck_format="{deck_format}",  # デフォルト: presenter_slides
  deck_length="{deck_length}",
  source_ids=["{source_id1}", "{source_id2}", ...]
)
```

指定されなかったオプションパラメータは省略する。

### 6. 初回待機

スライドデッキ生成のため、まず 5 分待機する。

```bash
sleep 300
```

### 7. ポーリング（完了待ち）

以下の手順でステータスをポーリングする:

1. `mcp__notebooklm-mcp__studio_status(notebook_id="{notebook_id}")` を呼び出す
2. status を確認:
   - **完了** → `artifact_id` を取得してステップ 8 へ
   - **処理中** → Bash `sleep 60` で 1 分待機してから再度 1 へ
   - **エラー** → ユーザーにエラー内容を報告して終了
3. 最大 20 分（初回 5 分 + ポーリング 15 回 × 1 分）まで繰り返す
4. タイムアウトした場合はユーザーに「スライドデッキ作成がまだ完了していません。NotebookLM の Web UI で直接確認してください。」と報告する

### 8. ダウンロード形式の選択

AskUserQuestion でダウンロード形式を選択してもらう:

- **PDF でダウンロード** — PDF ファイルとしてダウンロード（デフォルト）
- **PPTX でダウンロード** — PowerPoint ファイルとしてダウンロード
- **不要** — ダウンロードしない

### 9. ダウンロード

選択に応じて実行する:

**PDF ダウンロードの場合:**

```
mcp__notebooklm-mcp__artifact_download(
  notebook_id="{notebook_id}",
  artifact_id="{artifact_id}",
  file_format="pdf"
)
```

**PPTX ダウンロードの場合:**

```
mcp__notebooklm-mcp__artifact_download(
  notebook_id="{notebook_id}",
  artifact_id="{artifact_id}",
  file_format="pptx"
)
```

結果（ファイルパス）をユーザーに表示する。

## 注意事項

- notebooklm-mcp MCP サーバーが起動していない場合、ToolSearch でツールが見つからない。その場合は MCP サーバーの設定確認を案内する
- 認証エラーの場合は `mcp__notebooklm-mcp__refresh_auth` での再認証を案内する
- ノートブックにソースが存在しない場合、スライドデッキ作成が失敗する可能性がある。事前にソースの有無を確認すること
- 既存の `shiiman-google:slides` は Google Slides API を直接操作するスキル。本スキルは NotebookLM のソースから AI でスライドを生成する別機能
