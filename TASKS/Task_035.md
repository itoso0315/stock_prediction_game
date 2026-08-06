

# Task 035

## タイトル

ResultScreenをモック風の結果画面に整える

---

## 目的

ResultScreenを、ゲーム終了後の結果画面として見やすく、達成感のあるUIに整える。

現在の結果表示は機能としては成立しているが、まだ情報が縦に並んでいるだけの印象が強い。

本Taskでは、ダーク×ゴールド基調のシックな雰囲気を保ちながら、結果サマリー・ランク・回答詳細が見やすい画面へ近づける。

---

## 背景

Task030で、QuestionScreenの回答選択肢をカードUIにした。

Task031で、QuestionScreenに説明文と補足文を追加した。

Task032で、アプリ全体にダーク×ゴールドの共通テーマを適用した。

Task033で、QuestionScreenとResultScreenを画面サイズに応じて自然に見えるレスポンシブUIに整えた。

Task034で、HomeScreenをモック風の導入画面に整えた。

次は、ゲーム終了後に表示されるResultScreenを整える。

ResultScreenは、ユーザーが自分の回答結果を確認し、もう一度遊ぶか判断する重要な画面である。

---

## 前提条件

- Task034が完了していること
- HomeScreenからQuestionScreenへ遷移できること
- 3問回答後にResultScreenへ遷移できること
- ResultScreenで回答数、正解数、正答率、ランクが表示されること
- ResultScreenで各Questionの回答詳細が表示されること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

ResultScreenを、モックアップに近い結果画面として整える。

以下の要素を見やすく表示する。

- 結果タイトル
- ランク表示
- 正答率
- 正解数
- 回答数
- 各Questionの回答詳細
- ホームへ戻るボタン

---

## 変更対象

- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/widgets/score_card.dart

---

## 変更対象外

- HomeScreen
- QuestionScreen
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
- 結果が一目で分かる
- 回答詳細が読みやすい
- ゲーム終了後の達成感がある
- スマホでもMacでも自然に見える

---

## ResultScreen表示仕様

ResultScreenには以下を表示する。

### 結果タイトル

```text
結果発表
```

### 終了メッセージ

```text
ゲーム終了です
```

### サマリー

以下の情報を、1つのサマリーカード内で見やすく表示する。

```text
回答数: 3件
正解数: 2問
正答率: 66%
ランク: B
```

実際の数値は既存ロジックの計算結果を使う。

### 回答詳細

既存の回答詳細表示を維持する。

```text
Q1
選択: Chart A
正解: Chart A
結果: 正解
```

```text
Q2
選択: Chart C
正解: Chart B
結果: 不正解
```

```text
Q3
選択: Chart C
正解: Chart C
結果: 正解
```

### ホームへ戻るボタン

表示文言は以下を維持する。

```text
ホームへ戻る
```

---

## レイアウト方針

固定のスマホ幅に閉じ込めるのではなく、画面サイズに応じて自然に表示する。

- スマホ幅では縦に読みやすく表示する
- 広い画面では中央にまとまり、横に間延びしすぎない
- `LayoutBuilder` などを使って、余白やコンテンツ幅を調整してよい
- サマリーカードを作り、結果の重要情報をまとめる
- 回答詳細カードは、現状より読みやすく整理する
- ボタンは広い画面で横長になりすぎないようにする

---

## 操作仕様

既存の操作仕様を維持する。

- 3問回答後にResultScreenへ遷移する
- ResultScreenで結果を確認する
- `ホームへ戻る` ボタンを押す
- HomeScreenへ戻る

---

## テスト仕様

既存のWidgetテストが引き続き成功すること。

以下を確認する。

- 3問回答後にResultScreenへ遷移する
- ResultScreenに `結果発表` が表示される
- ResultScreenに `ゲーム終了です` が表示される
- ResultScreenに `回答数: 3件` が表示される
- ResultScreenに `正解数` が表示される
- ResultScreenに `正答率` が表示される
- ResultScreenに `ランク` が表示される
- ResultScreenに各Questionの回答詳細が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## 受け入れ条件

