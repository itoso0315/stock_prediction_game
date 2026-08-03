
# Coding Style

## 基本方針

- 可読性を最優先する
- シンプルな実装を選ぶ
- Taskの仕様を最優先する
- 推測で機能を追加しない

---

## Dart / Flutter

### 命名

- クラス名：UpperCamelCase
- メソッド・変数：lowerCamelCase
- 定数：lowerCamelCase を基本とする
- ファイル名：snake_case

---

## Widget設計

- 1つのWidgetにつき1つの責務
- 再利用できるUIは widgets/ に分離する
- 画面全体は screens/ に配置する
- データ構造は models/ に配置する
- StatelessWidget を優先し、状態が必要な場合のみ StatefulWidget を利用する

---

## コード品質

- const を利用できる箇所では積極的に利用する
- 不要なコメントを書かない
- コメントは「なぜ」を説明する場合のみ追加する
- マジックナンバーは避け、意味のある定数にする
- 同じコードを繰り返さない

---

## Material Design

- Material3 を利用する
- Theme を優先し、色のハードコードは最小限にする
- 標準Widgetを優先して利用する

---

## テスト

実装後は必ず以下を実行する。

- dart format .
- flutter analyze
- flutter test

すべて成功してから完了報告する。

---

## 禁止事項

- Taskにない機能を追加しない
- 指定外ファイルを編集しない
- 外部パッケージを勝手に追加しない
- Python側を勝手に変更しない
- 大規模リファクタリングを勝手に行わない