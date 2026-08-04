

# Task 024

## タイトル

回答内容を記録する基盤を実装する

---

## 目的

QuestionScreenでユーザーが選択した回答内容を記録できるようにする。

本Taskでは正誤判定やスコア計算は行わず、将来的に結果画面や採点機能で利用できる回答履歴の基盤を作る。

---

## 背景

Task023で、最後のQuestion回答後にResultScreenへ遷移できるようになった。

現在は回答ボタンを押すと次のQuestionへ進むが、ユーザーがどの回答を選んだかは保存していない。

本Taskでは、各Questionで選択した回答ラベルを記録する。

---

## 前提条件

- Task023が完了していること
- 回答ボタン押下で次のQuestionへ進めること
- 最後のQuestion回答後にResultScreenへ遷移できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- 回答履歴を表すモデルを新規作成する
- QuestionScreenで回答ボタン押下時に回答内容を記録する
- 記録した回答履歴をResultScreenへ渡す
- ResultScreenで回答件数を表示する
- 正誤判定やスコア計算は行わない

---

## 変更対象

- frontend/lib/models/answer_record.dart
- frontend/lib/screens/question_screen.dart
- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
- main.dart
- ChartCard
- AnswerButton
- Questionモデル
- QuestionRepositoryの大幅変更
- Pythonコード
- API通信
- FastAPI
- yfinance
- 採点機能
- 正誤判定
- スコア計算
- 実チャート表示
- 外部パッケージ

---

## AnswerRecord仕様

AnswerRecordモデルを新規作成する。

保持する情報は以下とする。

- questionNumber: int
- selectedAnswerLabel: String

AnswerRecordはデータ保持のみを担当する。

immutableなクラスとし、const constructorを持つ。

---

## QuestionScreen仕様

QuestionScreenは回答履歴をStateで保持する。

回答ボタン押下時に、以下の情報をAnswerRecordとして記録する。

- 現在のQuestion番号
- 選択された回答ラベル

回答記録後の画面遷移はTask023の仕様を維持する。

- 最後以外のQuestionでは次のQuestionへ進む
- 最後のQuestionではResultScreenへ遷移する

ResultScreenへ遷移する際、記録済みの回答履歴を渡す。

---

## ResultScreen仕様

ResultScreenは回答履歴を受け取る。

本Taskでは詳細な回答一覧は表示しない。

表示する内容は以下を追加する。

- 回答数：`回答数: x件`

xには受け取った回答履歴の件数を表示する。

既存の以下表示は維持する。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- HomeScreenへ戻るボタン：`ホームへ戻る`

---

## 表示仕様

QuestionScreenのUIは大きく変更しない。

ResultScreenに回答数表示を追加する。

例：

```text
回答数: 3件
```

---

## 操作仕様

ゲーム開始後、ユーザーが回答ボタンを押すたびに回答履歴を記録する。

```text
Question 1 / 10
↓ Chart Aを選択
AnswerRecord(questionNumber: 1, selectedAnswerLabel: 'Chart A')

Question 2 / 10
↓ 現金保有を選択
AnswerRecord(questionNumber: 2, selectedAnswerLabel: '現金保有')
```

本Taskでは、どの回答が正しいかは判定しない。

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- 回答ボタン押下で次のQuestionへ進む
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenに `回答数: 3件` が表示される
- ResultScreenに `結果発表` が表示される
- ResultScreenに `ゲーム終了です` が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## 受け入れ条件

- AnswerRecordモデルが実装されている
- QuestionScreenで回答履歴を記録している
- ResultScreenへ回答履歴を渡している
- ResultScreenで回答数を表示している
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- ゲーム開始
- `Question 1 / 10` 表示
- 回答ボタン押下
- `Question 2 / 10` 表示
- 回答ボタン押下
- `Question 3 / 10` 表示
- 回答ボタン押下
- ResultScreen表示
- `回答数: 3件` 表示
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push