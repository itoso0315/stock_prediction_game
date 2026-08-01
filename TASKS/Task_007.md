# TASK 007 - 正解発表と将来結果を表示する

## 1. Taskの目的

Task006で確定した利用者の回答と、Task005で保持している `GameQuestion.correct_label` を比較し、正解・不正解と各Chartの将来結果を表示する。

Task007では、回答後に初めて正解情報を公開する。

利用者が「どのチャートが最も上昇したか」を確認できるようにし、チャート予測ゲームとして1問分の答え合わせを成立させる。

---

## 2. ゴール

回答確定後に、以下を画面へ表示できること。

- 正解または不正解
- 利用者が選択したChartラベル
- 正解Chartラベル
- Chart A / Chart B / Chart Cそれぞれの将来60営業日後の騰落率
- 各Chartの基準日の次の共通取引日から評価日までの将来チャート

回答確定前は、Task006までと同様に正解や将来情報を表示しない。

---

## 3. 実装対象

- `selected_label` と `correct_label` の比較
- 正解・不正解の表示
- 利用者の回答ラベル表示
- 正解Chartラベル表示
- 各Chartの将来騰落率表示
- 各Chartの将来データ表示
- 将来チャートの生成
- 回答前後で表示内容を切り替える処理
- 回答済み問題をSession Stateから再利用
- 既存の問題生成APIとチャート生成APIの再利用
- エラー時の部分表示防止
- 型ヒントとDocstringの維持
- 構文チェックとStreamlit起動確認

---

## 4. 今回の対象外

- 次の問題ボタン
- Session Stateのリセット
- スコア
- 連勝記録
- ランキング
- 問題履歴
- AI解説
- 移動平均線
- ボリンジャーバンド
- RSI
- UIデザインの大幅な作り込み
- チャート全体をクリックして選択するカードUI
- スマートフォン最適化
- 永続キャッシュ
- ユーザー登録
- ログイン機能
- 自動テストファイルの新規作成

---

## 5. 作成・変更予定のファイル

変更予定：

- `app.py`
- `game/question_generator.py`

既存APIを利用：

- `data/downloader.py`
- `data/nikkei225.py`
- `ui/charts.py`

---

## 6. 将来表示用データ

Task005の `ChartQuestion` は、評価日と将来終値は保持しているが、将来チャート全体は保持していない。

Task007では、各Chartについて以下の期間を将来表示用データとする。

- 基準日の次の共通取引日を1日目とする
- 評価日を60日目とする
- 合計60共通取引日分のOHLCVデータ

将来表示用データは、3銘柄すべてで完全に同じ日付インデックスを持つこと。

---

## 7. 問題データ構造の拡張

`ChartQuestion` に、将来表示用データを保持するフィールドを追加する。

追加フィールド：

```python
future_data: pd.DataFrame
```

要件：

- `future_data` は評価対象となる60共通取引日分のみを保持する
- 3つの `future_data` の日付インデックスは完全に一致する
- `future_data.index[-1]` は `evaluation_date` と一致する
- `future_data.iloc[-1]["Close"]` は `future_close` と一致する
- `future_data` は入力DataFrameから独立した `copy(deep=True)` とする
- `ChartQuestion` の既存フィールドは削除・改名しない
- `GameQuestion` の既存構造は維持する
- `frozen=True` を維持する

Task007では、既存の `generate_game_question()` を拡張し、`future_data` を設定する。

`future_data` の追加に伴う `ChartQuestion` コンストラクタのシグネチャ変更は、Task007で明示的に許容する。

既存フィールドの削除・改名は行わないが、`future_data` は必須フィールドとして追加し、デフォルト値は設定しない。

---

## 8. 将来チャート

将来チャートは、Task004のローソク足＋出来高チャートと同じ形式を使用する。

表示対象：

- 上段：将来60共通取引日のローソク足
- 下段：同期間の出来高
- 共有X軸
- 非取引日をX軸上の空白として表示しない
- レンジスライダー非表示

既存の `create_candlestick_chart()` を再利用する。

将来チャートのタイトル：

```text
Chart A - Result
Chart B - Result
Chart C - Result
```

会社名、証券コード、ティッカーは表示しない。

---

## 9. 正誤判定

回答済みの場合、次の比較を行う。

```python
is_correct = (
    st.session_state.selected_label
    == st.session_state.game_question.correct_label
)
```

要件：

- `selected_label` が `correct_label` と一致すれば正解
- 一致しなければ不正解
- 正解判定は `submitted=True` の場合だけ行う
- 回答前は `correct_label` を参照して画面表示しない

