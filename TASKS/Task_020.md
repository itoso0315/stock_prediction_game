# Task 020

## 対象

Frontend（Flutter）

## 目的

QuestionScreen をゲームらしいレイアウトへ発展させ、今後 Python バックエンドと接続しやすい UI の土台を構築する。

## 背景

## 前提条件

- Task019（ホーム画面 → 問題画面の画面遷移）が完了していること。

Task019 でホーム画面と問題画面の画面遷移が完成した。
本Taskではダミーデータを用いて問題画面の UI を完成させる。

## 実装内容

- QuestionScreen のレイアウト作成
- ChartCard Widget を実装
- AnswerButton Widget を実装
- ダミー Question モデルを作成
- 3枚の ChartCard と4つの回答ボタンを表示

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/widgets/chart_card.dart
- frontend/lib/widgets/answer_button.dart
- frontend/lib/models/question.dart

## 変更対象外

- Python バックエンド
- API 通信
- yfinance
- チャート描画
- 採点ロジック
- 問題生成ロジック
- 外部パッケージ追加
- JSON変換
- HTTP通信
- 採点処理
- 正解判定
- アニメーション

## UI仕様

- 上部に「Question 1 / 10」を表示
- ChartCard を縦に3枚配置
- 回答ボタンを4つ配置
  - Chart A
  - Chart B
  - Chart C
  - 現金保有
- Material3 デザインを利用
- スクロール可能なレイアウトとする

### レイアウト

- AppBarタイトルは「Question 1 / 10」とする
- SafeAreaを利用する
- 画面全体をスクロール可能とする
- コンテンツは中央寄せ、最大幅800px程度とする
- ChartCardを縦に3枚配置し、各カード間は16pxとする
- 回答ボタンを縦一列に4つ配置し、各ボタン間は12pxとする
- 画面左右余白は24pxとする

## 責務分離

### QuestionScreen
- Scaffoldと画面レイアウトのみ担当
- ダミーQuestionを1件保持して表示する
- ChartCardとAnswerButtonを組み合わせる

### ChartCard
- チャート表示領域のみ担当
- Material3 Cardを利用する
- ラベル（Chart A/B/C）を表示する
- 実チャートは実装しない

### AnswerButton
- 回答ボタンのみ担当
- ボタン文言と押下コールバックを受け取る
- Material3 FilledButtonを利用する

### Questionモデル
- 問題データのみ保持する
- immutableとする
- constコンストラクタを利用する

## Questionモデル仕様

Questionは以下のフィールドを持つ。

- currentNumber : int
- totalQuestions : int
- chartLabels : List<String>
- answerLabels : List<String>

本TaskではダミーデータをQuestionScreen内で1件生成する。
API通信・JSON変換・永続化は実装しない。

## 操作仕様

- 回答ボタンは押下可能とする
- 押下時は採点・画面遷移を行わない
- 選択状態は保持しない
- ボタンは有効状態を維持する

## 受け入れ条件

- Question 1 / 10 が表示される
- ChartCardが3枚表示される
- Chart A/B/Cを識別できる
- 回答ボタンが4つ表示される
- 「現金保有」が表示される
- Widgetが責務分離されている
- Questionモデルを利用して画面表示している
- flutter analyze が成功する
- flutter test が成功する
- HomeScreenから問題画面へ遷移できる

## 動作確認

- ホーム画面から問題画面へ遷移できる
- ChartCard が3枚表示される
- ボタンが4つ表示される
- 画面サイズを変更しても崩れない
- エラーなく起動する
- HomeScreenへ戻れる
- flutter test が成功する
- Overflowが発生しない

## 完了条件

- 受け入れ条件をすべて満たす
- 実装内容をレビューする
- Gitへコミット・Pushする