- ResultScreenがダーク×ゴールド基調に合っている
- ResultScreenがモックアップの方向性に近づいている
- 結果サマリーが一目で分かる
- 回答詳細が読みやすい
- 画面サイズに応じて自然に表示される
- 固定スマホ幅に閉じ込める実装になっていない
- `ホームへ戻る` ボタンでHomeScreenへ戻れる
- 既存のゲーム進行が壊れていない
- 正解数算出ロジックを変更していない
- 正答率算出ロジックを変更していない
- ランク算出ロジックを変更していない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- `ゲーム開始` 押下
- QuestionScreen表示
- 3問回答
- ResultScreen表示
- 結果サマリーが見やすいことを確認
- 回答詳細が読みやすいことを確認
- Macアプリのウィンドウ幅を狭くして確認
- スマホ幅相当で見やすいことを確認
- Macアプリのウィンドウ幅を広げて確認
- 広い画面でも横に間延びしすぎないことを確認
- `ホームへ戻る` 押下
- HomeScreenへ戻ることを確認

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push
# Task 035

## タイトル

回答後に1問ごとの結果発表画面を表示する

---

## 目的

Flutter版のゲーム進行を、Web版と同じ「1問ごとに答え合わせを表示する流れ」に近づける。

現在のFlutter版は、QuestionScreenで複数問を連続回答したあと、最後にResultScreenでまとめて結果を表示している。

しかしWeb版では、1問回答するたびに結果発表画面を表示し、正解・不正解、あなたの回答、正解、現在の正答率などを確認してから次の問題へ進む構成になっている。

本Taskでは、まずFlutter版でも回答後に1問ごとの結果発表画面を挟む。

---

## 背景

Task030で、QuestionScreenの回答選択肢をカードUIにした。

Task031で、QuestionScreenに説明文と補足文を追加した。

Task032で、アプリ全体にダーク×ゴールドの共通テーマを適用した。

Task033で、QuestionScreenとResultScreenを画面サイズに応じて自然に見えるレスポンシブUIに整えた。

Task034で、HomeScreenをモック風の導入画面に整えた。

その後、Web版の画面構成を確認した結果、Flutter版とWeb版でゲーム進行が違うことが分かった。

Web版は以下の流れである。

```text
問題画面
↓
回答する
↓
1問ごとの結果発表画面
↓
次の問題へ
↓
これを繰り返す
↓
最後に全体の結果を表示
```

Flutter版もこの構成に近づける。

---

## 前提条件

- Task034が完了していること
- HomeScreenからQuestionScreenへ遷移できること
- QuestionScreenでカード選択できること
- QuestionScreenで回答ボタンを押せること
- QuestionRepositoryにダミー問題が存在すること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

回答後に、すぐ次のQuestionへ進むのではなく、1問ごとの結果発表画面を表示する。

以下の画面を新しく追加する。

- AnswerReviewScreen

AnswerReviewScreenでは、回答した1問について以下を表示する。

- 結果タイトル
- 現在の問題番号
- 現在の成績
- 現在の正答率
- 目標正答率
- 正解/不正解
- あなたの回答
- 正解
- 次の問題へボタン

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/screens/answer_review_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/screens/result_screen.dart

---

## 変更対象外

- HomeScreen
- main.dart
- Questionモデル
- AnswerRecordモデル
- QuestionRepositoryの大幅変更
- Pythonコード
- API通信
- FastAPI
- yfinance
- 外部パッケージ追加
- チャート描画ロジック
- 移動平均線表示ロジック
- 本物の株価データ取得

---

## UI方針

最終的には、Web版の結果発表画面と、2つ目のモックアップ画像の雰囲気を組み合わせたスマホアプリUIを目指す。

方向性は以下とする。

- シック
- ダーク/チャコール基調
- ゴールドアクセント
- 高級感
- 光沢は控えめ
- 1問ごとの結果が一目で分かる
- 正答率70%を目標として表示する
- ランク表示は使わない
- スマホでもMacでも自然に見える

---

## 画面遷移仕様

現在のFlutter版は以下の流れになっている。

```text
HomeScreen
↓
QuestionScreen
↓
QuestionScreen
↓
QuestionScreen
↓
ResultScreen
```

本Taskでは、以下の流れに変更する。

```text
HomeScreen
↓
QuestionScreen
↓
AnswerReviewScreen
↓
QuestionScreen
↓
AnswerReviewScreen
↓
QuestionScreen
↓
AnswerReviewScreen
↓
ResultScreen
```

※ 現時点ではダミー問題数に合わせた流れでよい。

最終的には10問連続プレイを目指すが、本Taskでは10問化までは必須にしない。

---

## AnswerReviewScreen表示仕様

AnswerReviewScreenには以下を表示する。

### タイトル

```text
結果発表
```

### 現在の問題番号

```text
問題 1 / 3
```

※ 実際の分母は現在のQuestionRepositoryの問題数を使う。

将来的に10問化した場合は `問題 1 / 10` になる。

### 現在の成績

