
# Task 030

## タイトル

選択肢をカードUIにする

---

## 目的

QuestionScreenの回答選択肢を、スマホアプリ向けのカードUIとして表示できるようにする。

Chart A / Chart B / Chart C / 現金保有をカードとして並べ、ユーザーがカードをタップして選択できるようにする。

回答はカード選択だけでは確定せず、既存の回答ボタンを押したときに確定する。

---

## 背景

Task029までで、Flutter版Stock Trainerは以下の流れを実装済みである。

- HomeScreenからゲーム開始
- QuestionScreenで回答
- 最後のQuestion回答後にResultScreenへ遷移
- 回答数を表示
- 正解数を表示
- 正答率を表示
- ランクを表示
- 回答結果一覧を表示

現在のQuestionScreenでは、Chart A / Chart B / Chart C / 現金保有が回答ボタンとして縦に並んでいる。

しかし、最終的にはスマホアプリとして、2つ目のモックアップ画像のようなシックなカードUIを目指す。

本Taskでは、回答選択肢をボタン中心のUIからカード選択UIへ近づける。

---

## 前提条件

- Task029が完了していること
- QuestionScreenで回答できること
- 回答後に次のQuestionへ進めること
- 最後のQuestion回答後にResultScreenへ遷移できること
- ResultScreenに回答結果が反映されること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- Chart A / Chart B / Chart C / 現金保有をカードUIとして表示する
- カードをタップすると選択状態になる
- 選択中のカードを視覚的に強調する
- 回答ボタンは残す
- 回答ボタンを押すと、選択中のカードのラベルを回答として扱う
- 未選択状態では回答ボタンを押せない、または押しても進まないようにする
- 既存のゲーム進行を維持する
- 既存のResultScreen表示を維持する

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/widgets/chart_card.dart
- frontend/lib/widgets/answer_button.dart

---

## 変更対象外

- HomeScreen
- ResultScreen
- main.dart
- Questionモデル
- AnswerRecordモデル
- QuestionRepository
- Pythonコード
- API通信
- FastAPI
- yfinance
- 実チャート表示
- 外部パッケージ追加
- 回答結果一覧の仕様変更
- 正解数算出ロジックの変更
- 正答率算出ロジックの変更
- ランク算出ロジックの変更

---

## UI方針

最終的には、2つ目のモックアップ画像のようなスマホアプリUIを目指す。

方向性は以下とする。

- ダーク/チャコール基調
- ゴールドアクセント
- 角丸カード
- 余白を広めに取る
- 1画面で判断しやすい構成
- 投資トレーニングアプリらしい落ち着いた見た目

ただし、本Taskでは全体テーマ変更までは行わない。

本Taskでは、選択肢をカードUI化することを優先する。

---

## QuestionScreen仕様

QuestionScreenでは、回答選択肢をカードとして表示する。

表示対象は以下とする。

- Chart A
- Chart B
- Chart C
- 現金保有

カードをタップすると、そのカードが選択状態になる。

選択状態のカードは、枠線や背景色などで通常状態と区別できるようにする。

選択できるカードは1つだけとする。

別のカードをタップした場合、選択状態は新しいカードへ切り替わる。

---

## 回答ボタン仕様

回答ボタンは残す。

回答ボタンの役割は、選択中のカードを回答として確定することである。

回答ボタン表示文言は以下とする。

```text
回答する
```

未選択状態では、回答ボタンは押せない状態にする。

カード選択後、回答ボタンを押せる状態にする。

回答ボタンを押すと、選択中カードのラベルを `selectedAnswerLabel` として扱い、次のQuestionへ進む。

---

## 表示仕様

カード表示は以下のどちらかを基本とする。

第1希望：縦4つ

```text
[ Chart A ]
[ Chart B ]
[ Chart C ]
[ 現金保有 ]
```

第2希望：2×2

```text
[ Chart A ] [ Chart B ]
[ Chart C ] [ 現金保有 ]
```

実装上、画面に収まりやすい方を選択してよい。

ただし、意図しない自動折り返しで不安定な見た目になることは避ける。

---

## 操作仕様

- QuestionScreen表示時点では、どのカードも未選択
- 回答ボタンは無効状態
- カードをタップすると選択状態になる
- 回答ボタンが有効状態になる
- 別のカードをタップすると選択が切り替わる
- 回答ボタンを押すと次のQuestionへ進む
- 次のQuestionでは選択状態をリセットする
- 最後のQuestion回答後はResultScreenへ遷移する

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- QuestionScreen表示直後は回答ボタンが無効である
- Chart Aカードをタップすると選択状態になる
- カード選択後、回答ボタンが有効になる
- 回答ボタンを押すと次のQuestionへ進む
- 次のQuestionでは選択状態がリセットされる
- 3問回答後、ResultScreenへ遷移する
- ResultScreenに `回答数: 3件` が表示される
- ResultScreenに `正解数: 1問` が表示される
- ResultScreenに `正答率: 33%` が表示される
- ResultScreenに `ランク: C` が表示される
- ResultScreenに回答結果一覧が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## テスト前提

Widgetテストでは、以下の選択と回答を行う。

- Question 1: `Chart A` カードを選択し、`回答する` を押す
- Question 2: `現金保有` カードを選択し、`回答する` を押す
- Question 3: `現金保有` カードを選択し、`回答する` を押す

QuestionRepositoryの正解は以下である。

- Question 1: `Chart A`
- Question 2: `Chart B`
- Question 3: `Chart C`

そのため、期待される結果は以下とする。

- 回答数: 3件
- 正解数: 1問
- 正答率: 33%
- ランク: C
- Q1: 正解
- Q2: 不正解
- Q3: 不正解

---

## 受け入れ条件

- 回答選択肢がカードUIとして表示されている
- カードをタップして選択できる
- 選択中カードが視覚的に分かる
- 選択できるカードは1つだけである
- 回答ボタンが残っている
- 未選択状態では回答ボタンが無効である
- 選択後に回答ボタンが有効になる
- 回答ボタンで次のQuestionへ進める
- 次のQuestionで選択状態がリセットされる
- 既存のResultScreen表示が壊れていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- ゲーム開始
- `Question 1 / 10` 表示
- 回答ボタンが無効であることを確認
- `Chart A` カードをタップ
- `Chart A` が選択状態になることを確認
- 回答ボタンを押す
- `Question 2 / 10` 表示
- 選択状態がリセットされていることを確認
- `現金保有` カードをタップ
- 回答ボタンを押す
- `Question 3 / 10` 表示
- `現金保有` カードをタップ
- 回答ボタンを押す
- ResultScreen表示
- `回答数: 3件` 表示
- `正解数: 1問` 表示
- `正答率: 33%` 表示
- `ランク: C` 表示
- 回答結果一覧が表示される
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push