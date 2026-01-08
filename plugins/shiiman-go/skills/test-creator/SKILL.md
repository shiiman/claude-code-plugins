# Test Creator

Go のテストコードを自動生成するスキル。

## トリガー

- 「テストを作って」「テスト追加」「〇〇のテストを書いて」
- 「テストケース追加」「単体テスト作成」「テストコード生成」「テストを生成」

## 実行内容

1. 対象ファイル/関数を特定
2. 既存のテストパターンを確認
3. テーブル駆動テストでテストコード生成
4. t.Parallel() を適用（独立したテストの場合）

## Claude への指示

### 実行手順

1. **対象の特定**

   ユーザーの指定から対象ファイル/関数を特定:
   - ファイル名が指定されていれば、そのファイルの関数をテスト
   - 関数名が指定されていれば、その関数をテスト
   - 指定がなければ、最近変更されたファイルを確認

2. **既存パターンの確認**

   ```bash
   # 既存のテストファイルを確認
   ls *_test.go 2>/dev/null || ls **/*_test.go 2>/dev/null | head -5
   ```

   確認項目:
   - テーブル駆動テストの使用有無
   - testify の使用有無
   - t.Parallel() の使用パターン
   - 命名規則

3. **テストコード生成**

   以下のベストプラクティスに従って生成:

   ```go
   func TestFunctionName(t *testing.T) {
       t.Parallel() // 独立したテストの場合

       tests := []struct {
           name     string
           input    InputType
           expected OutputType
           wantErr  bool
       }{
           {
               name:     "正常系: 基本的な入力",
               input:    InputType{...},
               expected: OutputType{...},
               wantErr:  false,
           },
           {
               name:     "異常系: 空の入力",
               input:    InputType{},
               expected: OutputType{},
               wantErr:  true,
           },
       }

       for _, tt := range tests {
           t.Run(tt.name, func(t *testing.T) {
               t.Parallel() // サブテストも並行実行

               got, err := FunctionName(tt.input)

               if (err != nil) != tt.wantErr {
                   t.Errorf("FunctionName() error = %v, wantErr %v", err, tt.wantErr)
                   return
               }
               if !reflect.DeepEqual(got, tt.expected) {
                   t.Errorf("FunctionName() = %v, want %v", got, tt.expected)
               }
           })
       }
   }
   ```

4. **テスト実行確認**

   ```bash
   go test -v -run TestFunctionName ./path/to/package
   ```

### テストケース設計

| カテゴリ | 内容 |
|----------|------|
| 正常系 | 基本的な入力、境界値 |
| 異常系 | 無効な入力、nil、空値 |
| エッジケース | 最大値、最小値、特殊文字 |

### 出力形式

```
## テストコード生成完了

### 対象
- ファイル: {ファイル名}
- 関数: {関数名}

### 生成したテスト
- ファイル: {テストファイル名}
- テストケース数: {N}件

### テスト実行結果
{go test の出力}
```
