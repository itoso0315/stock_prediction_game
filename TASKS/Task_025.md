

# Task 025

## タイトル

Questionに正解情報を持たせる

---

## 目的

Questionモデルに正解情報を追加し、将来的にユーザーの回答と正解を比較できる基盤を作る。

本Taskでは正誤判定やスコア計算は行わず、各Questionが「どの回答ラベルを正解とするか」を保持できるようにする。

---

## 背景

Task024で、ユーザーが選択した回答内容をAnswerRecordとして記録できるようになった。

現在は「ユーザーが何を選んだか」は記録できるが、「各Questionの正解が何か」はQuestionモデルに存在しない。

本Taskでは、Questionモデルに正解回答ラベルを追加する。

---

## 前提条件

- Task024が完了していること
- 回答履歴をAnswerRecordとして記録できること
- ResultScreenに回答数を表示できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- Questionモデルに正解回答ラベルを追加する
- QuestionRepositoryのダミーデータに正解回答ラベルを設定する
- 既存画面の表示・操作は変更しない
- 正誤判定は行わない
- スコア計算は行わない

---

## 変更対象

- frontend/lib/models/question.dart
- frontend/lib/repositories/question_repository.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
- QuestionScreenの大幅変更
- ResultScreenの大幅変更
- AnswerRecord
- ChartCard
- AnswerButton
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

## Questionモデル仕様

Questionモデルに以下のフィールドを追加する。

- correctAnswerLabel: String

correctAnswerLabelには、answerLabelsに含まれる回答ラベルのいずれかを設定する。

Questionは引き続きimmutableなデータモデルとする。

---

## QuestionRepository仕様

QuestionRepository内の全QuestionにcorrectAnswerLabelを設定する。

本Taskではダミーデータとして以下を設定する。

- Question 1: `Chart A`
- Question 2: `Chart B`
- Question 3: `Chart C`

correctAnswerLabelはanswerLabelsに含まれる値と一致させる。

---

## 表示仕様

本Taskでは画面表示を変更しない。

以下の表示はTask024と同じとする。

- Question 1 / 10
- Question 2 / 10
- Question 3 / 10
- ResultScreen
- 回答数: 3件

正解ラベルは画面に表示しない。

---

## 操作仕様

操作仕様はTask024から変更しない。

- 回答ボタンを押すと次のQuestionへ進む
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenからHomeScreenへ戻れる

---

## テスト仕様

以下を確認する。

- QuestionRepositoryから取得したQuestionにcorrectAnswerLabelが設定されている
- correctAnswerLabelがanswerLabelsに含まれている
- 既存の画面遷移テストが成功する
- ResultScreenに `回答数: 3件` が表示される

---

## 受け入れ条件

- QuestionモデルにcorrectAnswerLabelが追加されている
- QuestionRepositoryの全QuestionにcorrectAnswerLabelが設定されている
- correctAnswerLabelがanswerLabelsに含まれている
- 既存のゲーム進行が壊れていない
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