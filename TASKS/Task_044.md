

# Task 044: QuestionScreenの問題取得元をHTTP APIへ切り替える

## 目的
FlutterのQuestionScreenが、ローカルJSONではなくFastAPIの `/api/questions` から問題データを取得するように切り替える。

## 現在地
- `QuestionApiRepository` はTask043で実装済み。
- `GET /api/questions` のUnit Testは成功済み。
- `flutter analyze` は成功済み。
- `flutter test` は全件成功済み。
- 現在のQuestionScreenは `QuestionJsonRepository` から問題を取得している。

## 実装内容

### 1. QuestionScreenの取得元をAPIへ切り替える
- `QuestionJsonRepository` の利用をやめる。
- `QuestionApiRepository` を利用する。
- macOSでのローカル確認用ベースURLは `http://127.0.0.1:8000` とする。
- APIエンドポイントは `/api/questions` を利用する。

### 2. Repositoryを外から注入可能にする
- `QuestionScreen` のコンストラクタから `QuestionApiRepository` を渡せるようにする。
- Repositoryが未指定の場合は、`http://127.0.0.1:8000` を使う既定の `QuestionApiRepository` を生成する。
- Widget TestではMockClientを使ったRepositoryを注入できる状態にする。

### 3. initialQuestionsの挙動を維持する
- `initialQuestions` が渡された場合はAPIへ再取得しない。
- Task041で追加した問題データ持ち回りの挙動を壊さない。

### 4. 既存UIを維持する
- 読み込み中表示は現在の仕様を維持する。
- API通信失敗時は、現在のエラー表示を維持する。
- 回答カード、回答ボタン、結果画面、進捗表示などのUIは変更しない。

### 5. テストを更新する
- 既存Widget Testが実APIへ接続しないようにする。
- MockClientを使った `QuestionApiRepository` をQuestionScreenへ注入する。
- 少なくとも以下を確認する。
  - API取得成功時に問題画面が表示される。
  - 回答後に結果画面が表示される。
  - `initialQuestions` がある場合はAPIを呼ばない。
  - API取得失敗時にエラー表示が出る。

## 変更対象
- `frontend/lib/screens/question_screen.dart`
- 必要に応じてQuestionScreenを生成している既存ファイル
- `frontend/test/widget_test.dart`
- 必要に応じてQuestionScreen関連テスト

## 変更しないもの
- `frontend/lib/repositories/question_api_repository.dart` の基本仕様
- `frontend/lib/repositories/question_json_repository.dart`
- `frontend/assets/sample_questions.json`
- 既存の画面デザイン
- Backend側のAPI仕様

## 完了条件
- QuestionScreenがFastAPIの `/api/questions` から問題を取得する。
- `initialQuestions` がある場合はAPIを再取得しない。
- API通信失敗時にアプリがクラッシュしない。
- `flutter analyze` が成功する。
- `flutter test` が全件成功する。
- FastAPI起動中にmacOSアプリで問題画面から結果画面まで操作できる。

## 実装後の確認手順
1. FastAPIを起動する。
2. `http://127.0.0.1:8000/api/health` が `{"status":"ok"}` を返すことを確認する。
3. FlutterをmacOSで起動する。
4. 問題画面が表示されることを確認する。
5. 回答して結果画面まで進めることを確認する。
6. FastAPIを停止した状態でエラー表示を確認する。

## 制約
- Task044の範囲外のリファクタリングをしない。
- UIデザインを変更しない。
- Git commit、Git pushは行わない。