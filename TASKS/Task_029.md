# Task 029

## タイトル

結果画面に評価ランクを表示する

---

## 目的

ResultScreenに、正答率に応じた評価ランクを表示できるようにする。

Task028で表示した正答率を利用し、ゲーム結果をより直感的に理解できるようにする。

---

## 背景

Task026で正解数を表示できるようになった。

Task027で各Questionごとの回答結果一覧を表示できるようになった。

Task028で正答率を表示できるようになった。

現在は数値として正答率は表示されるが、結果の良し悪しを直感的に伝える評価表示はない。

本Taskでは、正答率に応じた評価ランクをResultScreenに表示する。

---

## 前提条件

- Task028が完了していること
- ResultScreenに回答数が表示されていること
- ResultScreenに正解数が表示されていること
- ResultScreenに正答率が表示されていること
- ResultScreenに回答結果一覧が表示されていること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- ResultScreenで正答率に応じた評価ランクを算出する
- ResultScreenに評価ランクを表示する
- 既存の回答数表示を維持する
- 既存の正解数表示を維持する
- 既存の正答率表示を維持する
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
- 詳細な採点ロジック

---

## ResultScreen仕様

ResultScreenで正答率に応じた評価ランクを算出する。

ランク条件は以下とする。

- 正答率 80%以上：`ランク: A`
- 正答率 50%以上80%未満：`ランク: B`
- 正答率 50%未満：`ランク: C`

回答数が0件の場合は、正答率0%として扱い、`ランク: C` とする。

---

## 表示仕様

既存の以下表示は維持する。

- AppBarタイトル：`Result`
- メイン見出し：`結果発表`
- 説明文：`ゲーム終了です`
- `回答数: x件`
- `正解数: y問`
- `正答率: z%`
- 回答結果一覧
- `ホームへ戻る`

評価ランクは、正答率の下に表示する。

表示順は以下とする。

```text
回答数: 3件
正解数: 1問
正答率: 33%
ランク: C
```

---

## 操作仕様

操作仕様はTask028から変更しない。

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
- ResultScreenに `ランク: C` が表示される
- ResultScreenに回答結果一覧が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## テスト前提

Widgetテストでは、Task028と同じく以下の回答を行う。

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
- ランク: C
- Q1: 正解
- Q2: 不正解
- Q3: 不正解

---

## 受け入れ条件

- ResultScreenに評価ランクが表示されている
- 評価ランクが正答率から算出されている
- 既存の回答数表示が維持されている
- 既存の正解数表示が維持されている
- 既存の正答率表示が維持されている
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
