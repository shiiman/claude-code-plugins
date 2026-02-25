# notebooklm-mcp 問題点まとめ

`notebooklm-deepresearch` スキルのテスト中に発見された notebooklm-mcp の問題点。

テスト日: 2026-02-25

## 1. `research_poll` のステータスが `completed` にならない

### 事象

`research_start` で deep research を開始後、`research_poll` を繰り返しても `status` が `"running"` のまま `"completed"` にならない。
NotebookLM の Web UI 上ではリサーチが完了しレポートとソース一覧が表示されている状態でも、API は `running` を返し続ける。

### 詳細

```json
{
  "status": "running",
  "task_id": "10a80ed0-...",
  "sources": [],
  "report": null,
  "raw": [
    [
      /* レポートID, [notebook_id, query, status_code=5, report_data, ...], timestamps, task_metadata */
    ]
  ]
}
```

- `raw` フィールド内にはレポート本文（45 件のソースを含む完全なレポート）が存在する
- しかし `status` は `"running"`、`sources` は空リスト `[]`、`report` は `null`
- `raw` 内の `inner[2]` が `5` であり、これが「完了」を示すステータスコードの可能性がある

### 影響

- ポーリングループが完了判定できず、最大待機時間までループし続ける
- `sources` が空のため、後続の `research_import` でインポート対象が見つからない

### 想定される原因

`research_poll` のレスポンスパーサーが deep research（`mode="deep"`）の raw レスポンス構造を正しく解釈できていない可能性がある。raw データ内にはステータスコード `5`（完了?）やソースリストが存在するが、パーサーがこれを `status: "completed"` や `sources: [...]` にマッピングできていない。

---

## 2. `research_poll` の `task_id` が notebook_id を返す

### 事象

`research_poll` のレスポンスの `task_id` フィールドが、`research_start` で返された実際の `task_id` ではなく `notebook_id` を返す。

### 詳細

| フィールド                    | 期待値                                 | 実際の値                                  |
| ----------------------------- | -------------------------------------- | ----------------------------------------- |
| `research_start` の `task_id` | `805eb230-e964-44d6-b5be-b167f05a2082` | `805eb230-e964-44d6-b5be-b167f05a2082`    |
| `research_poll` の `task_id`  | `805eb230-e964-44d6-b5be-b167f05a2082` | `10a80ed0-...`（= notebook_id）           |
| `raw` 内の実際の task_id      | -                                      | `805eb230-e964-44d6-b5be-b167f05a2082` ✅ |

- `raw[0][1][5][0]` に正しい task_id が格納されているが、トップレベルの `task_id` には `notebook_id` が返される

### 影響

- `research_poll` の `task_id` を使って `research_import` を呼ぶと notebook_id を渡すことになり、タスクが見つからずエラーになる
- ただし `research_start` の戻り値の `task_id` を保持していれば回避可能（問題 3 参照）

---

## 3. `research_import` でタスクが見つからない

### 事象

`research_start` が返した `task_id` を `research_import` に渡しても `"タスク {task_id} が見つかりません"` エラーが返る。

### 詳細

```
research_import(notebook_id="10a80ed0-...", task_id="805eb230-...")
→ {"error": "タスク 805eb230-... が見つかりません"}

research_import(notebook_id="10a80ed0-...", task_id="fcb5227c-...")  # report_id
→ {"error": "タスク fcb5227c-... が見つかりません"}

research_import(notebook_id="10a80ed0-...", task_id="10a80ed0-...")  # notebook_id
→ {"status": "no_importable_sources", "total_sources": 0}
```

### 影響

- ディープリサーチの結果をプログラム的にインポートできない
- ユーザーは NotebookLM の Web UI で手動インポートする必要がある

### 想定される原因

問題 1 と関連。`research_poll` が `sources` を空リストで返すため、`research_import` 内部でもインポート対象ソースを取得できていない可能性がある。または `research_import` が deep research のタスク管理方式に対応していない可能性がある。

---

## 4. `research_poll` の結果が大量（602KB）で MCP レスポンス上限を超える

### 事象

`research_poll` の戻り値が 602,484 文字に達し、MCP のレスポンスサイズ上限を超えてファイルに保存される。

### 詳細

- `raw` フィールドにレポート本文全体（Markdown 形式、45 ソース分）が含まれる
- Claude Code 側でレスポンスを直接処理できず、ファイルから読み込む必要がある

### 影響

- スキルワークフロー内で poll 結果を直接利用できず、Bash + jq/python 等での間接処理が必要になる
- ポーリングの度にこの大量データが返されるため、無駄なデータ転送が発生する

### 改善提案

- `research_poll` はステータスとソースリスト（URL + タイトルのみ）を返し、レポート本文は別ツール（例: `research_report`）で取得する設計が望ましい
- または `raw` フィールドを省略するオプションを追加する

---

## まとめ

| #   | 問題                                   | 重要度 | ワークアラウンド                 |
| --- | -------------------------------------- | ------ | -------------------------------- |
| 1   | poll の status が completed にならない | 高     | raw 内の status code で判定      |
| 2   | poll の task_id が notebook_id を返す  | 中     | research_start の task_id を保持 |
| 3   | research_import でタスクが見つからない | 高     | Web UI で手動インポート          |
| 4   | poll レスポンスが 600KB 超で上限超過   | 中     | ファイル経由で jq/python で処理  |

問題 1〜3 は相互に関連しており、根本原因は `research_poll` のレスポンスパーサーが deep research の raw レスポンス構造に対応していないことと推測される。
