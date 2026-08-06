# Task 034

## タイトル

HomeScreenをモック風の導入画面に整える

---

## 目的

HomeScreenを、Stock Trainerの最初の画面としてふさわしい導入画面に整える。

現在の素朴な開始画面から、ダーク×ゴールド基調のシックなスマホアプリUIへ近づける。

---

## 背景

Task030で、QuestionScreenの回答選択肢をカードUIにした。

Task031で、QuestionScreenに説明文と補足文を追加した。

Task032で、アプリ全体にダーク×ゴールドの共通テーマを適用した。

Task033で、QuestionScreenとResultScreenを画面サイズに応じて自然に見えるレスポンシブUIに整えた。

次は、アプリ起動直後に表示されるHomeScreenを整える。

HomeScreenはユーザーが最初に見る画面なので、ここを整えるとアプリ全体の印象が大きく良くなる。

---

## 前提条件

- Task033が完了していること
- QuestionScreenへ遷移できること
- アプリ全体にダーク×ゴールドの共通テーマが適用されていること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

HomeScreenを、モックアップに近い導入画面として整える。

以下の要素を表示する。

- アプリ名
- 短いキャッチコピー
- ゲーム内容の簡単な説明
- 今日のトレーニングを始める雰囲気のカード
- ゲーム開始ボタン

---

## 変更対象

- frontend/lib/screens/home_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/widgets/score_card.dart

---

## 変更対象外

- QuestionScreen
- ResultScreen
- main.dart
- Questionモデル
- AnswerRecordモデル
- QuestionRepository
- Pythonコード
- API通信
- FastAPI
- yfinance
- 外部パッケージ追加
- 正解数算出ロジック
- 正答率算出ロジック
- ランク算出ロジック
- 共通テーマの大幅変更

---

## UI方針

最終的には、2つ目のモックアップ画像のようなスマホアプリUIを目指す。

方向性は以下とする。

- シック
- ダーク/チャコール基調
- ゴールドアクセント
- 高級感
- 光沢は控えめ
- 余白をきれいに使う
- 説明しすぎず、すっきり見せる
- スマホでもMacでも自然に見える

---

## HomeScreen表示仕様

HomeScreenには以下を表示する。

### アプリ名

```text
Stock Trainer
```

### キャッチコピー

```text
チャートだけで未来を読む
```

### 説明文

```text
銘柄名を隠したチャートを見比べて、1か月後に最も伸びる選択肢を選びましょう。
```

### トレーニングカード

以下のような内容を表示する。

```text
Today's Training
3問チャレンジ
チャートの形、出来高、流れを見て判断します。
```

### 開始ボタン

表示文言は以下を維持する。

```text
ゲーム開始
```

---

## レイアウト方針

固定のスマホ幅に閉じ込めるのではなく、画面サイズに応じて自然に表示する。

- スマホ幅では縦に読みやすく表示する
- 広い画面では中央にまとまり、横に間延びしすぎない
- `LayoutBuilder` などを使って、余白やコンテンツ幅を調整してよい
- ボタンは広い画面で横長になりすぎないようにする

---

## 操作仕様

既存の操作仕様を維持する。

- HomeScreen表示
- `ゲーム開始` ボタンを押す
- QuestionScreenへ遷移する

---

## テスト仕様

既存のWidgetテストが引き続き成功すること。

以下を確認する。

- HomeScreenに `Stock Trainer` が表示される
- HomeScreenに `チャートだけで未来を読む` が表示される
- HomeScreenに `ゲーム開始` が表示される
- `ゲーム開始` を押すとQuestionScreenへ遷移する
- 既存のQuestionScreen以降のテストが壊れていない

---

## 受け入れ条件

- HomeScreenがダーク×ゴールド基調に合っている
- HomeScreenがモックアップの方向性に近づいている
- アプリ起動直後の画面として自然である
- 画面サイズに応じて自然に表示される
- 固定スマホ幅に閉じ込める実装になっていない
- `ゲーム開始` ボタンでQuestionScreenへ遷移できる
- 既存のゲーム進行が壊れていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- Macアプリのウィンドウ幅を狭くして確認
- スマホ幅相当で見やすいことを確認
- Macアプリのウィンドウ幅を広げて確認
- 広い画面でも横に間延びしすぎないことを確認
- `ゲーム開始` 押下
- QuestionScreenへ遷移することを確認
- 3問回答
- ResultScreen表示
- `ホームへ戻る` 押下
- HomeScreenへ戻ることを確認

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push