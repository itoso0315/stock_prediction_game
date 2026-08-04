

# Task 022

## タイトル

回答後に次の問題へ進む機能を実装する

---

## 目的

QuestionScreenで回答ボタンを押したあと、次のQuestionを表示できるようにする。

Task021で作成したQuestionRepositoryを利用し、複数問題を順番に表示するゲーム進行の基盤を作る。

---

## 背景

Task021でQuestionRepositoryを作成し、複数のQuestionを保持できるようになった。

現在のQuestionScreenはRepositoryからindex=0のQuestionを取得して表示しているが、回答しても次の問題へ進まない。

本Taskでは、回答ボタン押下をきっかけに次の問題へ進む機能を追加する。

---

## 前提条件

- Task021が完了していること
- QuestionRepositoryが実装されていること
- QuestionScreenがRepository経由でQuestionを表示していること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- QuestionScreenをStatefulWidgetへ変更する
- 現在の問題番号をStateで管理する
- 回答ボタンを押したら次のQuestionへ進む
- 最後のQuestionでは次へ進まず、現在のQuestionを維持する
- QuestionRepositoryからQuestion一覧を取得して利用する
- UIの見た目は大きく変更しない

---

## 変更対象

- frontend/lib/screens/question_screen.dart
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
- スコア表示
- 結果画面
- 外部パッケージ

---

## QuestionScreen仕様

QuestionScreenはStatefulWidgetとする。

Stateで現在の問題indexを保持する。

初期値は0とする。

QuestionRepositoryからQuestion一覧を取得し、現在のindexに対応するQuestionを表示する。

回答ボタン押下時に、現在のindexが最後の問題でなければindexを1増やす。

最後の問題で回答ボタンを押した場合は、indexを変更しない。

---

## 表示仕様

Task020・Task021のUIを維持する。

以下は既存仕様どおり表示する。

- AppBarの `Question x / 10`
- Chart A / Chart B / Chart C
- 回答ボタン4件
- `現金保有`

問題が進むとAppBarの表示も更新される。

例：

- 最初：Question 1 / 10
- 1回回答後：Question 2 / 10
- 2回回答後：Question 3 / 10

---

## 操作仕様

任意の回答ボタンを押すと次の問題へ進む。

本Taskでは、どの回答を選んだかは保存しない。

正解・不正解の判定は行わない。

スコア計算は行わない。

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- 初期表示が `Question 1 / 10` である
- 回答ボタン押下後に `Question 2 / 10` が表示される
- さらに回答ボタン押下後に `Question 3 / 10` が表示される
- 最後のQuestionで回答してもクラッシュしない
- Chart A / Chart B / Chart C が表示される
- 回答ボタン4件が表示される
- `現金保有` が表示される

---

## 受け入れ条件

- QuestionScreenがStatefulWidgetになっている
- 回答ボタン押下で次のQuestionへ進む
- QuestionRepositoryの複数Questionを利用している
- 最後のQuestionでクラッシュしない
- UIが大きく変化していない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- ゲーム開始
- QuestionScreen表示
- `Question 1 / 10` 表示
- 回答ボタン押下
- `Question 2 / 10` 表示
- 回答ボタン押下
- `Question 3 / 10` 表示
- Overflowなし
- HomeScreenへ戻れる

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push