```text
現在の成績
1問正解 / 1問回答
```

### 現在の正答率

```text
現在の正答率
100%
```

### 目標

```text
目標
70%
```

### 結果

正解の場合：

```text
結果
○ 正解
```

不正解の場合：

```text
結果
× 不正解
```

### あなたの回答

```text
あなたの回答
Chart C
```

### 正解

```text
正解
Chart B
```

### 目標メッセージ

```text
正答率70%を目指しましょう
```

### 次へボタン

最終問題ではない場合：

```text
次の問題へ
```

最終問題の場合：

```text
最終結果を見る
```

---

## ResultScreen仕様

ResultScreenは、全問終了後の最終結果画面として扱う。

本Taskでは大きく作り込まなくてよい。

ただし、ランク表示は使わない。

ResultScreenに表示する中心情報は以下とする。

- 正答率
- 正解数
- 回答数
- 正答率70%を目指しましょう
- ホームへ戻るボタン

---

## ランク表示方針

ランク表示は使わない。

以下のような表示は削除する。

```text
ランク: A
ランク: B
ランク: C
```

学習アプリとしては、ランクよりも正答率目標の方が分かりやすいため、正答率70%を目標として表示する。

---

## チャート表示方針

Web版では、結果発表画面に各チャートのレビューや銘柄名、騰落率、Yahoo!ファイナンスリンク、AIひとこと解説が表示される。

ただし、現時点のFlutter版はまだダミーデータ中心であり、API未接続である。

そのため本Taskでは、詳細チャートレビューやAI解説は必須にしない。

これらは後続Taskで扱う。

---

## 移動平均線表示方針

Web版には、移動平均線表示のON/OFF切り替えがある。

仕様は以下とする。

- OFF時もローソク足と出来高は常に表示する
- ON時のみ、20日・40日・70日の移動平均線を追加表示する

ただし、本Taskでは移動平均線ON/OFFの実装は行わない。

API接続後、Python側でMA20/MA40/MA70を計算してFlutterへ返し、Flutter側ではON/OFFに応じて表示を切り替える方針とする。

---

## 操作仕様

- HomeScreenで `ゲーム開始` を押す
- QuestionScreenへ遷移する
- 回答カードを選択する
- `回答する` ボタンを押す
- AnswerReviewScreenへ遷移する
- 正解/不正解、あなたの回答、正解、現在の正答率を確認する
- `次の問題へ` を押す
- 次のQuestionScreenへ進む
- 最終問題のAnswerReviewScreenでは `最終結果を見る` を表示する
- `最終結果を見る` を押す
- ResultScreenへ遷移する
- `ホームへ戻る` を押す
- HomeScreenへ戻る

---

## テスト仕様

既存のWidgetテストを更新し、以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- QuestionScreenで回答カードを選択できる
- 回答ボタン押下後、AnswerReviewScreenへ遷移する
- AnswerReviewScreenに `結果発表` が表示される
- AnswerReviewScreenに `あなたの回答` が表示される
- AnswerReviewScreenに `正解` が表示される
- AnswerReviewScreenに `正答率70%を目指しましょう` が表示される
- 最終問題ではない場合、`次の問題へ` が表示される
- `次の問題へ` 押下後、次のQuestionScreenへ遷移する
- 最終問題後、`最終結果を見る` が表示される
- `最終結果を見る` 押下後、ResultScreenへ遷移する
- ResultScreenに正答率、回答数、正解数が表示される
- `ホームへ戻る` ボタンでHomeScreenへ戻れる

---

## 受け入れ条件

- 回答後にすぐ次の問題へ進まず、AnswerReviewScreenが表示される
- AnswerReviewScreenで正解/不正解が分かる
- AnswerReviewScreenであなたの回答と正解が分かる
- AnswerReviewScreenで現在の正答率が分かる
- 目標として70%が表示される
- ランク表示がない
- 最終問題ではResultScreenへ進める
- 既存のゲーム進行が壊れていない
- 固定スマホ幅に閉じ込める実装になっていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- `ゲーム開始` 押下
- QuestionScreen表示
- 回答カード選択
- `回答する` 押下
- AnswerReviewScreen表示
- 正解/不正解表示を確認
- あなたの回答表示を確認
- 正解表示を確認
- 正答率70%目標表示を確認
- `次の問題へ` 押下
- 次のQuestionScreen表示
- 最終問題まで回答
- 最終問題のAnswerReviewScreenで `最終結果を見る` 表示を確認
- `最終結果を見る` 押下
- ResultScreen表示
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push