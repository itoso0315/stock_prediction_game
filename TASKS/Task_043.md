# Task 043: Flutter HTTP API Repository

## 目的
FlutterアプリからFastAPIバックエンドへアクセスするためのRepository層を追加する。

## 実装内容
- `frontend/pubspec.yaml` に `http` パッケージを追加する。
- `frontend/lib/repositories/question_api_repository.dart` を新規作成する。
- `frontend/test/question_api_repository_test.dart` を新規作成する。
- APIエンドポイント `/api/questions` を取得できるRepositoryを実装する。
- 現時点では `QuestionScreen` の取得元は変更しない。
- `flutter analyze` と `flutter test` が成功する状態にする。

## 完了条件
- HTTP通信Repositoryが追加されている。
- Unit Testが追加されている。
- `flutter analyze` が成功する。
- `flutter test` が成功する。
- 既存UIの挙動に変更がない。
