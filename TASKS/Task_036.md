

# Task 036

## タイトル

API接続を見据えてQuestionモデルを拡張する

---

## 目的

Flutter版のデータ構造を、将来のPython API接続に耐えられる形へ近づける。

現在のFlutter版では、回答選択肢を `Chart A`、`Chart B`、`Chart C`、`現金保有` という文字列だけで扱っている。

しかしWeb版や将来のAPI接続後は、各選択肢に以下のような情報が必要になる。

- 表示ラベル
- 銘柄コード
- 銘柄名
- 基準日終値
- 評価日終値
- 騰落率
- 正解かどうか
- チャートデータ
- 出来高データ
- 移動平均線データ

本Taskでは、いきなりAPI通信を実装するのではなく、まずFlutter側のモデルをAPIレスポンスに近い形へ拡張する。

---

## 背景

Task035で、回答後に1問ごとの結果発表画面を表示する流れを追加した。

これにより、Web版に近い以下の流れになった。

```text
QuestionScreen
↓
AnswerReviewScreen
↓
QuestionScreen
↓
AnswerReviewScreen
↓
ResultScreen
```

ただし、現在のFlutter版はまだダミーデータ中心であり、Questionモデルも最低限の情報しか持っていない。

現在のように、選択肢を文字列だけで扱う設計のままAPI接続すると、以下の問題が起きやすい。

- Chart Aに対応する銘柄名を表示できない
- Chart Aに対応する騰落率を表示できない
- 正解チャートの詳細を表示できない
- AnswerReviewScreenにWeb版と同じ情報を渡せない
- ローソク足、出来高、移動平均線データの置き場がない
- APIレスポンスをFlutterのどこに変換すべきか曖昧になる

そのため、API接続前にFlutter側のモデルを整理する。

---

## 前提条件

- Task035が完了していること
- QuestionScreenからAnswerReviewScreenへ遷移できること
- AnswerReviewScreenから次のQuestionScreenへ進めること
- 最終問題後にResultScreenへ進めること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Frontend（Flutter）

---

## 実装内容

Questionモデルを、API接続後に扱いやすい構造へ拡張する。

具体的には、文字列だけの回答選択肢から、選択肢ごとの情報を持つモデルへ移行する。

---

## 変更対象

- frontend/lib/models/question.dart
- frontend/lib/models/answer.dart
- frontend/lib/repositories/question_repository.dart
- frontend/lib/screens/question_screen.dart
- frontend/lib/screens/answer_review_screen.dart
- frontend/lib/screens/result_screen.dart
- frontend/test/widget_test.dart

必要に応じて以下も変更してよい。

- frontend/lib/models/answer_record.dart

---

## 変更対象外

- HomeScreen
- main.dart
- Pythonコード
- API通信
- FastAPI
- yfinance
- 外部パッケージ追加
- 本物の株価取得
- チャート描画の本格実装
- 移動平均線ON/OFFの実装
- 10問化

---

## 現在の問題点

現在のQuestionモデルでは、回答選択肢は主に以下のような文字列で扱われている。

```dart
answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有']
correctAnswerLabel: 'Chart B'
```

この形式はMVPでは分かりやすいが、API接続後には情報が不足する。

Web版の結果発表画面に近づけるには、各選択肢が以下の情報を持つ必要がある。

```text
Chart A
銘柄コード
銘柄名
基準日終値
評価日終値
騰落率
正解かどうか
```

また、将来的には以下も必要になる。

```text
ローソク足データ
出来高データ
MA20
MA40
MA70
Yahoo!ファイナンスリンク
AIひとこと解説
```

---

## 新しいモデル方針

新しく `Answer` モデルを拡張し、選択肢1つ分の情報を持たせる。

想定する構造は以下とする。

```dart
class Answer {
  const Answer({
    required this.label,
    required this.type,
    this.ticker,
    this.companyName,
    this.baseClose,
    this.evaluationClose,
    this.returnRate,
  });

  final String label;
  final AnswerType type;
  final String? ticker;
  final String? companyName;
  final double? baseClose;
  final double? evaluationClose;
  final double? returnRate;
}
```

`AnswerType` は以下を想定する。

```dart
enum AnswerType {
  stock,
  cash,
}
```

---

## Questionモデル方針

Questionモデルは、文字列の回答ラベルではなく、`Answer` のリストを持つ。

想定する構造は以下とする。

```dart
class Question {
  const Question({
    required this.currentNumber,
    required this.totalQuestions,
    required this.answers,
    required this.correctAnswerLabel,
  });

  final int currentNumber;
  final int totalQuestions;
  final List<Answer> answers;
  final String correctAnswerLabel;
}
```

既存コードとの互換性を保つため、一時的に以下のgetterを用意してもよい。

```dart
List<String> get answerLabels => answers.map((answer) => answer.label).toList();
```

これにより、QuestionScreen側の大幅変更を抑えながら段階的に移行できる。

