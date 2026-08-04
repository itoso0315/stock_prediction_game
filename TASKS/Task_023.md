

# Task 023

## タイトル

最後の問題回答後に結果画面へ遷移する

---

## 目的

QuestionScreenで最後のQuestionまで回答したあと、ゲーム終了を表すResultScreenへ遷移できるようにする。

本Taskではスコア計算や正誤判定は行わず、ゲーム進行の完了地点として結果画面を表示する基盤を作る。

---

## 背景

Task022で、回答ボタンを押すと次のQuestionへ進む機能を実装した。

現在は最後のQuestionで回答しても同じ画面に留まる仕様になっている。

本Taskでは、最後のQuestionで回答した場合にResultScreenへ遷移する。

---

## 前提条件

- Task022が完了していること
- 回答ボタン押下で次のQuestionへ進めること
- 最後のQuestionでクラッシュしないこと
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- ResultScreenを新規作成する
- 最後のQuestionで回答ボタンを押したらResultScreenへ遷移する
- 最後以外のQuestionではこれまでどおり次のQuestionへ進む
- ResultScreenにはゲーム終了を示す文言を表示する
- ResultScreenからHomeScreenへ戻れる導線を用意する

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreenの大幅変更
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

## ResultScreen仕様

ResultScreenを新規作成する。

表示する内容は以下とする。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- HomeScreenへ戻るボタン：`ホームへ戻る`

`ホームへ戻る` ボタンを押すと、HomeScreenへ戻る。

戻る方法は、現在のNavigationスタックをすべて戻してHomeScreenを表示する形とする。

---

## QuestionScreen仕様

回答ボタン押下時の挙動を以下に変更する。

- 現在のQuestionが最後ではない場合
  - 次のQuestionへ進む
- 現在のQuestionが最後の場合
  - ResultScreenへ遷移する

最後のQuestionで回答した場合、同じQuestionに留まらない。

---

## 表示仕様

QuestionScreenのUIはTask022から大きく変更しない。

ResultScreenはシンプルな画面とする。

Material3の標準Widgetを利用する。

---

## 操作仕様

ゲーム開始後、回答ボタンを押すたびに以下のように進む。

```text
Question 1 / 10
↓ 回答
Question 2 / 10
↓ 回答
Question 3 / 10
↓ 回答
ResultScreen
```

本Taskでは、どの回答を選んだかは保存しない。

正解・不正解の判定は行わない。

スコア計算は行わない。

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- 初期表示が `Question 1 / 10` である
- 回答後に `Question 2 / 10` が表示される
- さらに回答後に `Question 3 / 10` が表示される
- 最後のQuestionで回答するとResultScreenへ遷移する
- ResultScreenに `結果発表` が表示される
- ResultScreenに `ゲーム終了です` が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## 受け入れ条件

- ResultScreenが実装されている
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenからHomeScreenへ戻れる
- QuestionScreenの既存UIが大きく変化していない
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
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push