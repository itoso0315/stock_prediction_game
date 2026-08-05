

# Task 032

## タイトル

共通テーマをダーク×ゴールドにする

---

## 目的

Flutterアプリ全体の見た目を、最終イメージである2つ目のモックアップ画像に近づけるため、共通テーマをダーク×ゴールド基調に変更する。

Task030〜031でQuestionScreenの機能と説明文を整えたが、まだFlutter標準UIに近い見た目である。

本Taskでは、アプリ全体の色・ボタン・カード・背景の基本トーンを整え、今後のUI改善の土台を作る。

---

## 背景

Task030で、回答選択肢をカードUIにした。

Task031で、QuestionScreenに説明文と補足文を追加した。

しかし、現状の画面はまだ以下の課題がある。

- 背景色が標準的である
- カード色がモック画像のシックな印象と異なる
- ボタンが標準Flutter感に近い
- ゴールドアクセントがない
- 画面全体の投資アプリらしい落ち着きが弱い

本Taskでは、まず共通テーマを整え、今後HomeScreen / QuestionScreen / ResultScreenをモック寄りに改善しやすくする。

---

## 前提条件

- Task031が完了していること
- HomeScreenからQuestionScreenへ遷移できること
- QuestionScreenでカード選択できること
- 回答ボタンで回答できること
- ResultScreenへ遷移できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- アプリ全体にダークテーマを適用する
- 背景色をチャコール系にする
- カード色を濃いグレー系にする
- 主要アクセント色をゴールド系にする
- FilledButtonの色をゴールド系にする
- AppBarの見た目をダーク基調にする
- 文字色を白〜薄いグレー系にする
- 既存の画面遷移とゲーム進行を維持する
- 既存のテストが通る状態を維持する

---

## 変更対象

- frontend/lib/main.dart
- frontend/test/widget_test.dart

必要に応じて以下を新規作成してよい。

- frontend/lib/theme/app_theme.dart

---

## 変更対象外

- HomeScreenの構成変更
- QuestionScreenの構成変更
- ResultScreenの構成変更
- Questionモデル
- AnswerRecordモデル
- QuestionRepository
- ChartCardのロジック変更
- 回答選択ロジック変更
- 正解数算出ロジック変更
- 正答率算出ロジック変更
- ランク算出ロジック変更
- Pythonコード
- API通信
- FastAPI
- yfinance
- 外部パッケージ追加

---

## デザイン方針

最終的には、2つ目のモックアップ画像のようなスマホアプリUIを目指す。

方向性は以下とする。

- シック
- ダーク/チャコール基調
- ゴールドアクセント
- 高級感のある投資アプリ風
- 角丸カード
- 落ち着いた文字色
- 派手すぎないコントラスト

---

## 色方針

厳密な色指定は今後調整してよいが、本Taskでは以下の方向にする。

```text
背景        : チャコール / ほぼ黒
カード      : 濃いグレー
アクセント  : ゴールド
主要文字    : 白
補助文字    : 薄いグレー
枠線        : 暗めのグレー
```

---

## テーマ仕様

可能であれば `ThemeData` を整理する。

以下を設定する。

- `brightness: Brightness.dark`
- `scaffoldBackgroundColor`
- `colorScheme`
- `appBarTheme`
- `cardTheme`
- `filledButtonTheme`
- `textTheme`

実装が長くなりすぎる場合は、`frontend/lib/theme/app_theme.dart` を作成し、テーマ定義を分離してよい。

---

## 表示仕様

既存画面の表示内容は維持する。

HomeScreenでは以下が維持されること。

- `Stock Trainer`
- `ゲーム開始`

QuestionScreenでは以下が維持されること。

- `Question 1 / 10`
- 説明文
- 補足文
- Chart A / Chart B / Chart C / 現金保有
- `回答する`

ResultScreenでは以下が維持されること。

- `結果発表`
- `回答数: 3件`
- `正解数: 1問`
- `正答率: 33%`
- `ランク: C`
- 回答結果一覧
- `ホームへ戻る`

---

## 操作仕様

操作仕様はTask031から変更しない。

- HomeScreenからゲーム開始できる
- QuestionScreenでカード選択できる
- 回答ボタンで次のQuestionへ進める
- 最後のQuestion回答後にResultScreenへ遷移する
- ResultScreenからHomeScreenへ戻れる

---

## テスト仕様

既存のWidgetテストが引き続き成功すること。

本Taskでは主にテーマ変更を行うため、新しい操作テストの追加は必須としない。

ただし、必要に応じて以下を確認してよい。

- HomeScreenが表示される
- QuestionScreenが表示される
- ResultScreenが表示される
- 既存のテキストが表示される
- ボタン操作が維持される

---

## 受け入れ条件

- アプリ全体がダーク基調になっている
- 主要アクセントがゴールド系になっている
- FilledButtonがゴールド系になっている
- Cardがダーク基調になっている
- AppBarがダーク基調になっている
- 既存の表示文言が維持されている
- 既存のゲーム進行が壊れていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- 背景がダーク基調になっていることを確認
- `ゲーム開始` ボタンがゴールド系になっていることを確認
- ゲーム開始
- QuestionScreen表示
- カードがダーク基調になっていることを確認
- 選択中カードのアクセントが分かることを確認
- 回答ボタンがゴールド系になっていることを確認
- 3問回答
- ResultScreen表示
- ResultScreenもダーク基調で表示されることを確認
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push