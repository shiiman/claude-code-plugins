# Skill 作成ガイド

このガイドでは、Claude Code Skills の作成方法を説明します。

## 概要

Skills は、特定のドメインや作業フローに特化した知識と手順を提供する仕組みです。コマンドとは異なり、ユーザーの自然な会話から Claude が自動的に適切な Skill を起動し、最適な手順を実行します。

## Skills とコマンドの使い分け

### 基本的な違い

| 観点                       | Skills                                              | Slash Commands                       |
| -------------------------- | --------------------------------------------------- | ------------------------------------ |
| **起動方法**               | Model-Invoked (Claude が自動判断)                   | User-Invoked (明示的に `/command`)   |
| **発見方法**               | description フィールドでコンテキストマッチ          | コマンド名を直接入力                 |
| **使用例**                 | 「コードレビューして」→ 自動的にレビュー Skill 起動 | `/review` と明示的に入力             |
| **適用場面**               | 自然な対話で自動的に機能を適用したい                | 特定のプロンプトを再利用可能にしたい |
| **構成要素**               | SKILL.md + scripts/ + references/ + assets/         | 単一の Markdown ファイル             |
| **Progressive Disclosure** | ✅ 段階的なリソース読み込み                         | ❌ なし                              |
| **リッチな文脈**           | ✅ スクリプト、参照資料、テンプレート等を含められる | ❌ プロンプトテキストのみ            |

**重要な概念**:

Skills とコマンドの最大の違いは起動方法です：

- **Model-Invoked (Skills)**: Claude がユーザーの自然な会話から自律的に適切な Skill を判断して起動
- **User-Invoked (Commands)**: ユーザーが `/command` 形式で明示的に呼び出す

### 使い分けの原則

**Skills を使う場合**:

- 自然な会話で Claude に機能を発見してほしい
- 複雑な多段階ワークフローがある
- スクリプトやリファレンスなどの補助資料が必要
- バンドルされたリソース（テンプレート、参照資料）を活用したい
- Progressive Disclosure でコンテキストを効率管理したい
- 例：「このコードをレビューして」→ レビュー Skill が自動起動

**Slash Commands を使う場合**:

- 明示的な制御が必要
- 頻繁に使う定型プロンプトを再利用したい
- シンプルな 1 ステップのタスク
- 補助資料が不要
- 例：`/commit` でコミットメッセージ生成

## 配置場所

```text
plugins/{plugin-name}/skills/{skill-name}/SKILL.md
```

## scripts パス規約（プラグイン内）

scripts の標準配置は Skill 配下です。複数 Skill で共通利用する場合のみ plugin ルートに配置します。

- 標準配置: `plugins/{plugin-name}/skills/{skill-name}/scripts/{script-file}`
- 標準呼び出し: `${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/scripts/{script-file}`
- 共通配置: `plugins/{plugin-name}/scripts/{script-file}`
- 共通呼び出し: `${CLAUDE_PLUGIN_ROOT}/scripts/{script-file}`
- 共通化の運用基準: 2 つ以上の `SKILL.md` から参照される script を plugin ルートへ集約

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/example-skill/scripts/helper-script.py" --help
python "${CLAUDE_PLUGIN_ROOT}/scripts/shared-helper.py" --help
```

## ディレクトリ構造

```text
plugins/{plugin-name}/skills/{skill-name}/
├── SKILL.md                 # 必須
├── LICENSE.txt              # 推奨
├── reference.md             # オプション（単一ファイル形式）
├── references/              # オプション（ディレクトリ形式、どちらでも可）
│   ├── api-reference.md
│   └── best-practices.md
├── scripts/                 # オプション（実行可能コード）
│   └── helper-script.py
└── assets/                  # オプション（出力に使用されるファイル）
    └── template.md
