

# Task 027

## タイトル

結果画面に回答結果一覧を表示する

---

## 目的

ResultScreenに、各Questionごとの回答結果を一覧表示できるようにする。

Task026で実装した正誤判定を利用し、ユーザーがどの問題で何を選び、それが正解だったかを確認できる基盤を作る。

---

## 背景

Task026で、回答履歴とQuestionの正解情報を比較し、ResultScreenに正解数を表示できるようになった。

現在は合計の正解数のみ表示しており、各Questionごとの詳細な結果は確認できない。

本Taskでは、ResultScreenに回答結果の簡易一覧を追加する。

---

## 前提条件

- Task026が完了していること
- AnswerRecordにユーザーの選択回答が記録されていること
- QuestionにcorrectAnswerLabelが存在すること
- ResultScreenに回答数と正解数を表示できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- ResultScreenに回答結果一覧を追加する
- 各Questionごとに以下を表示する
  - 問題番号
  - 選択した回答
  - 正解回答
  - 正誤結果
- 既存の回答数表示を維持する
- 既存の正解数表示を維持する
- 詳細な解説表示は行わない

---

## 変更対象

- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
- QuestionScreenの大幅変更
- main.dart
- Questionモデル
- AnswerRecordモデル
- QuestionRepositoryの大幅変更
- ChartCard
- AnswerButton
- Pythonコード
- API通信
- FastAPI
- yfinance
- 実チャート表示
- 外部パッケージ
- チャート解説表示
- スコア計算ロジックの大幅変更

---

## ResultScreen仕様

ResultScreenに回答結果一覧を表示する。

表示対象は、answerRecordsに含まれる回答履歴とする。

各AnswerRecordに対応するQuestionを、questionNumberとcurrentNumberで照合する。

各行には以下を表示する。

- `Q1`
- `選択: Chart A`
- `正解: Chart A`
- `結果: 正解`

不正解の場合は以下のように表示する。

- `Q2`
- `選択: 現金保有`
- `正解: Chart B`
- `結果: 不正解`

---

## 表示仕様

既存の以下表示は維持する。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- `回答数: x件`
- `正解数: y問`
- `ホームへ戻る`

回答結果一覧は、回答数・正解数の下に表示する。

一覧の見た目はシンプルでよい。

Material3の標準Widgetを利用する。

必要に応じて、ResultScreen全体をスクロール可能にする。

---

## 操作仕様

操作仕様はTask026から変更しない。

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
- ResultScreenに `Q1` が表示される
- ResultScreenに `選択: Chart A` が表示される
- ResultScreenに `正解: Chart A` が表示される
- ResultScreenに `結果: 正解` が表示される
- ResultScreenに `Q2` が表示される
- ResultScreenに `選択: 現金保有` が表示される
- ResultScreenに `正解: Chart B` が表示される
- ResultScreenに `結果: 不正解` が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## テスト前提

Widgetテストでは、Task026と同じく以下の回答を行う。

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
- Q1: 正解
- Q2: 不正解
- Q3: 不正解

---

## 受け入れ条件

- ResultScreenに回答結果一覧が表示されている
- 各Questionごとの選択回答が表示されている
- 各Questionごとの正解回答が表示されている
- 各Questionごとの正誤結果が表示されている
- 既存の回答数表示が維持されている
- 既存の正解数表示が維持されている
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
- Q1の結果が正解として表示される
- Q2の結果が不正解として表示される
- Q3の結果が不正解として表示される
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push