

# Task 041

## タイトル

ゲームセッションとしてQuestionリストを持ち回る

---

## 目的

QuestionScreenで読み込んだ1ゲーム分のQuestionリストを、画面遷移のたびに再読み込みせず、ゲームセッションとして保持して使い回せるようにする。

Task040では、QuestionScreenが `QuestionJsonRepository` からローカルJSONを読み込むようになった。

ただし現在の実装では、AnswerReviewScreenから次の問題へ進むたびに、新しいQuestionScreenを作り直している。

```text
QuestionScreen
↓
AnswerReviewScreen
↓
QuestionScreenを再生成
↓
JSONを再読み込み
```

ローカルJSONでは大きな問題になりにくいが、API接続後は危険である。

本Taskでは、最初に読み込んだQuestionリストを次のQuestionScreenへ渡し、同じ問題セットを使い続けるようにする。

---

## 背景

Task040で、QuestionScreenはローカルJSON Repositoryから非同期で問題を読み込むようになった。

現在は以下が実現できている。

- HomeScreenからQuestionScreenへ遷移できる
- QuestionScreenでJSON由来の問題を表示できる
- 回答後にAnswerReviewScreenへ遷移できる
- AnswerReviewScreenでJSON由来の銘柄名・騰落率を表示できる
- 最終ResultScreenまで遷移できる

一方で、次の問題へ進むたびにQuestionScreenを再生成しているため、API接続後に以下の問題が起きる可能性がある。

- 次の問題へ進むたびにAPIを再取得してしまう
- APIレスポンスが毎回変わる可能性がある
- Q1で解いた問題セットとQ2以降の問題セットがズレる
- 回答履歴と正解データが一致しなくなる
- 通信失敗によりゲーム途中で止まる

そのため、1ゲーム開始時に読み込んだQuestionリストを、ゲーム終了まで保持する必要がある。

---

## 前提条件

- Task040が完了していること
- QuestionScreenが `QuestionJsonRepository` から問題を読み込めること
- AnswerReviewScreenへ遷移できること
- ResultScreenへ遷移できること
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

- frontend/lib/screens/answer_review_screen.dart

---

## 変更対象外

- Pythonコード
- FastAPI実装
- HTTP通信
- yfinance取得処理
- 本物の株価取得
- チャート描画の本格実装
- 10問化
- UIの大幅変更
- 新規外部パッケージ追加

---

## 現在の問題点

現在のQuestionScreenは、初期化時に毎回Questionリストを読み込む。

```dart
@override
void initState() {
  super.initState();
  _currentIndex = widget.initialIndex;
  _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);
  _loadQuestions();
}
```

さらに、AnswerReviewScreenから次の問題へ進むときに、QuestionScreenを再生成している。

```dart
QuestionScreen(
  initialIndex: _currentIndex + 1,
  initialAnswerRecords: _answerRecords,
)
```

このため、次の問題へ進むたびに `_loadQuestions()` が走る。

ローカルJSONでは許容できるが、API接続後は良くない。

---

## 実装方針

QuestionScreenに、既に読み込んだQuestionリストを外から渡せるようにする。

```dart
final List<Question>? initialQuestions;
```

最初のQuestionScreenでは `initialQuestions` がnullのため、Repositoryから読み込む。

次のQuestionScreenへ進むときは、現在保持しているQuestionリストを渡す。

```dart
QuestionScreen(
  initialIndex: _currentIndex + 1,
  initialAnswerRecords: _answerRecords,
  initialQuestions: questions,
)
```

これにより、2問目以降はJSONを再読み込みせず、同じQuestionリストを使える。

---

## 実装内容

### 1. QuestionScreenにinitialQuestionsを追加

QuestionScreenのコンストラクタに以下を追加する。

```dart
this.initialQuestions,
```

フィールドも追加する。

```dart
final List<Question>? initialQuestions;
```

---

### 2. initStateの読み込み処理を分岐する

`initialQuestions` が渡されている場合は、それを使う。

```dart
@override
void initState() {
  super.initState();
  _currentIndex = widget.initialIndex;
  _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);

  final initialQuestions = widget.initialQuestions;

  if (initialQuestions != null) {
    _questions = initialQuestions;
    _isLoading = false;
    return;
  }

  _loadQuestions();
}
```

---

### 3. 次のQuestionScreenへquestionsを渡す

`_goToNextFromReview` の次の問題へ進む処理で、現在のQuestionリストを渡す。

```dart
QuestionScreen(
  initialIndex: _currentIndex + 1,
  initialAnswerRecords: _answerRecords,
  initialQuestions: questions,
)
```

---

### 4. ResultScreenにも同じquestionsを渡す

これはTask040で既にできている可能性が高い。

```dart
ResultScreen(
  answerRecords: _answerRecords,
  questions: questions,
)
```

この形を維持する。

---

## テスト方針

既存Widgetテストが引き続き成功すること。

また、必要に応じて以下を確認する。

- 1問目表示時に読み込みが完了する
- 2問目以降も同じQuestionリストで表示できる
- AnswerReviewScreenから次の問題へ進める
- 最終ResultScreenに同じQuestionリストが渡る

---

## 受け入れ条件

- QuestionScreenが `initialQuestions` を受け取れる
- 初回表示時はRepositoryからQuestionリストを読み込む
- 2問目以降は受け取ったQuestionリストを使う
- 次の問題へ進むたびにRepository再取得へ依存しない
- AnswerReviewScreenへの遷移が壊れていない
- ResultScreenへの遷移が壊れていない
- 既存のWidgetテストが成功する
- 既存のQuestionJsonRepositoryテストが成功する
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
- QuestionScreenで `Question 1 / 3` が表示される
- 回答後、AnswerReviewScreenへ進む
- `次の問題へ` 押下
- QuestionScreenで `Question 2 / 3` が表示される
- 同じゲームセットの問題として結果発表まで進める
- 最終ResultScreenまで進める

---

## 後続Task案

### Task042

最終ResultScreenを学習向けサマリー画面に整理する。

### Task043

Python側でFastAPIの最小構成を作る。

### Task044

Python APIでsample_questions.json相当の固定JSONを返す。

### Task045

FlutterからPython APIへHTTP接続する。

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push