```

**ファイル構造の柔軟性**:

参照資料は以下のどちらの形式でも許容されます：

- **単一ファイル**: `reference.md` - シンプルな参照資料の場合
- **ディレクトリ**: `references/*.md` - 複数の参照資料がある場合

## SKILL.md の形式

````markdown
---
name: skill-name
description: Skill の説明（最大 1024 文字）。何をするか + いつ使うか。
allowed-tools: [Read, Write, Bash]
argument-hint: "[--help]"
---

# Skill タイトル

この Skill は、[目的] を効率化します。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/skill-name - Skill タイトル

概要:
  この Skill は、[目的] を効率化します。

使用方法:
  /skill-name [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

ユーザーが「[トリガーワード]」と要求したら：

### 1. ステップ名

```bash
実行するコマンド
```

### 2. 次のステップ名

具体的な手順を記述

## 重要な注意事項

- ✅ 推奨する動作
- ❌ 禁止する動作
````

## フロントマターフィールド

| フィールド    | 必須   | 説明                                               |
| ------------- | ------ | -------------------------------------------------- |
| name          | はい   | スキル識別子（小文字、ハイフン、最大 64 文字）     |
| description   | はい   | トリガーフレーズを含む説明（最大 1024 文字）       |
| allowed-tools | いいえ | スキルが使用できるツール（省略時は全ツール使用可） |
| argument-hint | はい（このリポジトリ運用） | 引数ヒント。必ず `"[--help]"` を指定する            |

## `--help` 必須ルール（このリポジトリ運用）

このリポジトリで作成・更新する `SKILL.md` には、以下を必須とします。

1. frontmatter に `argument-hint: "[--help]"` を記載する
2. 本文の冒頭（タイトル・導入文の直後、最初の `##` 見出しの前）に `## Help` を置く
3. `## Help` に ``$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:`` を記載する
4. Usage は `/skill-name [オプション]` 形式で記載する

## description フィールドの書き方

**最重要**: description フィールドは Claude が Skill を自動起動するために**唯一**使用される情報源です。

### 必須要件

1. **三人称で記述**: システムプロンプトに注入されるため、一貫性が重要
2. **何をするか (what) といつ使うか (when) の両方を含める**
3. **トリガーワードを 7 つ含める**: ユーザーが使う可能性のある自然言語表現を網羅
4. **最大 1024 文字**: 簡潔に、しかし十分な情報を提供

### 構成テンプレート

```text
{機能説明}。「トリガー 1」「トリガー 2」「トリガー 3」「トリガー 4」「トリガー 5」「トリガー 6」「トリガー 7」などで起動。{詳細説明}。
```

**トリガーワードの選び方**:

- フォーマル: 「機能を実行してください」「〜を作成して」
- カジュアル: 「〜やって」「〜して」
- 具体的: 「PR を作って」「エラーを直して」
- 疑問形: 「〜できる？」「〜は？」

### 良い description の例

```yaml
# ✅ 7 つのトリガーワードを含む
description: 現在のブランチから Pull Request を作成する。「PR を作って」「プルリクエストを出したい」「PR 作成して」「プルリク出して」「このブランチで PR」「変更を PR にして」「レビュー依頼したい」などで起動。変更内容を分析し、適切な説明とラベルを自動生成。

# ✅ トリガーワードと詳細説明のバランスが良い
description: エラーメッセージから根本原因を特定し解決策を提案する。「エラーを直して」「このエラー修正して」「エラー解決して」「このエラー何？」「エラーの原因は？」「ビルドエラーを直して」「テスト失敗を解決して」などで起動。解決時間を予測し、実証済みの解決策を提示。
```

### 悪い description の例

```yaml
# ❌ 一人称（You can use...）は避ける
description: You can use this to process Excel files

# ❌ トリガーワードが不足（3 つのみ）
description: Git 操作を行います。「git を実行」「リポジトリ操作」「バージョン管理」などで起動。

# ❌ 本文に「使用タイミング」セクションを記述
# description にトリガーワードを含めるべきで、本文に記述しても自動起動には使われない
description: Git 操作を行います。
## 使用タイミング
- 「git を実行」  # ← これは無視される
```

## allowed-tools フィールド

SKILL.md の frontmatter で、Claude が使用できるツールを制限できます。

### 基本構文

```yaml
---
name: read-only-analyzer
description: コードベースを分析するが変更はしない
allowed-tools: [Read, Grep, Glob]
---
```

### 用途

- **セキュリティ**: 読み取り専用 Skills（Write, Edit を禁止）
- **制御**: 特定ツールのみ許可（例: Read, Grep のみ）
- **安全性**: 破壊的な操作を防止

### 例

**読み取り専用の分析 Skill**:

```yaml
---
name: code-analyzer
description: コードベースの品質を分析し、レポートを生成
allowed-tools: [Read, Grep, Glob, Bash]
---
```

**ドキュメント生成専用 Skill**:

```yaml
---
name: doc-generator
description: 既存コードからドキュメントを生成
allowed-tools: [Read, Glob, Write]
---
```

## リソースの使い分け

### scripts/ （実行可能コード）

確実な実行が必要なタスクや、繰り返し生成されるコードを避けたい場合に使用。

- **含めるべきとき**: 同じコードが繰り返し生成されている場合、または確実な実行が必要な場合
- **例**: PDF 回転タスク用の `scripts/rotate_pdf.py`
- **利点**: トークン効率的、決定的、コンテキストに読み込まずに実行可能

### references/ （参照資料）

Claude のプロセスと思考を支援するために、必要に応じてコンテキストに読み込まれることを想定したドキュメント。

- **含めるべきとき**: Claude が作業中に参照すべきドキュメント用
- **例**: 財務スキーマ用の `references/finance.md`、API 仕様用の `references/api_docs.md`
- **利点**: SKILL.md を簡潔に保ち、Claude が必要と判断した時のみ読み込まれる

### assets/ （出力用ファイル）

コンテキストに読み込まれることを想定していないが、Claude が生成する出力内で使用されるファイル。

- **含めるべきとき**: Skill が最終出力で使用するファイルが必要な場合
- **例**: テンプレート用の `assets/template.md`、ボイラープレート用の `assets/hello-world/`
- **利点**: 出力リソースをドキュメントから分離し、Claude がファイルをコンテキストに読み込まずに使用できる

## Progressive Disclosure 設計原則

Skills はコンテキストを効率的に管理するために 3 段階のロードシステムを使用します：

1. **Metadata (name + description)** - 常にコンテキスト内（約 100 ワード）
2. **SKILL.md 本文** - Skill がトリガーされた時（5k ワード未満推奨）
3. **Bundled resources** - Claude が必要とする時
   - **references/**: 必要に応じてコンテキストに読み込まれる
   - **scripts/**: コンテキストに読み込まずに実行可能
   - **assets/**: 出力生成時のみ使用（コンテキスト非ロード）

## Skills の実装パターン

Skills には主に 2 つの実装パターンがあります。

### 独自実装パターン

**特徴**: Skill が独自のロジックを持ち、独立して動作する。

**構造**:

```text
my-skill/
├── SKILL.md              # メインロジック
├── templates/            # 生成用テンプレート
│   └── output.md
├── scripts/              # ヘルパースクリプト
│   └── processor.py
└── references/           # 参考資料
    └── guide.md
```

**SKILL.md の構造**:

```markdown
## 実行内容

1. ユーザーから情報を収集
2. `templates/output.md` を使用してファイル生成
3. `scripts/processor.py` で処理を実行
4. 結果をユーザーに返す

## 関連ファイル

- `templates/output.md` - 生成用テンプレート
- `scripts/processor.py` - ヘルパースクリプト
- `references/guide.md` - 参考資料
```

**利点**:

- Commands に依存しない完全な独立性
- 複雑なワークフローを内包可能
- カスタムスクリプトやテンプレートを使用可能

## ベストプラクティス

### 1. 簡潔さと "Claude は既に賢い" 原則

**簡潔さが重要**:

- SKILL.md が読み込まれると、すべてのトークンが会話履歴や他のコンテキストと競合します
- 必要最小限の情報のみを記載し、冗長な説明は避けます
- 長大なワークフローや詳細なリファレンスは別ファイル（references/）に分離します

**"Claude は既に賢い" 原則**:

- デフォルトの前提として、Claude は既に一般的なプログラミング知識や開発手法を理解しています
- **Claude が既に知らない情報のみを追加する**ことが重要です
- 一般的なプログラミング知識や Git の基本操作などは記載不要です
- プロジェクト固有のルール、制約、ワークフローに焦点を当てます

### 2. ステップバイステップのワークフロー

複雑な作業は段階的な手順に分解します。

````markdown
## ワークフロー名

### 1. ステップ 1 の名前

```bash
実行するコマンド
```

### 2. ステップ 2 の名前

具体的な処理内容や SlashCommand の呼び出し

### 3. ステップ 3 の名前

確認方法や次の手順
````

### 3. 詳細情報は references/ に分離

SKILL.md には必要最小限の情報のみを記載し、詳細なコマンドリファレンスやトラブルシューティングは `references/` に分離します。

**SKILL.md（簡潔に）**:

```markdown
詳細は `references/api-reference.md` を参照。
```

**references/api-reference.md（詳細に）**:

````markdown
# API Reference

## エンドポイント一覧

### GET /api/users

```bash
curl -X GET https://api.example.com/users
```

...
````

### 4. Slash Commands との連携

Skill 内で Slash Commands を使用する場合、**Slash Commands をシングルソースオブトゥルース（SSOT）** として扱います。

**✅ 良い例（SlashCommand ツールで委譲）**:

```markdown
## コミット処理

SlashCommand ツールで `/commit` を実行：

- 変更を論理的な単位に分割
- Conventional Commits 形式でコミットメッセージを生成

詳細は `/commit` のドキュメントを参照。
```

**❌ 悪い例（ロジックを重複記述）**:

````markdown
## コミット処理

```bash
# ❌ Slash Commands と同じロジックを再実装している
git diff --staged
# コミットメッセージを生成...
git commit -m "..."
```
````

## Skill のテストとデバッグ

### 1. 実タスクでのテスト（最重要）

**テストシナリオではなく、実際の業務タスクで Skill を使用してください**:

- ❌ 悪い例: 「この Skill をテストして」と依頼する
- ✅ 良い例: 「この PR をレビューして」と実際の作業を依頼する

**観察すべきポイント**:

- Claude がどこで苦労するか
- どこで成功するか
- 予想外の選択をする箇所

**反復改善**:

- Claude の振る舞いを観察し、SKILL.md を調整
- 実タスクを繰り返しながら Skill を洗練

### 2. Skill の読み込み確認

Skill を作成したら、Claude Code で実際に起動してみます：

```bash
# ユーザーが実際に発言するトリガーワードを試す
「spec を作成して」
「コードレビューして」
```

Skill が正常に起動すると、システムメッセージ `The "skill-name" skill is running` が表示されます。

### 3. ワークフローの検証

各ワークフローが正しく動作するか確認します：

- コマンドが正しく実行されるか
- エラーハンドリングが適切か
- プロジェクトルールが守られているか

## トラブルシューティング

### Skills が起動しない場合

**description の具体性を確認**:

- ❌ 悪い例: `"ドキュメント処理を支援"`
- ✅ 良い例: `"PDF ファイルからテキストとテーブルを抽出し、構造化されたマークダウンに変換する"`

**ファイルパスと YAML 構文を確認**:

```bash
# SKILL.md の frontmatter が正しいか確認
cat plugins/{plugin-name}/skills/{skill-name}/SKILL.md
```

**ファイルの存在を確認**:

```bash
# ディレクトリ構造を確認
ls -la plugins/{plugin-name}/skills/{skill-name}/
```

**デバッグモード**:

```bash
# 詳細なログで読み込みエラーを確認
claude --debug
```

### Progressive Disclosure が機能しない場合

**SKILL.md からの明示的な参照**:

```markdown
詳細は `references/api-reference.md` を参照してください。
```

**ファイル名の明確化**:

Claude が必要と判断できるよう、分かりやすいファイル名を使用：

- ✅ `references/api-specification.md`
- ✅ `references/best-practices.md`
- ❌ `references/misc.md`

### Skill が期待通りに動作しない場合

**実タスクで検証**:

- テストシナリオではなく、実際の業務タスクで Skill を使用
- Claude がどこで苦労するか観察
- SKILL.md の手順を調整

## Skill を作成すべきタイミング

以下の場合に Skill の作成を検討します：

1. **繰り返し行う複雑なワークフローがある**
   - 例：要件分析 → 設計 → 実装計画の 3 段階プロセス

2. **プロジェクト固有のルールや制約がある**
   - 例：「特定のコマンド直接実行禁止、wrapper 経由で実行」

3. **自然な会話で機能を呼び出したい**
   - 例：「spec を作成して」と言うだけで 3 段階プロセスを実行

4. **補助資料やスクリプトが必要**
   - 例：EARS 記法リファレンス、テンプレートファイル

5. **複数の関連機能をまとめたい**
   - 例：要件定義、設計、実装計画を 1 つの Skill に

## 命名規則

### Skill 特有の制約

- **name フィールド**: 小文字、数字、ハイフン（`a-z`, `0-9`, `-`）のみ、最大 64 文字
- **ディレクトリ名**: kebab-case、name フィールドと一致させる
- **プラグイン名をプレフィックスに含めない**: `lister` ✅ / `plugin-lister` ❌

### 命名パターン

```bash
# 名詞形（ツールや機能を表現）
commit-helper
code-reviewer
pdf-processing

# 複合語
github-pr-manager
spec-driven-dev
```

### ファイル名

- `SKILL.md`: 必須（大文字）
- `references/*.md`: オプション（小文字）
- `scripts/*.py`: オプション（小文字）
- `assets/*`: オプション（小文字）

## よくある質問

### Q: 1 つの Skill に複数のワークフローを含めるべき？

**A**: 関連性の高いワークフローは 1 つの Skill にまとめます。

**良い例**: spec-driven-development Skill に「要件定義」「設計」「実装計画」を含める
**悪い例**: spec-driven-development Skill に「データベースマイグレーション」を含める

### Q: references/ は必須？

**A**: 推奨ですが必須ではありません。詳細なリファレンスやベストプラクティス集が必要な場合に作成します。

簡潔な Skill であれば SKILL.md のみでも十分です。

### Q: プラグインと Skill の関係は？

**A**: プラグインは Skill を含むことができます。

```text
plugins/{plugin-name}/
├── skills/
│   └── {skill-name}/
│       └── SKILL.md
└── agents/
```

## 実装例

ファイル: `plugins/shiiman-git/skills/git-commit/SKILL.md`

````markdown
---
name: shiiman-git:git-commit
description: 変更をコミットしてプッシュする。「コミット」「コミットして」「変更をコミット」「プッシュして」「commit して」「git commit」「コミットしたい」などで起動。差分を分析し適切なコミットメッセージを生成。
argument-hint: "[--help]"
---

# git-commit

変更をコミットしてプッシュします。

## Help

`$ARGUMENTS` に `--help` が含まれる場合、以下を表示して終了:

```text
/shiiman-git:git-commit - git-commit

概要:
  変更をコミットしてプッシュします。

使用方法:
  /shiiman-git:git-commit [オプション]

オプション:
  --help  このヘルプを表示
```

## ワークフロー

### 1. 変更確認

```bash
git status --short --branch
git diff
git diff --cached
```

### 2. コミット対象の選定

変更内容を分析し、コミットに含めるファイルを決定。

### 3. コミット＆プッシュ

- Conventional Commits 形式でメッセージを生成
- `git add` → `git commit` → `git push`

## 重要な注意事項

- ✅ Conventional Commits 形式を使用
- ✅ `--no-verify` は絶対に使わない
- ❌ デフォルトブランチへの直接プッシュは禁止
````

## 参考資料

公式ドキュメント:

- [Claude Code Skills 公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Slash Commands vs Skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Claude Code Plugins 公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Anthropic Skills リポジトリ](https://github.com/anthropics/skills)
