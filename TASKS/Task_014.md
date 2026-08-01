# Task 014

## タイトル
「どれにも投資しない」を追加し、現金保有を含む4択へ変更する

## 1. 目的

現在のゲームはChart A、Chart B、Chart Cの3択であり、3銘柄すべてが上昇しない場合でも、必ずいずれか1つを選ぶ必要がある。

実際の投資では、魅力的な候補がない場合に「投資しない」「現金で保有する」という判断も重要である。

Task014では、3つのChartに加えて次の4つ目の選択肢を追加する。

```text
どれにも投資しない（現金で保有）
```

3つのChartの将来騰落率がすべて0%以下の場合は、現金で保有した場合の騰落率0%が最も良い結果となるため、「どれにも投資しない（現金で保有）」を正解とする。

これにより、ゲームを単なる上昇銘柄当てではなく、「投資するか、見送るか」まで判断する学習ゲームへ改善する。

---

## 2. ゲームルール

利用者は次の4択から1つを選択する。

```text
Chart A
Chart B
Chart C
どれにも投資しない（現金で保有）
```

現金保有の将来騰落率は常に次とする。

```text
0.00%
```

正解は、Chart A/B/Cの未丸め将来騰落率と、現金保有の0%を比較して決定する。

### Chartが正解になる条件

Chart A/B/Cの最大将来騰落率が0より大きい場合、最大値を持つChartを正解とする。

```text
max(chart_returns) > 0
```

### 現金保有が正解になる条件

Chart A/B/Cの最大将来騰落率が0以下の場合、現金保有を正解とする。

```text
max(chart_returns) <= 0
```

### 判定例1

```text
Chart A：+5.20%
Chart B：-1.50%
Chart C：+2.10%
現金保有：0.00%

正解：Chart A
```

### 判定例2

```text
Chart A：-5.20%
Chart B：-1.50%
Chart C：-2.10%
現金保有：0.00%

正解：どれにも投資しない（現金で保有）
```

### 判定例3

```text
Chart A：0.00%
Chart B：-1.50%
Chart C：-2.10%
現金保有：0.00%

正解：どれにも投資しない（現金で保有）
```

正解判定には表示用に丸めた値ではなく、既存の未丸め`future_return_percent`を使用する。

表示上は`0.00%`でも、内部値が正の値である場合は、そのChartが正解となる。

---

## 3. 正解ラベル

現金保有の選択ラベルは次の固定文字列とする。

```python
CASH_OPTION_LABEL = "どれにも投資しない（現金で保有）"
```

この文字列を、次の用途で共通して使用する。

- 問題画面の選択肢
- `answer_choice`
- `selected_label`
- `correct_label`
- 結果画面の利用者回答
- 結果画面の正解表示

表示上の短縮文言を使用してもよいが、保存・比較には必ず`CASH_OPTION_LABEL`を使用する。

---

## 4. 同率時の扱い

### 複数Chartが同率で最大かつ正の場合

既存どおりChart A、Chart B、Chart Cの順で先に存在するChartを正解とする。

例：

```text
Chart A：+3.00%
Chart B：+3.00%
Chart C：-1.00%

正解：Chart A
```

### 最大Chartと現金保有が同率0%の場合

現金保有を正解とする。

```text
max(chart_returns) == 0
```

の場合は、Chartではなく`CASH_OPTION_LABEL`を正解とする。

---

## 5. 実装対象

- 現金保有の固定ラベル追加
- `generate_game_question()`の正解判定変更
- 3Chartと現金0%を比較するルールの追加
- 問題画面を3択から4択へ変更
- Task013の選択UIへ現金保有カードを追加
- 回答確定時に現金保有を保存可能にする
- 結果画面に現金保有0.00%を追加表示
- 正解が現金保有の場合の正誤表示
- 次問題で4択すべて未選択へ戻す
- 既存のChart A/B/C結果表示・Reviewチャートを維持

---

## 6. 今回の対象外

