

# Task 031

## タイトル

QuestionScreenをシックなスマホUIに整える

---

## 目的

QuestionScreenの画面構成を、最終イメージである2つ目のモックアップ画像に近いシックなスマホアプリUIへ整える。

Task030で実装したカード選択UIをベースに、問題文、説明文、カード配置、回答ボタン周りをより見やすくする。

---

## 背景

Task030で、Chart A / Chart B / Chart C / 現金保有をカードUIとして表示し、カード選択後に回答ボタンで確定できるようになった。

現在のUIは機能としては成立しているが、まだFlutter標準UIに近く、最終的に目指すスマホアプリらしいシックな雰囲気には届いていない。

本Taskでは、QuestionScreenをスマホアプリとして見やすく、落ち着いた画面構成に整える。

---

## 前提条件

- Task030が完了していること
- QuestionScreenでカードを選択できること
- 回答ボタンで回答を確定できること
- 最後のQuestion回答後にResultScreenへ遷移できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- QuestionScreenに短い説明文を追加する
- QuestionScreen全体の余白を整える
- カード選択エリアを見やすく整える
- 回答ボタンの配置を整える
- 既存のカード選択ロジックを維持する
- 既存のゲーム進行を維持する
- 既存のResultScreen表示を維持する

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/widgets/chart_card.dart

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
- 正解数算出ロジック
- 正答率算出ロジック
- ランク算出ロジック

---

## UI方針

最終的には、2つ目のモックアップ画像のようなスマホアプリUIを目指す。

方向性は以下とする。

- シック
- ダーク/チャコール基調
- ゴールドアクセント
- カードUI
- 余白を広めに取る
- 情報を詰め込みすぎない
- 投資トレーニングアプリらしい落ち着いた見た目

ただし、本Taskではアプリ全体のテーマ変更までは行わない。

本Taskでは、QuestionScreen単体の画面構成改善を優先する。

---

## QuestionScreen仕様

QuestionScreenには、現在のQuestion番号を表示する。

既存の表示は維持する。

```text
Question 1 / 10
```

その下に、ユーザーが何をすればよいか分かる短い説明文を表示する。

表示文言は以下とする。

```text
6か月分のチャートを見て、1か月後の評価日に最も騰落率が高い選択肢を選んでください。
```

補足文として以下を表示する。

```text
銘柄名は隠されています。チャートの形だけで判断しましょう。
```

---

## カード表示仕様

Task030で実装した選択カードを維持する。

表示対象は以下とする。

- Chart A
- Chart B
- Chart C
- 現金保有

カード表示は縦4つを基本とする。

```text
[ Chart A ]
[ Chart B ]
[ Chart C ]
[ 現金保有 ]
```

画面に収まらない場合はスクロールしてよい。

選択中カードの強調表示は維持する。

---

## 回答ボタン仕様

回答ボタンは画面下部に配置する。

回答ボタン表示文言は維持する。

```text
回答する
```

未選択状態では回答ボタンは無効状態とする。

カード選択後、回答ボタンを有効状態にする。

---

## 操作仕様

操作仕様はTask030から変更しない。

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
- QuestionScreenに `Question 1 / 10` が表示される
- QuestionScreenに説明文が表示される
- QuestionScreenに補足文が表示される
- QuestionScreen表示直後は回答ボタンが無効である
- Chart Aカードをタップすると回答ボタンが有効になる
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

- QuestionScreenに説明文が表示されている
- QuestionScreenに補足文が表示されている
- カード選択UIが維持されている
- 回答ボタンが維持されている
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
- 説明文が表示される
- 補足文が表示される
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