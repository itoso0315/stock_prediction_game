

# Task 039

## タイトル

ローカルJSONからQuestionリストを生成する

---

## 目的

Python API接続の前段階として、Flutter側でAPIレスポンス風JSONを読み込み、`Question` / `Answer` モデルへ変換できるようにする。

本Taskでは、まだ本物のAPI通信は行わない。

まずはローカルのサンプルJSONを使い、以下の流れを作る。

```text
ローカルJSON
↓
JSON読み込み
↓
Question / Answer へ変換
↓
QuestionScreen / AnswerReviewScreen / ResultScreenで表示
```

---

## 背景

Task038で、Python APIがFlutterへ返すレスポンス構造を設計した。

しかし、いきなりPython API接続へ進むと、問題が起きたときに原因を切り分けにくい。

例えば以下が同時に混ざってしまう。

- Python API側の問題
- JSON形式の問題
- Flutter側のJSON変換処理の問題
- Flutter画面側の問題
- ネットワーク通信の問題

そのため、本Taskではまず通信を使わず、Flutter内のローカルJSONからQuestionリストを生成できるようにする。

これにより、後続TaskでHTTP APIに切り替える際も、データ取得元だけを差し替えやすくなる。

---

## 前提条件

- Task038が完了していること
- APIレスポンス設計が決まっていること
- `Answer` モデルが存在すること
- `Question` モデルが存在すること
- `QuestionRepository` のダミーデータで画面が動作していること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 変更対象

- frontend/assets/sample_questions.json
- frontend/pubspec.yaml
- frontend/lib/models/answer.dart
- frontend/lib/models/question.dart
- frontend/lib/repositories/question_json_repository.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/repositories/question_repository.dart
- frontend/lib/screens/question_screen.dart

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
- HomeScreenの大幅変更
- ResultScreenの大幅変更

---

## 実装方針

本Taskでは、Task038で設計したAPIレスポンス風のJSONを、Flutterアプリ内のassetsとして配置する。

そのJSONを読み込み、既存の `Question` / `Answer` モデルに変換する。

ただし、いきなり既存の `QuestionRepository` を削除しない。

まずは新しく `QuestionJsonRepository` を作り、既存のRepositoryと切り分ける。

---

## 追加するファイル

### 1. sample_questions.json

以下のファイルを追加する。

```text
frontend/assets/sample_questions.json
```

内容は、Task038で定義したAPIレスポンス風JSONにする。

MVPでは3問分でよい。

---

### 2. QuestionJsonRepository

以下のファイルを追加する。

```text
frontend/lib/repositories/question_json_repository.dart
```

役割：

- assets内のJSONを読み込む
- JSONをdecodeする
- `questions` 配列を `List<Question>` に変換する

想定する構造：

```dart
class QuestionJsonRepository {
  const QuestionJsonRepository();

  Future<List<Question>> getQuestions() async {
    // rootBundle.loadString
    // jsonDecode
    // Question.fromJson
  }
}
```

---

## モデル変更方針

### Answer.fromJson を追加する

`Answer` モデルに `fromJson` を追加する。

想定：

```dart
factory Answer.fromJson(Map<String, dynamic> json) {
  return Answer(
    label: json['label'] as String,
    type: AnswerType.fromJson(json['type'] as String),
    ticker: json['ticker'] as String?,
    companyName: json['companyName'] as String?,
    baseClose: (json['baseClose'] as num?)?.toDouble(),
    evaluationClose: (json['evaluationClose'] as num?)?.toDouble(),
    returnRate: (json['returnRate'] as num?)?.toDouble(),
  );
}
```

### AnswerType.fromJson を追加する

`AnswerType` に変換用メソッドを追加する。

想定：

```dart
extension AnswerTypeJson on AnswerType {
  static AnswerType fromJson(String value) {
    switch (value) {
      case 'stock':
        return AnswerType.stock;
      case 'cash':
        return AnswerType.cash;
      default:
        throw ArgumentError('Unknown answer type: $value');
    }
  }
}
```

実装方法はextensionでもstatic helperでもよい。

---

### Question.fromJson を追加する

`Question` モデルに `fromJson` を追加する。

Task038のAPI設計では `choices` という名前を使っているが、Flutterモデルでは `answers` として扱う。

想定：

```dart
factory Question.fromJson(Map<String, dynamic> json) {
  final answers = (json['choices'] as List<dynamic>)
      .map((choiceJson) => Answer.fromJson(choiceJson as Map<String, dynamic>))
      .toList();

  return Question(
    currentNumber: json['currentNumber'] as int,
    totalQuestions: json['totalQuestions'] as int,
    chartLabels: answers
        .where((answer) => answer.isStock)
        .map((answer) => answer.label)
        .toList(),
    answers: answers,
    correctAnswerLabel: json['correctChoiceLabel'] as String,
  );
}
```

---

## pubspec.yaml変更

assetsを読み込むため、`pubspec.yaml` に以下を追加する。

```yaml
flutter:
  assets:
    - assets/sample_questions.json
```

既に `flutter:` セクションが存在する場合は、既存構造を壊さないように追記する。

---

## 既存Repositoryとの関係

現時点では、`QuestionRepository` をすぐ削除しない。

理由：

- 既存のダミーデータが安定して動いている
- JSON読み込みに失敗したときの切り分けがしやすい
- 段階的に移行した方が安全

本Taskでは、まず `QuestionJsonRepository` のテストを追加し、JSONから `List<Question>` を作れることを確認する。

その後、必要に応じて `QuestionScreen` が `QuestionJsonRepository` を使う形にする。

---

## QuestionScreenへの反映方針

本Taskでは、可能であれば `QuestionScreen` をローカルJSON読み込み対応にする。

ただし、`Future<List<Question>>` になるため、以下の状態を考慮する必要がある。

- 読み込み中
- 読み込み成功
- 読み込み失敗

画面側が複雑になりすぎる場合は、本TaskではRepositoryの実装とテストまでに留めてもよい。

優先順位は以下。

1. JSONからモデル変換できること
2. テストで確認できること
3. 既存画面が壊れないこと
4. 画面がJSON Repositoryを使うこと

---

## テスト仕様

以下を確認する。

- `Answer.fromJson` でstock選択肢を生成できる
- `Answer.fromJson` でcash選択肢を生成できる
- `Question.fromJson` でQuestionを生成できる
- `choices` が `answers` に変換される
- `correctChoiceLabel` が `correctAnswerLabel` に変換される
- `chartLabels` にはstockのChart A/B/Cのみが入る
- 現金保有は `answers` には含まれるが `chartLabels` には含まれない
- `QuestionJsonRepository` から3問取得できる
- flutter analyze成功
- flutter test成功

---

## 受け入れ条件

- `frontend/assets/sample_questions.json` が存在する
- `pubspec.yaml` でsample JSONがassets登録されている
- `Answer.fromJson` が実装されている
- `Question.fromJson` が実装されている
- `QuestionJsonRepository` が実装されている
- ローカルJSONから `List<Question>` を生成できる
- 既存のWidgetテストが壊れていない
- API通信はまだ実装していない
- Pythonコードはまだ変更していない
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

必要に応じてアプリを起動して確認する。

```bash
flutter run -d macos
```

---

## 後続Task案

### Task040

QuestionScreenをローカルJSON Repositoryから読み込む形へ切り替える。

### Task041

Python側でFastAPIの `/api/questions` を作成する。

### Task042

FlutterからPython APIへHTTP通信で接続する。

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push