- 3銘柄のうち少なくとも1つを必ず上昇銘柄にする処理
- 銘柄または期間の再抽選
- 現金以外の資産クラス
- 配当金・金利の考慮
- 売買手数料
- 税金
- 空売り
- 損切り・利確ルール
- 複数銘柄への分散投資
- 投資比率の指定
- AI解説
- テクニカル分析解説
- スコア・履歴
- 結果画面の全面的なデザイン変更
- 自動テストファイルの新規作成

---

## 7. 作成・変更予定ファイル

### 変更予定

- `game/question_generator.py`
- `app.py`

### 変更しない

- `ui/charts.py`
- `data`配下
- `README.md`

### 新規作成

- なし

### 削除

- なし

---

## 8. 問題生成ロジック

`generate_game_question()`で3Chartの`future_return_percent`を計算した後、次のルールで`correct_label`を決定する。

```python
best_chart = max(
    chart_questions,
    key=lambda chart: chart.future_return_percent,
)

if best_chart.future_return_percent <= 0:
    correct_label = CASH_OPTION_LABEL
else:
    correct_label = best_chart.label
```

実際のコードでは既存のデータ構造・変数名に合わせる。

### 維持する処理

- 120共通取引日の観察期間
- 20共通取引日の予測期間
- `base_close`
- `future_close`
- `future_return_percent`
- Chart A/B/Cの並び順
- 同率時のA/B/C先頭優先
- 同一シードによる再現性
- 入力DataFrame非破壊
- 出力DataFrameの独立性

### 変更しない公開API

- `generate_game_question()`の関数名・引数・戻り値
- `GameQuestion`のフィールド
- `ChartQuestion`のフィールド
- `generate_question()`
- `select_common_window()`
- `calculate_return_percent()`

`correct_label`は既存の文字列フィールドをそのまま利用し、新しいフィールドは追加しない。

単一銘柄用`generate_question()`の正解判定や戻り値は変更しない。

---

## 9. 問題画面の4択UI

Task013のChart A/B/Cカードを維持する。

問題画面の表示順は次のとおりとする。

```text
Chart Aカード
Chart Bカード
Chart Cカード
既存の予測説明文
現金保有のルール説明文
どれにも投資しないカード
回答するボタン
```

現金保有カードは、2つの説明文の直後、回答ボタンの直前に表示する。

現金保有カードにはチャートを表示しない。

### 未選択時の表示

```text
○ どれにも投資しない
   現金で保有する（騰落率 0.00%）
```

### 選択中の表示

```text
● どれにも投資しない
   現金で保有する（騰落率 0.00%）
```

ボタンまたはカード内に、次の意味が分かる補足を表示する。

```text
3つとも上昇しないと思う場合はこちら
```

問題画面ではChart A/B/Cの将来騰落率を表示しない。

現金保有の0.00%は固定条件であり、未来情報ではないため問題画面に表示してよい。

---

## 10. 現金保有カードのUI

Task013のカードデザインと統一する。

container keyは次とする。

```text
cash_option_card
```

widget keyは次とする。

```text
select_cash_option
```

選択操作には既存の`select_answer()`を`on_click`コールバックとして使用し、引数に`CASH_OPTION_LABEL`を渡す。

### 未選択カード

- 背景色：`#FFFFFF`
- 枠線：`1px solid #D9E2EC`
- 角丸：`12px`
- 内側余白：`12px`
- カード間余白：`16px`
- 影：`0 2px 8px rgba(15, 23, 42, 0.06)`

### 選択中カード

- 背景色：`#F3F8FF`
- 枠線：`2px solid #4A90E2`
- 角丸：`12px`
- 内側余白：`12px`
- カード間余白：`16px`
- 影：`0 4px 12px rgba(74, 144, 226, 0.15)`

選択状態は既存の`answer_choice`だけを正とする。

Chart A/B/Cまたは現金保有のいずれか1つだけが選択状態になる。

選択操作では明示的な`st.rerun()`を追加しない。

---

## 11. 問題画面の説明文

既存の次の説明文は維持する。

```text
📈 あなたが利用できる情報はここまでです。この先約1か月（20共通取引日）の値動きを予測してください。
```

その直後に、次の説明を追加する。

```text
3つとも上昇しないと予想する場合は、「どれにも投資しない（現金で保有）」を選択してください。
```

この説明文はChartの未来情報を含まない。

