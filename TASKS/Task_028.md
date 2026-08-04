

# Task 028

## タイトル

結果画面に正答率を表示する

---

## 目的

ResultScreenに、回答数と正解数に加えて正答率を表示できるようにする。

Task026で実装した正解数算出と、Task027で整備した結果画面を利用し、ゲーム結果をより分かりやすくする。

---

## 背景

Task026で、回答履歴とQuestionの正解情報を比較し、正解数を算出できるようになった。

Task027で、ResultScreenに各Questionごとの回答結果一覧を表示できるようになった。

現在は `回答数: 3件` と `正解数: 1問` は表示されるが、正答率は表示されていない。

本Taskでは、ResultScreenに正答率を追加する。

---

## 前提条件

- Task027が完了していること
- ResultScreenに回答数が表示されていること
- ResultScreenに正解数が表示されていること
- ResultScreenに回答結果一覧が表示されていること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- ResultScreenで正答率を算出する
- ResultScreenに正答率を表示する
- 既存の回答数表示を維持する
- 既存の正解数表示を維持する
- 既存の回答結果一覧を維持する

---

## 変更対象

- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
- QuestionScreen
- main.dart
- Questionモデル
- AnswerRecordモデル
- QuestionRepository
- ChartCard
- AnswerButton
- Pythonコード
- API通信
- FastAPI
- yfinance
- 実チャート表示
- 外部パッケージ
- チャート解説表示
- ランク表示
- 点数表示

---

## ResultScreen仕様

ResultScreenで正答率を算出する。

正答率は以下の式で算出する。

```text
正答率 = 正解数 ÷ 回答数 × 100
```

小数点以下は表示しない。

表示形式は以下とする。

```text
正答率: 33%
```

回答数が0件の場合は、0%として扱う。

---

## 表示仕様

既存の以下表示は維持する。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- `回答数: x件`
- `正解数: y問`
- 回答結果一覧
- `ホームへ戻る`

正答率は、正解数の下に表示する。

表示順は以下とする。

```text
回答数: 3件
正解数: 1問
正答率: 33%
```

---

## 操作仕様

操作仕様はTask027から変更しない。

- 回答ボタンを押すと次のQuestionへ進む
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenからHomeScreenへ戻れる

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenに `回答数: 3件` が表示される
- ResultScreenに `正解数: 1問` が表示される
- ResultScreenに `正答率: 33%` が表示される
- ResultScreenに回答結果一覧が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## テスト前提

Widgetテストでは、Task027と同じく以下の回答を行う。

- Question 1: `Chart A`
- Question 2: `現金保有`
- Question 3: `現金保有`

QuestionRepositoryの正解は以下である。

- Question 1: `Chart A`
- Question 2: `Chart B`
- Question 3: `Chart C`

そのため、期待される結果は以下とする。

- 回答数: 3件
- 正解数: 1問
- 正答率: 33%
- Q1: 正解
- Q2: 不正解
- Q3: 不正解

---

## 受け入れ条件

- ResultScreenに正答率が表示されている
- 正答率が正解数と回答数から算出されている
- 小数点以下が表示されていない
- 既存の回答数表示が維持されている
- 既存の正解数表示が維持されている
- 既存の回答結果一覧が維持されている
- 既存のゲーム進行が壊れていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- ゲーム開始
- `Question 1 / 10` 表示
- `Chart A` を選択
- `Question 2 / 10` 表示
- `現金保有` を選択
- `Question 3 / 10` 表示
- `現金保有` を選択
- ResultScreen表示
- `回答数: 3件` 表示
- `正解数: 1問` 表示
- `正答率: 33%` 表示
- 回答結果一覧が表示される
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push