表示文言：

正解時：

```text
正解！
```

不正解時：

```text
不正解
```

回答ラベル：

```text
あなたの回答：Chart B
```

正解ラベル：

```text
正解：Chart A
```

---

## 10. 騰落率表示

回答後に、Chart A/B/Cの将来60営業日後の騰落率を表示する。

表示例：

```text
Chart A：+12.34%
Chart B：-4.56%
Chart C：+7.89%
```

要件：

- 表示順はChart A / Chart B / Chart C
- 表示時は小数第2位まで丸める
- 正の値には `+` を付ける
- 負の値には `-` をそのまま表示する
- 小数第2位へ丸めた結果が0になる場合は、元の符号に関係なく `0.00%` と表示する
- 内部の `future_return_percent` 自体は丸めない
- 正解Chartだけが分かる表示は許容する
- 色分けや装飾はTask007では任意とする

---

## 11. 画面仕様

### 11.1 回答前

Task006の画面を維持する。

- Chart A/B/Cの表示用チャート
- 各チャート直下の選択ボタン
- 選択中ラベル
- 回答ボタン

この時点では以下を表示しない。

- 正解・不正解
- 正解ラベル
- 将来騰落率
- 将来終値
- 将来チャート

### 11.2 回答後

表示順は次のとおりとする。

```text
Stock Trainer

［表示用 Chart A］
［表示用 Chart B］
［表示用 Chart C］

あなたの回答：Chart B
正解：Chart A
不正解

Chart A：+12.34%
［Chart A - Result］

Chart B：-4.56%
［Chart B - Result］

Chart C：+7.89%
［Chart C - Result］
```

要件：

- 回答後も元の3チャートを表示し続ける
- 回答後も選択ボタンは無効化された状態で表示する
- 回答ボタンは非表示または無効化する
- 正誤結果を元チャートより後、将来結果より前に表示する
- 将来結果はChart A/B/C順に表示する
- 将来結果をすべて準備してから画面表示する

---

## 12. エラー処理

回答後の画面では、元の表示用チャートと将来チャートを含む必要なFigureをすべて生成してから、画面への描画を開始する。

次の順序で処理する。

1. 3件の `display_data` と `future_data` を確認する
2. 元の3つのFigureをすべて生成する
3. 将来3つのFigureをすべて生成する
4. 全6件のFigure生成に成功した後、元チャート、正誤結果、騰落率、将来チャートを表示する

回答後にいずれかのFigure生成へ失敗した場合、元チャート・正誤結果・騰落率・将来チャートを部分表示しない。

通常画面には次のメッセージだけを表示する。

```text
結果を表示できませんでした。時間をおいて再度お試しください。
```

例外詳細、会社名、証券コード、ティッカーは通常画面へ表示しない。

回答前の元チャート生成に失敗した場合は、Task006までの問題生成エラーメッセージを表示し、チャートを部分表示しない。

---

## 13. Session State

Task006で使用している次の状態を継続利用する。

```python
st.session_state.game_question
st.session_state.answer_choice
st.session_state.selected_label
st.session_state.submitted
```

Task007では新しいSession Stateキーを追加しない。

要件：

- 回答前はTask006と同じ挙動を維持する
- 回答後も同じ `game_question` を使う
- 回答後も `selected_label` と `submitted` を維持する
- 正誤判定結果をSession Stateへ保存しない
- 将来FigureをSession Stateへ保存しない
- Streamlit再実行時は保存済み問題から結果を再構築する

---

## 14. app.pyの処理順

`app.py` は概ね次の順序で処理する。

1. Session Stateを初期化する
2. 初回だけ問題を生成する
3. 未回答の場合は元の3つの表示用Figureをすべて生成する
4. 未回答の場合は元のChart A/B/Cと選択UIを表示し、Task006の回答処理を行う
5. 回答済みの場合は元の3つの表示用Figureをすべて生成する
6. 回答済みの場合は3つの将来Figureをすべて生成する
7. 全6件のFigure生成に成功した後、元のChart A/B/Cを表示する
8. `selected_label` と `correct_label` を比較する
9. 正解・不正解、回答ラベル、正解ラベルを表示する
10. Chart A/B/Cの騰落率と将来チャートを表示する

回答前には手順6以降を実行しない。

---

## 15. 既存APIとの整合性

以下の既存公開要素は削除・改名・シグネチャ変更しない。

- `Question`
- `ChartQuestion`
- `GameQuestion`
- `calculate_return_percent()`
- `generate_question()`
- `generate_game_question()`
- `DISPLAY_TRADING_DAYS`
- `FORECAST_TRADING_DAYS`
- `select_random_tickers()`
- `select_common_window()`
- `normalize_japanese_ticker()`
- `download_daily_prices()`
- `create_candlestick_chart()`