---

## AnswerRecord方針

現時点では、AnswerRecordは既存のままでもよい。

```dart
selectedAnswerLabel: 'Chart A'
```

ただし、将来的には以下のように、選択したAnswer自体やIDを持つ設計へ移行する可能性がある。

```dart
selectedAnswerLabel: 'Chart A'
selectedTicker: '3099'
```

本Taskでは、AnswerRecordの大幅変更は必須にしない。

---

## ダミーデータ方針

QuestionRepositoryのダミーデータを、新しいAnswerモデル形式へ変更する。

例：

```dart
answers: [
  Answer(
    label: 'Chart A',
    type: AnswerType.stock,
    ticker: '3099',
    companyName: '三越伊勢丹ホールディングス',
    baseClose: 2733.5,
    evaluationClose: 2631.5,
    returnRate: -3.73,
  ),
  Answer(
    label: 'Chart B',
    type: AnswerType.stock,
    ticker: '6723',
    companyName: 'ルネサスエレクトロニクス',
    baseClose: 1662.5,
    evaluationClose: 1871.0,
    returnRate: 12.54,
  ),
  Answer(
    label: 'Chart C',
    type: AnswerType.stock,
    ticker: '7186',
    companyName: '横浜フィナンシャルグループ',
    baseClose: 1118.0,
    evaluationClose: 1109.5,
    returnRate: -0.76,
  ),
  Answer(
    label: '現金保有',
    type: AnswerType.cash,
    returnRate: 0,
  ),
]
```

---

## 画面側の方針

QuestionScreenでは、今まで通り `Chart A`、`Chart B`、`Chart C`、`現金保有` を表示できればよい。

本Taskでは、QuestionScreenの見た目を大きく変えない。

AnswerReviewScreenでは、可能であれば以下の情報を追加表示する。

- あなたの回答の銘柄名
- 正解の銘柄名
- 騰落率

ただし、画面が大きく崩れる場合は、まずモデル移行を優先し、表示追加は後続Taskに回してよい。

ResultScreenでは、既存の表示が壊れないことを優先する。

---

## API接続後の想定

将来のPython APIレスポンスは、以下のような構造を想定する。

```json
{
  "currentNumber": 1,
  "totalQuestions": 10,
  "answers": [
    {
      "label": "Chart A",
      "type": "stock",
      "ticker": "3099",
      "companyName": "三越伊勢丹ホールディングス",
      "baseClose": 2733.5,
      "evaluationClose": 2631.5,
      "returnRate": -3.73,
      "candles": [],
      "volumes": [],
      "ma20": [],
      "ma40": [],
      "ma70": []
    }
  ],
  "correctAnswerLabel": "Chart B"
}
```

本TaskではAPI接続は行わないが、Flutter側のモデルはこの構造に近づける。

---

## 移動平均線データ方針

移動平均線データは、将来的にはPython API側で計算してFlutterへ渡す。

Python側では以下のように計算する想定。

```python
df['ma20'] = df['Close'].rolling(window=20).mean()
df['ma40'] = df['Close'].rolling(window=40).mean()
df['ma70'] = df['Close'].rolling(window=70).mean()
```

Flutter側では、ON/OFFに応じて表示を切り替える。

- OFF時：ローソク足と出来高を表示
- ON時：ローソク足、出来高、MA20、MA40、MA70を表示

ただし、本Taskでは移動平均線ON/OFF表示は実装しない。

---

## テスト仕様

既存のWidgetテストが引き続き成功すること。

以下を確認する。

- QuestionRepositoryから取得したQuestionがAnswerリストを持つ
- 各Questionの正解ラベルがAnswerリスト内に存在する
- HomeScreenからQuestionScreenへ遷移できる
- QuestionScreenで回答カードを選択できる
- AnswerReviewScreenへ遷移できる
- AnswerReviewScreenであなたの回答と正解が表示される
- ResultScreenへ遷移できる
- flutter analyze成功
- flutter test成功

---

## 受け入れ条件

- Questionが `Answer` のリストを持つ
- 既存の `answerLabels` 相当の表示が壊れていない
- 正解判定が壊れていない
- QuestionScreenが表示できる
- AnswerReviewScreenが表示できる
- ResultScreenが表示できる
- API接続後に銘柄名・騰落率などを追加しやすい構造になっている
- 文字列だけに依存しすぎた設計から一歩進んでいる
- 外部API通信はまだ実装していない
- flutter analyze成功
- flutter test成功

---

## 動作確認

- HomeScreen表示
- `ゲーム開始` 押下
- QuestionScreen表示
- 回答カード選択
- `回答する` 押下
- AnswerReviewScreen表示
- `次の問題へ` 押下
- 次のQuestionScreen表示
- 最終問題まで回答
- `最終結果を見る` 押下
- ResultScreen表示
- `ホームへ戻る` 押下
- HomeScreen表示

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push