---

## 12. 回答確定

`answer_choice`の許容値は次の5種類とする。

- `None`
- `Chart A`
- `Chart B`
- `Chart C`
- `CASH_OPTION_LABEL`

回答確定処理はTask013までの既存処理を維持する。

回答確定時は既存どおり次を一括更新する。

- `selected_label = answer_choice`
- `submitted = True`
- `current_view = "result"`

更新後に`st.rerun()`を1回だけ呼ぶ。

未選択時の警告文言は維持する。

```text
1つ選択してください。
```

---

## 13. 結果画面

結果画面上部の表示順はTask010〜013の既存順を維持する。

`selected_label`または`correct_label`が現金保有の場合も、固定ラベルをそのまま表示する。

### 共通比較情報

既存のChart A/B/Cの比較に加えて、現金保有を次の固定値で表示する。

```text
現金で保有：0.00%
```

表示位置は、基準日・評価日の共通情報、利用者回答、正解、正誤の後、Chart Aの比較情報より前とする。

### 正解がChartの場合

既存どおりChart A/B/Cの最大正値を持つChartを正解として表示する。

### 正解が現金保有の場合

次を明確に表示する。

```text
3つのChartがすべて0%以下だったため、現金保有が最も良い結果でした。
```

この補足文は、`correct_label == CASH_OPTION_LABEL`の場合だけ表示する。

### Reviewチャート

Chart A/B/CのReviewチャート3件は既存どおり表示する。

現金保有用のチャートは追加しない。

表示順は次とする。

1. 結果発表
2. 基準日・評価日
3. 利用者回答
4. 正解
5. 正誤
6. 現金で保有：0.00%
7. 現金保有正解時の補足文
8. Chart A比較＋Reviewチャート
9. Chart B比較＋Reviewチャート
10. Chart C比較＋Reviewチャート
11. 次の問題

---

## 14. 結果画面の部分表示防止

Task012までの結果Figure事前生成と部分表示防止を維持する。

Review Figure 3件、現金保有0.00%、現金保有正解時の補足文、その他の表示用文字列をすべて準備してから結果画面を描画する。

1件でもFigure生成に失敗した場合は、次を表示しない。

- 結果発表
- 利用者回答
- 正解
- 正誤
- 日付
- 現金保有0.00%
- 現金保有正解時の補足文
- Chart比較情報
- 一部のReview Figure
- 次の問題ボタン

既存の結果用エラーメッセージだけを表示する。

---

## 15. 次の問題

既存の次問題成功・失敗処理を変更しない。

次問題成功時は既存どおり次へ戻る。

- `game_question = 新しい問題`
- `answer_choice = None`
- `selected_label = None`
- `submitted = False`
- `current_view = "question"`

Chart A/B/Cと現金保有の4択すべてが未選択表示へ戻る。

次問題失敗時は、旧結果画面と4択の回答結果を維持する。

---

## 16. Session Stateとwidget key

新しいアプリ状態用Session Stateキーは追加しない。

既存の状態を維持する。

- `game_question`
- `answer_choice`
- `selected_label`
- `submitted`
- `current_view`

追加するwidget識別用keyは次だけとする。

```text
select_cash_option
```

既存widget keyを維持する。

- `select_chart_a`
- `select_chart_b`
- `select_chart_c`
- `submit_answer`
- `next_question`

widget keyを選択状態の判定に使用しない。

---

## 17. エラー処理

### 問題生成

既存処理を維持する。

3Chartすべてが0以下であってもエラーにしない。

再抽選や自動差し替えを行わない。

### 問題画面Figure

既存どおり、3件すべて生成成功後に4択UIを描画する。

Figure生成失敗時は現金保有カードも表示しない。

### 結果画面Figure

既存どおり、3件すべて生成成功後に結果情報を描画する。

Figure生成失敗時は現金保有情報も部分表示しない。

---

## 18. 既存API・状態との整合性

### 変更しない

- `generate_game_question()`のシグネチャ
- `generate_question()`のシグネチャと挙動
- `select_common_window()`
- `calculate_return_percent()`
- `GameQuestion`
- `ChartQuestion`
- `Question`
- `create_candlestick_chart()`
- `create_review_chart()`
- Task009以降の画面遷移
- Task013の選択UI設計
- `period="5y"`

