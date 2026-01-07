# List

プロジェクトの Claude Code リソース一覧を表示します。

## 使い方

```bash
/shiiman-claude:list
/shiiman-claude:list --commands
/shiiman-claude:list --skills
/shiiman-claude:list --agents
/shiiman-claude:list --hooks
/shiiman-claude:list --help
```

## オプション

| オプション | 説明 |
|------------|------|
| `--help` | このコマンドのヘルプを表示 |
| `--commands` | コマンドのみ表示 |
| `--skills` | スキルのみ表示 |
| `--agents` | エージェントのみ表示 |
| `--hooks` | フックのみ表示 |
| （なし） | すべて表示 |

## Claude への指示

**`--help` が指定された場合**: このファイルの内容を要約して表示し、終了。

### 実行手順

1. オプションに応じて表示対象を決定
2. 以下のリソースを収集:
   - **コマンド**: `.claude/commands/` 配下の `.md` ファイル
   - **スキル**: `.claude/skills/` 配下のディレクトリ（`SKILL.md` を含む）
   - **エージェント**: `.claude/agents/` 配下の `.md` ファイル
   - **フック**: `.claude/settings.json` と `.claude/settings.local.json` の `hooks` セクション
3. 各リソースの説明を取得（ファイル冒頭から抽出）
4. 整形して表示

### 出力フォーマット

```markdown
## プロジェクトリソース一覧

### コマンド (2)

| コマンド | 説明 |
|----------|------|
| /my-command | カスタムコマンドの説明 |
| /deploy | デプロイコマンドの説明 |

### スキル (1)

| スキル | 説明 |
|--------|------|
| my-skill | カスタムスキルの説明 |

### エージェント (1)

| エージェント | 説明 |
|--------------|------|
| reviewer | コードレビューエージェント |

### フック (3)

| イベント | 件数 |
|----------|------|
| PreToolUse | 1 |
| PostToolUse | 2 |
```

### 説明の取得方法

- **コマンド/エージェント**: ファイル冒頭の `# タイトル` の次の段落
- **スキル**: `SKILL.md` の `description` フィールドまたは冒頭の説明

### 重要な注意事項

- ✅ 存在しないディレクトリはスキップ
- ✅ 各リソースタイプの件数を表示
- ✅ リソースがない場合は「なし」と表示
- ❌ ファイル内容の詳細は表示しない（一覧のみ）
