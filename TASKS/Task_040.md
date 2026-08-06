

# Task 040

## タイトル

QuestionScreenをローカルJSON Repositoryに切り替える

---

## 目的

Flutter版のQuestionScreenで、固定ダミーデータの `QuestionRepository` ではなく、Task039で作成した `QuestionJsonRepository` から問題データを読み込むようにする。

本Taskでは、まだPython API通信は行わない。

ローカルJSONを実際の画面表示に使うことで、将来API接続する前に、非同期データ読み込み・画面表示・結果発表画面への受け渡しが正しく動くことを確認する。

---

## 背景

Task039で以下が実装された。

- `frontend/assets/sample_questions.json`
- `pubspec.yaml` へのassets登録
- `Answer.fromJson`
- `Question.fromJson`
- `QuestionJsonRepository`
- `QuestionJsonRepository` 専用テスト

これにより、ローカルJSONから `List<Question>` を生成できるようになった。

ただし、現在のQuestionScreenはまだ以下のように固定Repositoryを使っている。

```dart
final _questions = const QuestionRepository().getQuestions();
```

このままだと、JSON読み込みの仕組みはできていても、実際のゲーム画面では使われていない。

本Taskでは、QuestionScreenを `QuestionJsonRepository` ベースに切り替える。

---

## 前提条件

- Task039が完了していること
- `sample_questions.json` が存在すること
- `pubspec.yaml` に `assets/sample_questions.json` が登録されていること
- `Answer.fromJson` が実装されていること
- `Question.fromJson` が実装されていること
- `QuestionJsonRepository` が実装されていること
- `QuestionJsonRepository` のテストが成功していること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/repositories/question_json_repository.dart
- frontend/lib/repositories/question_repository.dart

---

## 変更対象外

- Pythonコード
- FastAPI実装
- HTTP通信
- yfinance取得処理
- 本物の株価取得
- チャート描画の本格実装
- 10問化
- HomeScreenの大幅変更
- ResultScreenの大幅変更
- AnswerReviewScreenの大幅変更
- 新規外部パッケージ追加

---

## 現在の問題点

現在のQuestionScreenは同期的にQuestionリストを取得している。

```dart
final _questions = const QuestionRepository().getQuestions();
```

一方、`QuestionJsonRepository` はassetsを読み込むため、非同期である。

```dart
Future<List<Question>> getQuestions()
```

そのため、単純に以下のようには置き換えられない。

```dart
final _questions = const QuestionJsonRepository().getQuestions();
```

`Future<List<Question>>` を扱うため、QuestionScreenに以下の状態が必要になる。

- 読み込み中
- 読み込み成功
- 読み込み失敗

---

## 実装方針

QuestionScreenを、非同期読み込みに対応させる。

画面状態は以下のようにする。

```text
起動
↓
読み込み中
↓
読み込み成功
↓
Question表示
```

読み込みに失敗した場合は、エラーメッセージを表示する。

```text
問題データを読み込めませんでした
```

---

## 実装内容

### 1. QuestionScreenのRepository切り替え

`QuestionRepository` ではなく、`QuestionJsonRepository` をimportして使う。

変更前：

```dart
import '../repositories/question_repository.dart';
```

変更後：

```dart
import '../repositories/question_json_repository.dart';
```

---

### 2. QuestionScreenの状態管理変更

現在は `_questions` が即時取得される前提になっている。

変更後は以下のような状態を持つ。

```dart
List<Question>? _questions;
bool _isLoading = true;
String? _errorMessage;
```

また、`initState` で読み込み処理を開始する。

```dart
@override
void initState() {
  super.initState();
  _currentIndex = widget.initialIndex;
  _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);
  _loadQuestions();
}
```

---

### 3. _loadQuestionsを追加

`QuestionJsonRepository` から問題を読み込む。

```dart
Future<void> _loadQuestions() async {
  try {
    final questions = await const QuestionJsonRepository().getQuestions();

    if (!mounted) return;

    setState(() {
      _questions = questions;
      _isLoading = false;
    });
  } catch (_) {
    if (!mounted) return;

    setState(() {
      _errorMessage = '問題データを読み込めませんでした';
      _isLoading = false;
    });
  }
}
```

---

### 4. buildの分岐

`build` の先頭で状態分岐する。

```dart
if (_isLoading) {
  return const Scaffold(
    body: Center(child: CircularProgressIndicator()),
  );
}

if (_errorMessage != null) {
  return Scaffold(
    body: Center(child: Text(_errorMessage!)),
  );
}

final questions = _questions!;
final question = questions[_currentIndex];
```

以降は、既存の `_questions` 参照を `questions` に置き換える。

---

### 5. 画面遷移時の注意

現在、AnswerReviewScreenから次の問題へ進むとき、QuestionScreenを再生成している。

```dart
QuestionScreen(
  initialIndex: _currentIndex + 1,
  initialAnswerRecords: _answerRecords,
)
```

この実装のままだと、次の問題へ進むたびにJSONを再読み込みする可能性がある。

MVPでは許容してよい。

理由：

- sample JSONは軽い
- API接続前の段階である
- まずは画面が壊れずに動くことを優先する

ただし、将来的にはゲームセッション単位でQuestionリストを保持する設計に変更する可能性がある。

---

## テスト修正方針

QuestionScreenが非同期読み込みになるため、Widgetテストでは `pumpAndSettle()` を適切に使う。

`ゲーム開始` 押下後、読み込み完了まで待ってから `Question 1 / 3` を確認する。

例：

```dart
await tester.tap(find.text('ゲーム開始'));
await tester.pumpAndSettle();

expect(find.text('Question 1 / 3'), findsOneWidget);
```

既存テストが失敗する場合は、読み込み中状態の1フレームを考慮して修正する。

---

## 受け入れ条件

- QuestionScreenが `QuestionJsonRepository` から問題を読み込んでいる
- `QuestionRepository` の固定ダミーデータに依存していない
- 読み込み中にローディング表示が出る
- 読み込み成功後に `Question 1 / 3` が表示される
- 回答カードを選択できる
- `回答する` 押下後にAnswerReviewScreenへ遷移できる
- AnswerReviewScreenにJSON由来の銘柄名・騰落率が表示される
- `次の問題へ` で次のQuestionScreenへ進める
- 最終問題後にResultScreenへ進める
- 既存のQuestionJsonRepositoryテストが成功する
- 既存のWidgetテストが成功する
- flutter analyze成功
- flutter test成功

---

## 動作確認

```bash
cd ~/Python/stock_prediction_game/frontend
dart format .
flutter analyze
flutter test
```

アプリ起動後、以下を確認する。

```bash
flutter run -d macos
```

確認項目：

- HomeScreen表示
- `ゲーム開始` 押下
- QuestionScreen表示
- `Question 1 / 3` と表示される
- 回答カードを選択
- `回答する` 押下
- AnswerReviewScreen表示
- JSON由来の銘柄名・騰落率が表示される
- `次の問題へ` 押下
- `Question 2 / 3` と表示される
- 最終問題後にResultScreenへ進める

---

## 後続Task案

### Task041

ゲームセッションとしてQuestionリストを保持する設計に改善する。

現在のTask040では、次の問題へ進むたびにJSONを再読み込みする可能性がある。

API接続前に、読み込んだQuestionリストを画面間で持ち回れるようにする。

### Task042

Python側でFastAPIの `/api/questions` を作成する。

### Task043

FlutterからPython APIへHTTP通信で接続する。

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push