# Task 021

## タイトル

複数問題データの管理基盤を実装する

---

## 目的

QuestionScreenが固定のダミーデータではなく、複数の問題データの中から1問を表示できる基盤を構築する。

将来的にPython APIから問題データを取得できる設計へ発展しやすい構成とする。

---

## 背景

Task020でQuestionScreenのUIが完成した。

現在はQuestionを1件だけ画面内で生成しているため、ゲームとして問題を切り替えることができない。

本Taskでは複数Questionを管理できる土台を作る。

---

## 前提条件

- Task020が完了していること
- QuestionScreenが正常表示できること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

- Questionデータを複数件保持できるようにする
- QuestionRepositoryを新規作成する
- frontend/lib/repositories/ ディレクトリが存在しない場合は新規作成する
- QuestionScreenはRepositoryから1問取得して表示する
- QuestionScreenのUIは変更しない
- Questionモデルは再利用する

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/models/question.dart
- frontend/lib/repositories/（新規ディレクトリ。存在しない場合のみ作成）
- frontend/lib/repositories/question_repository.dart
- frontend/test/widget_test.dart

---

## 変更対象外

- HomeScreen
- main.dart
- ChartCard
- AnswerButton
- Pythonコード
- API通信
- FastAPI
- yfinance
- 採点機能
- 問題切り替え機能
- 状態管理ライブラリ
- 外部パッケージ

---

## QuestionRepository仕様

QuestionRepositoryはQuestion一覧を保持する。

公開API

- getQuestions()
- getQuestion(int index)

本Taskではダミーデータを3問保持する。

データはconst Questionを利用する。

---

## QuestionScreen仕様

QuestionScreenはRepositoryからindex=0の問題を取得して表示する。

QuestionScreen内でQuestionを生成しない。

QuestionRepository以外から問題データを取得しない。

UIはTask020と同一とする。

---

## 責務分離

QuestionRepository

- 問題一覧を保持する

QuestionScreen

- 問題表示のみ担当

Question

- データのみ保持

---

## 操作仕様

画面の見た目はTask020から変更しない。

回答ボタン動作も変更しない。

---

## テスト仕様

- Repositoryから3件取得できる
- getQuestion(0)でQuestionが取得できる
- HomeScreenからQuestionScreenへ遷移できる
- UIがTask020から変わっていない

---

## 受け入れ条件

- Repositoryが実装されている
- QuestionScreenがRepository経由で表示している
- UIが変化していない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- ゲーム開始
- QuestionScreen表示
- ChartCard3枚
- 回答ボタン4件
- Overflowなし
- HomeScreenへ戻れる

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push