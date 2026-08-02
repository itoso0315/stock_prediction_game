

# Task 019

## 対象

Frontend（Flutter）

## 目的

ホーム画面から問題画面へ遷移できるFlutterアプリの土台を構築する。

## 背景

Task018でFlutter開発環境の構築とホーム画面の作成が完了した。
Task019では責務分離を開始し、画面遷移を実装する。

## 実装内容

- HomeScreenを独立ファイルへ分離
- QuestionScreenを新規作成
- screensフォルダを利用した画面管理
- 「ゲーム開始」ボタンからQuestionScreenへ画面遷移
- main.dartはアプリ起動とルーティングのみを担当

## 変更対象

- frontend/lib/main.dart
- frontend/lib/screens/home_screen.dart
- frontend/lib/screens/question_screen.dart

## 変更対象外

- Pythonコード
- API通信
- チャート描画
- yfinance
- 問題生成ロジック

## 完了条件

- ホーム画面が表示される
- 「ゲーム開始」を押すとQuestionScreenへ遷移する
- QuestionScreenが表示される
- flutter analyze が成功する
- 既存のホーム画面デザインを維持する