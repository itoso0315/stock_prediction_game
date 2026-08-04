# Task 026

## タイトル

回答の正誤判定を実装する

---

## 目的

ユーザーが選択した回答とQuestionの正解情報を比較し、正解数を算出できるようにする。

本Taskでは、Task025で追加したcorrectAnswerLabelとTask024で記録したAnswerRecordを利用して、ResultScreenに正解数を表示する。

---

## 背景

Task024で、ユーザーが選択した回答内容をAnswerRecordとして記録できるようになった。

Task025で、QuestionモデルにcorrectAnswerLabelを追加し、各Questionが正解情報を持てるようになった。

現在は回答数のみ表示しており、ユーザーの回答が正解だったかどうかは判定していない。

本Taskでは、回答履歴と正解情報を比較し、ResultScreenに正解数を表示する。

---

## 前提条件

- Task025が完了していること
- QuestionにcorrectAnswerLabelが存在すること
- AnswerRecordにユーザーの選択回答が記録されていること
- ResultScreenに回答数を表示できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- ResultScreenで回答履歴とQuestion一覧を比較する
- 正解数を算出する
- ResultScreenに正解数を表示する
- 既存の回答数表示は維持する
- 詳細な回答一覧は表示しない

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
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
- 詳細な回答結果一覧
- 解説表示

---

## QuestionScreen仕様

ResultScreenへ遷移する際、以下を渡す。

- 回答履歴
- Question一覧

既存の回答記録処理は維持する。

既存の画面遷移は維持する。

---

## ResultScreen仕様

ResultScreenは以下を受け取る。

- answerRecords: List<AnswerRecord>
- questions: List<Question>

ResultScreenで、answerRecordsとquestionsを比較して正解数を算出する。

比較方法は以下とする。

- AnswerRecord.questionNumber と Question.currentNumber が一致するQuestionを探す
- AnswerRecord.selectedAnswerLabel と Question.correctAnswerLabel が一致した場合、正解とする

ResultScreenには以下を表示する。

- `回答数: x件`
- `正解数: y問`

xには回答履歴の件数を表示する。

yには正解数を表示する。

既存の以下表示は維持する。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- HomeScreenへ戻るボタン：`ホームへ戻る`

---

## 表示仕様

ResultScreenに正解数表示を追加する。

例：

```text
回答数: 3件
正解数: 1問
```

本Taskでは、正答率やスコア表記は表示しない。

---

## 操作仕様

操作仕様はTask025から変更しない。

- 回答ボタンを押すと次のQuestionへ進む
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenからHomeScreenへ戻れる

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- 回答ボタン押下で次のQuestionへ進む
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenに `回答数: 3件` が表示される
- ResultScreenに `正解数: 1問` が表示される
- ResultScreenに `結果発表` が表示される
- ResultScreenに `ゲーム終了です` が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## テスト前提

既存テストでは、3問すべてで `現金保有` を選択している。

QuestionRepositoryの正解は以下である。

- Question 1: `Chart A`
- Question 2: `Chart B`
- Question 3: `Chart C`

そのため、テスト上の正解数は0問になる。

ただし、テストで1問正解させる場合は、最初の回答のみ `Chart A` を選択し、残りは `現金保有` を選択する。

本TaskのWidgetテストでは、以下の選択とする。

- Question 1: `Chart A`
- Question 2: `現金保有`
- Question 3: `現金保有`

この場合、期待される正解数は `1問` とする。

---

## 受け入れ条件

- ResultScreenで正解数を算出している
- ResultScreenに `正解数: y問` が表示されている
- 回答数表示が維持されている
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
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push