Task007では、`ChartQuestion` に `future_data` フィールドを追加することを許容する。

この追加による `ChartQuestion` コンストラクタのシグネチャ変更は許容する。

`generate_game_question()` の関数名・引数・戻り値は維持する。

`app.py` からyfinanceを直接呼び出さない。

---

## 16. 実装手順

1. `ChartQuestion` に `future_data` を追加する
2. `generate_game_question()` で将来60共通取引日を切り出す
3. `future_data` をディープコピーして保持する
4. `future_data` と既存の評価日・将来終値の整合性を確認する
5. `app.py` で回答済み時だけ正誤判定する
6. 3つの将来Figureを生成する
7. 正解・不正解を表示する
8. 回答ラベルと正解ラベルを表示する
9. 3件の騰落率を表示する
10. 将来チャートをA/B/C順で表示する
11. 回答前は将来情報が表示されないことを確認する
12. エラー時に将来結果が部分表示されないことを確認する
13. 構文チェックとStreamlit起動確認を行う

---

## 17. 受け入れ条件

以下をすべて満たした場合、Task007を完了とする。

- [ ] `ChartQuestion` に `future_data` が追加されている
- [ ] 各 `future_data` が60共通取引日分である
- [ ] 3つの `future_data` の日付インデックスが完全に一致する
- [ ] `future_data.index[-1]` が `evaluation_date` と一致する
- [ ] `future_data` 最終日の終値が `future_close` と一致する
- [ ] `future_data` が入力DataFrameから独立したディープコピーである
- [ ] 回答前は正解・将来情報が表示されない
- [ ] 回答後に正解または不正解が表示される
- [ ] 利用者の回答ラベルが表示される
- [ ] 正解ラベルが表示される
- [ ] Chart A/B/Cの騰落率が表示される
- [ ] 騰落率が小数第2位まで表示される
- [ ] 正の騰落率に `+` が付く
- [ ] 将来チャートがChart A/B/C順で表示される
- [ ] 将来チャートにローソク足と出来高が表示される
- [ ] 将来チャートのX軸に非取引日の空白がない
- [ ] 回答後も元の3チャートが表示される
- [ ] 回答後も選択変更・二重回答ができない
- [ ] 回答後のFigure生成失敗時に、元チャートを含む結果画面全体が部分表示されない
- [ ] 既存公開APIが維持される
- [ ] `app.py` からyfinanceを直接呼び出していない
- [ ] 構文チェックが成功する
- [ ] `git diff --check` が成功する
- [ ] Streamlitが正常に起動する

---

## 18. 動作確認

1. 回答前に正解・騰落率・将来チャートが表示されないこと
2. 正解Chartを選んだ場合に「正解！」と表示されること
3. 不正解Chartを選んだ場合に「不正解」と表示されること
4. 利用者の回答ラベルが正しいこと
5. 正解ラベルが `correct_label` と一致すること
6. 各 `future_data` が60件であること
7. 3つの `future_data` の日付インデックスが完全一致すること
8. 評価日が `future_data` の最終日であること
9. 将来終値が `future_data` 最終日の終値と一致すること
10. `future_data` が入力DataFrameから独立していること
11. Chart A/B/Cの騰落率が計算済み値と一致すること
12. 騰落率の表示形式が仕様どおりであること
13. 将来チャートがA/B/C順に表示されること
14. 将来チャートにローソク足と出来高があること
15. 将来チャートの非取引日が詰めて表示されること
16. 回答後も元チャートが同じ問題のまま表示されること
17. 回答後に選択ボタンが無効であること
18. 回答ボタンが再実行できないこと
19. 回答後のいずれかのFigure生成失敗時に、元チャートを含む結果画面全体が部分表示されないこと
20. 会社名・証券コード・ティッカーが表示されないこと
21. 既存公開APIが維持されていること
22. `app.py` にyfinanceの直接importがないこと
23. Python構文チェックが成功すること
24. `git diff --check` が成功すること
25. Streamlitが正常起動すること

---

## 19. 残課題

Task008では、「次の問題」ボタンを追加し、Session Stateをリセットして新しい問題を生成できるようにする予定とする。

将来のUI/UX改善フェーズでは、チャート全体をカードとして選択できるUIを検討する。

`ChartQuestion` の構造変更後に古いSession Stateが残る開発中のブラウザセッションでは、サーバー再起動またはブラウザセッションの再作成を行う。