### 変更する意味上の挙動

- `GameQuestion.correct_label`がChart A/B/Cだけでなく、`CASH_OPTION_LABEL`になる場合がある
- 問題画面の選択肢が3択から4択になる

---

## 19. 実装手順

1. `game/question_generator.py`へ`CASH_OPTION_LABEL`を追加する。
2. 3Chartの最大未丸め騰落率を取得する。
3. 最大値が0以下なら`correct_label=CASH_OPTION_LABEL`とする。
4. 最大値が正なら既存どおり最大Chartを正解とする。
5. `app.py`から`CASH_OPTION_LABEL`をimportする。
6. Task013のCSSへ現金保有カードのcontainer keyを追加する。
7. 3Chartカード後に、既存の予測説明文、現金保有のルール説明文、現金保有カードをこの順で追加する。
8. `select_answer()`の`on_click`で現金保有を選択可能にする。
9. 結果画面へ現金保有0.00%を追加する。
10. 現金保有正解時の補足文を追加する。
11. 既存Review Figure 3件の事前生成を維持する。
12. 次問題で4択すべて未選択へ戻ることを確認する。
13. 現金保有0.00%と現金保有正解時の補足文を、Review Figure 3件と同じく描画前のローカル準備対象へ含める。
14. 構文・差分・Streamlit起動を確認する。

---

## 20. 受け入れ条件

- `CASH_OPTION_LABEL`が固定文字列として定義されている。
- 3Chartの最大未丸め騰落率が正の場合、最大Chartが正解になる。
- 3Chartの最大未丸め騰落率が0以下の場合、現金保有が正解になる。
- 最大値がちょうど0の場合、現金保有が正解になる。
- 表示用に丸めた騰落率ではなく未丸め値で判定する。
- 正の同率最大Chartは既存どおりA/B/C先頭優先になる。
- `generate_game_question()`のシグネチャを変更しない。
- `GameQuestion`と`ChartQuestion`へフィールドを追加しない。
- `generate_question()`の挙動を変更しない。
- `answer_choice`の許容値が`None`、`Chart A`、`Chart B`、`Chart C`、`CASH_OPTION_LABEL`の5種類である。
- 保存・比較には短縮表示ではなく`CASH_OPTION_LABEL`を使用する。
- 問題画面に4つの選択肢が表示される。
- Chart A/B/CのカードUIを維持する。
- 問題画面の表示順が、Chart A、Chart B、Chart C、既存の予測説明文、現金保有のルール説明文、現金保有カード、回答ボタンの順である。
- 現金保有カードが3Chart後、回答ボタン前に表示される。
- 現金保有カードにチャートを表示しない。
- 現金保有カードに0.00%を表示する。
- 現金保有の表示は常に`0.00%`であり、`-0.00%`にならない。
- 現金保有カードに「3つとも上昇しないと思う場合」の意味を表示する。
- 問題画面にChart A/B/Cの将来騰落率を表示しない。
- 問題画面で`future_data`をFigure生成関数へ渡さない。
- 問題画面で`create_review_chart()`を呼び出さない。
- 回答確定時に現金保有を`selected_label`へ保存できる。
- 未選択警告を維持する。
- 結果画面に現金保有0.00%が表示される。
- 結果画面の表示順が、結果発表、基準日・評価日、利用者回答、正解、正誤、現金保有0.00%、現金保有正解時の補足文、Chart A、Chart B、Chart C、次の問題の順である。
- 正解がChartの場合は既存どおりChart A/B/Cの最大正値を持つChartを正解として表示する。
- 現金保有が正解の場合は専用補足文が表示される。
- Chart正解時に専用補足文がない。
- 現金保有が正解でもReviewチャート3件を表示する。
- ReviewチャートはA/B/Cの3件だけである。
- 現金保有用チャートを生成しない。
- 結果Figure事前生成と部分表示防止を維持する。
- 次問題で4択すべて未選択へ戻る。
- 次問題失敗時に旧回答と結果を維持する。
- 新しいアプリ状態用Session Stateキーを追加しない。
- 追加widget keyが`select_cash_option`だけである。
- 3Chartすべて0以下でも再抽選しない。
- 同一入力・同一シードで同じ問題と正解を生成する。
- 入力DataFrameを変更しない。
- 出力DataFrameが入力から独立している。
- `CASH_OPTION_LABEL`を`game/question_generator.py`から`app.py`へimportする。
- `ui/charts.py`と`data`配下を変更しない。
- `app.py`からyfinanceを直接利用しない。
- 自動テストファイルを作成しない。
- Git管理対象のTask014差分が`game/question_generator.py`と`app.py`だけである。
- Python構文チェックが成功する。
- `git diff --check`が成功する。
- Streamlitが正常起動する。

