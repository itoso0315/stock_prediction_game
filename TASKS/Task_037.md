

# Task 037

## タイトル

問題数表示を実データ件数に統一する

---

## 目的

Flutter版で表示される問題数のズレを修正する。

現在、ダミーデータは3問しかないにもかかわらず、画面によって以下のように表示が混在している。

```text
QuestionScreen: Question 1 / 10
AnswerReviewScreen: 問題 1 / 3
```

この状態はユーザー体験として不自然であり、将来API接続した際にも混乱の原因になる。

本Taskでは、問題数表示を `QuestionRepository` から取得した実データ件数に統一する。

---

## 背景

Task036で、API接続を見据えて `Question` が `Answer` リストを持つ構造へ拡張された。

次に整えるべきなのは、問題数の扱いである。

現在は `Question` モデル内の `totalQuestions` に `10` が固定で入っている一方、実際のダミー問題数は3問である。

そのため、以下のようなズレが発生している。

- 問題画面では `Question 1 / 10`
- 結果発表画面では `問題 1 / 3`
- テストでは3問完了で最終結果に進む

API接続後は、APIから取得した問題件数を基準に画面表示する必要がある。

そのため、現時点でも表示上は実データ件数を正とする。

---

## 前提条件

- Task036が完了していること
- `Answer` モデルが存在すること
- `Question` モデルが `List<Answer>` を持っていること
- `QuestionScreen` から `AnswerReviewScreen` に遷移できること
- `AnswerReviewScreen` から次の問題へ進めること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 変更対象

- frontend/lib/screens/question_screen.dart
- frontend/lib/repositories/question_repository.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/models/question.dart
- frontend/lib/screens/answer_review_screen.dart

---

## 変更対象外

- HomeScreen
- ResultScreenの大幅なUI変更
- Answerモデルの追加拡張
- API通信
- Pythonコード
- FastAPI
- 本物の株価取得
- チャート描画の本格実装
- 10問化

---

## 現在の問題点

現在の `QuestionRepository` では、各Questionに以下のような固定値が入っている。

```dart
totalQuestions: 10,
```

一方で、実際に返しているQuestionは3件のみである。

そのため、画面によって表示が食い違う。

```text
Question 1 / 10
問題 1 / 3
```

ユーザーは3問しか解いていないのに、問題画面では10問あるように見える。

これは良くない。

---

## 実装方針

問題数表示は、現在取得しているQuestionリストの件数を正とする。

つまり、現時点では以下の表示に統一する。

```text
Question 1 / 3
問題 1 / 3
Question 2 / 3
問題 2 / 3
Question 3 / 3
問題 3 / 3
```

---

## 実装内容

### 1. QuestionScreenの表示修正

QuestionScreenのAppBar表示で、`question.totalQuestions` に依存しすぎないようにする。

現在の想定：

```dart
Question ${question.currentNumber} / ${question.totalQuestions}
```

変更後の想定：

```dart
Question ${_currentIndex + 1} / ${_questions.length}
```

これにより、実際に取得している問題数と表示が一致する。

---

### 2. QuestionRepositoryのtotalQuestions整理

`QuestionRepository` のダミーデータで、`totalQuestions: 10` となっている箇所を、現在の実データ数に合わせる。

現時点では3問のため、以下にする。

```dart
totalQuestions: 3,
```

ただし、将来的に10問化するTaskでは、ここを10問の実データに合わせて変更する。

---

### 3. テスト修正

Widgetテスト内の期待値を、実データ件数に合わせる。

現在のような期待値があれば修正する。

```dart
expect(find.text('Question 1 / 10'), findsOneWidget);
expect(find.text('Question 2 / 10'), findsOneWidget);
expect(find.text('Question 3 / 10'), findsOneWidget);
```

変更後：

```dart
expect(find.text('Question 1 / 3'), findsOneWidget);
expect(find.text('Question 2 / 3'), findsOneWidget);
expect(find.text('Question 3 / 3'), findsOneWidget);
```

---

## API接続後の考え方

API接続後は、APIから返ってきた問題配列の件数を正とする。

例えばAPIが10問返す場合：

```text
Question 1 / 10
問題 1 / 10
```

APIが5問返す場合：

```text
Question 1 / 5
問題 1 / 5
```

Flutter側で固定値を持ちすぎず、取得済みデータの件数を基準にする。

---

## テスト仕様

以下を確認する。

- HomeScreenからQuestionScreenへ遷移できる
- QuestionScreenで `Question 1 / 3` が表示される
- 1問回答後、AnswerReviewScreenで `問題 1 / 3` が表示される
- `次の問題へ` 押下後、QuestionScreenで `Question 2 / 3` が表示される
- 2問回答後、AnswerReviewScreenで `問題 2 / 3` が表示される
- 3問回答後、AnswerReviewScreenで `問題 3 / 3` が表示される
- 最終問題後、ResultScreenへ進める
- flutter analyze成功
- flutter test成功

---

## 受け入れ条件

- `Question 1 / 10` のような実データ件数とズレた表示が出ない
- QuestionScreenとAnswerReviewScreenの問題数表示が一致している
- 現在のダミーデータ3問に対して `1 / 3`、`2 / 3`、`3 / 3` と表示される
- 次の問題へ進む挙動が壊れていない
- 最終結果へ進む挙動が壊れていない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- `ゲーム開始` 押下
- QuestionScreenで `Question 1 / 3` を確認
- 回答カード選択
- `回答する` 押下
- AnswerReviewScreenで `問題 1 / 3` を確認
- `次の問題へ` 押下
- QuestionScreenで `Question 2 / 3` を確認
- 最終問題まで回答
- AnswerReviewScreenで `問題 3 / 3` を確認
- `最終結果を見る` 押下
- ResultScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push