---

## 21. 動作確認

- `CASH_OPTION_LABEL`の文字列が仕様と完全一致する。
- 全Chartが負の場合、現金保有が正解になる。
- 最大Chartが0の場合、現金保有が正解になる。
- 1Chartだけ正の場合、そのChartが正解になる。
- 複数Chartが正の場合、最大Chartが正解になる。
- 正の同率最大がChart BとChart Cの場合にChart Bが正解になる。
- 表示上0.00%でも内部値が正の場合、そのChartが正解になる。
- 内部値が微小な正値で表示が`0.00%`になる場合でもChartが正解になる。
- 内部値が微小な負値で表示が`0.00%`になる場合は現金保有との比較で判定される。
- 3Chartすべて0の場合に現金保有が正解になる。
- 1Chartが0、残りが負の場合に現金保有が正解になる。
- A/B/C/現金保有をそれぞれ選択できる。
- A→現金→Cなど連続選択しても選択表示が常に1件だけである。
- 現金保有選択後にChartへ選び直せる。
- Chart選択後に現金保有へ選び直せる。
- `answer_choice`が仕様で定めた5種類以外にならない。
- 短縮表示ではなく`CASH_OPTION_LABEL`が状態へ保存される。
- 現金保有カードに0.00%と補足文が表示される。
- 問題画面の7要素が仕様どおりの順で表示される。
- 問題画面でChart A/B/Cの将来騰落率が表示されない。
- 問題画面で`future_data`がFigure生成関数へ渡されない。
- 問題画面で`create_review_chart()`が呼ばれない。
- 現金保有の表示が`-0.00%`にならない。
- 現金保有回答を確定できる。
- 現金保有回答時に結果画面へ遷移する。
- 現金保有が正解の場合に正解表示される。
- 現金保有が不正解の場合に不正解表示される。
- 結果画面の11要素が仕様どおりの順で表示される。
- 結果画面に現金保有0.00%が1回だけ表示される。
- 現金保有正解時の補足文が1回だけ表示される。
- Chart正解時に専用補足文がない。
- 現金保有正解時もReview FigureがA/B/Cの3件表示される。
- 現金保有用Figureが生成されない。
- 問題Figure失敗時に現金保有カードが部分表示されない。
- 結果Figure失敗時に現金保有情報と次の問題ボタンが部分表示されない。
- 回答確定時の状態遷移が従来どおりである。
- 次問題で4択すべて未選択になる。
- 次問題失敗時に旧回答と結果を維持する。
- 同一入力・同一シードで同じ問題と正解を生成する。
- 入力DataFrameが変更されない。
- 出力DataFrameが入力から独立している。
- `generate_question()`が従来どおり動作する。
- `select_common_window()`が従来どおり動作する。
- `calculate_return_percent()`が従来どおり動作する。
- `period="5y"`が維持される。
- `ui/charts.py`と`data`配下に差分がない。
- `app.py`にyfinanceの直接importがない。
- 自動テストファイルが作成されていない。
- Python構文チェック成功。
- `git diff --check`成功。
- Streamlit起動成功。

---

## 22. 残課題

今後のTaskで次を検討する。

- 現金保有を選んだ理由を利用者へ入力させる。
- 結果画面で「見送るべきチャート」の特徴を解説する。
- 現金比率や投資比率を選択できるようにする。
- 市場全体の地合いを判断材料へ追加する。
- スコアで「損失回避」を評価する。