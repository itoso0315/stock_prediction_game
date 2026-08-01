# TASK 009 - 結果画面を独立させる

## 1. Taskの目的

Sprint2の最初のTaskとして、問題画面と結果画面を分離する。

現在は回答確定後、同じ画面の下部に正解・騰落率・将来チャートが追加表示されるため、次の点が分かりにくい。

- どこまでが出題画面か
- どこからが答え合わせか
- どの情報を見て判断したのか
- どのタイミングで結果画面へ切り替わったのか

Task009では、回答確定後に問題画面から結果画面へ切り替え、正解発表を独立した画面として表示する。

このTaskでは、企業名・証券コード・期間説明はまだ追加しない。

---

## 2. ゴール

アプリに次の2画面を持たせる。

### 問題画面

- Chart A / Chart B / Chart Cの表示用チャート
- 各チャートの選択UI
- 選択中のChart表示
- 「回答する」ボタン
- 正解・騰落率・将来チャートは表示しない

### 結果画面

- 正解または不正解
- 利用者の回答ラベル
- 正解Chartラベル
- Chart A / B / Cの将来騰落率
- Chart A / B / Cの将来チャート
- 「次の問題」ボタン
- 問題画面の表示用チャートは表示しない

回答確定後は結果画面へ切り替わり、問題画面と結果画面を同時表示しない。

---

## 3. 画面遷移の方針

Task009では、Streamlitのマルチページ機能や新規ページファイルは使用しない。

`app.py` 内でSession Stateの画面状態を管理し、同一Streamlitページ内の表示分岐として画面遷移を実現する。

新しいSession Stateキー：

```python
st.session_state.current_view
```

保持する値：

```text
"question"
"result"
```

要件：

- 初期値は `"question"`
- 回答前は `"question"`
- 回答確定後は `"result"`
- 「次の問題」成功後は `"question"`
- それ以外の値は使用しない
- ページURLの変更は行わない
- 新しいPythonファイルは作成しない

---

## 4. 実装対象

- `current_view` のSession State追加
- 問題画面と結果画面の描画処理分離
- 回答確定後の結果画面への切り替え
- 結果画面では表示用チャートを非表示
- 結果画面ではTask007の正誤・騰落率・将来チャートを表示
- 結果画面でTask008の「次の問題」ボタンを表示
- 新問題への切り替え成功後に問題画面へ戻す
- 新問題生成失敗時は結果画面を維持
- 既存の4つのSession Stateと問題生成処理を維持
- 既存APIの維持
- エラー時の部分表示防止
- 構文チェック、差分チェック、Streamlit起動確認

---

## 5. 今回の対象外

- Streamlitマルチページ機能
- 新しいページファイルの作成
- URLによるページ遷移
- ブラウザの戻る・進む操作への対応
- 企業名の表示
- 証券コードの表示
- 業種の表示
- 観察期間・予測期間の説明
- 基準日・評価日の表示
- 基準終値・評価終値の表示
- AI解説
- テクニカル指標の解説
- チャート全体をクリックして選択するカードUI
- スコア
- 連勝記録
- ランキング
- 問題履歴
- スマートフォン最適化
- 永続キャッシュ
- ユーザー登録
- ログイン機能
- 自動テストファイルの新規作成

---

## 6. 作成・変更予定のファイル

変更予定：

- `app.py`

既存APIを変更せず利用：

- `game/question_generator.py`
- `ui/charts.py`
- `data/downloader.py`
- `data/nikkei225.py`

新規ファイル作成・削除は予定しない。

---

## 7. Session State

Task008までの状態：

```python
st.session_state.game_question
st.session_state.answer_choice
st.session_state.selected_label
st.session_state.submitted
```

Task009で追加する状態：

```python
st.session_state.current_view
```

### 7.0 既存Session Stateからの移行

Task008以前から継続しているブラウザセッションでは、`current_view` が存在しない場合がある。

`current_view` が存在しない場合は、既存の `submitted` から初期値を決定する。

```text
submitted = False → current_view = "question"
submitted = True  → current_view = "result"
```

新規セッションでは `submitted=False` であるため、初期値は通常どおり `"question"` となる。

### 7.1 初回起動時

```text
game_question = 生成済み問題
answer_choice = None
selected_label = None
submitted = False
current_view = "question"
```

### 7.2 選択中

```text
game_question = 同じ問題
answer_choice = "Chart B"
selected_label = None
submitted = False
current_view = "question"
```

### 7.3 回答確定後

```text
game_question = 同じ問題
answer_choice = "Chart B"
selected_label = "Chart B"
submitted = True
current_view = "result"
```

### 7.4 次の問題への切り替え成功後

```text
game_question = 新しい問題
answer_choice = None
selected_label = None
submitted = False
current_view = "question"
```

### 7.5 次の問題生成失敗後

```text
game_question = 旧問題
answer_choice = 旧選択ラベル
selected_label = 旧回答ラベル
submitted = True
current_view = "result"
```

要件：

- 既存値を初期化処理で上書きしない
- `current_view` が存在しない場合だけ、既存の `submitted` から値を決定する
- `submitted=True` かつ `selected_label` が存在する状態を結果画面とする
- `submitted=False` の状態を問題画面とする
- 画面描画前に `submitted`・`selected_label`・`current_view` の整合性を確認する
- `submitted=True` かつ `selected_label` が存在する場合は、`current_view="result"` に補正する
- `submitted=False` の場合は未回答状態を正とし、`selected_label=None`、`current_view="question"` に補正する。`answer_choice` は現在の選択中ラベルとして保持してよい。
- `submitted=True` かつ `selected_label=None` の場合は不完全な回答状態とみなし、`answer_choice=None`、`selected_label=None`、`submitted=False`、`current_view="question"` へ補正する
- 結果画面で `answer_choice` と `selected_label` が異なる場合は、確定回答である `selected_label` を正とし、`answer_choice` を同じ値へ補正する
- `current_view` が `"question"`・`"result"` 以外の場合は、上記ルールに従って `submitted` と `selected_label` から有効な値へ補正する
- 補正後は `current_view` を画面表示分岐の正とする
- 通常操作では矛盾した組み合わせを作らない

---

## 8. 問題画面

`current_view == "question"` の場合だけ表示する。

表示内容：

```text
Stock Trainer

Chart A
［表示用チャート］
［Chart Aを選ぶ］

Chart B
［表示用チャート］
［Chart Bを選ぶ］

Chart C
［表示用チャート］
［Chart Cを選ぶ］

選択中：Chart B
［回答する］
```

要件：

- Task006までの選択処理を維持する
- Task007の将来Figureを生成しない
- 将来Figure生成処理自体を呼び出さない
- 正解・不正解を表示しない
- 正解ラベルを表示しない
- 将来騰落率を表示しない
- 将来チャートを表示しない
- 「次の問題」ボタンを表示しない

---

## 9. 回答確定と画面切り替え

「回答する」ボタン押下時：

### 未選択の場合

- `1つ選択してください。` を表示する
- `selected_label` は `None` のまま
- `submitted` は `False` のまま
- `current_view` は `"question"` のまま

### 選択済みの場合

次の3状態を一括更新する。

```text
selected_label = answer_choice
submitted = True
current_view = "result"
```

3状態すべての更新完了後に `st.rerun()` を実行する。

要件：

- 回答確定前に結果画面を表示しない
- `st.rerun()` は状態更新後に1回だけ実行する
- 再実行後は問題画面ではなく結果画面へ入る

---

## 10. 結果画面

`current_view == "result"` の場合だけ表示する。

表示順：

```text
Stock Trainer

結果発表

あなたの回答：Chart B
正解：Chart A
不正解

Chart A：+12.34%
［Chart A - Result］

Chart B：-4.56%
［Chart B - Result］

Chart C：+7.89%
［Chart C - Result］

［次の問題］
```

要件：

- 問題画面の表示用Chart A/B/Cを表示しない
- 問題画面の表示用Figure生成処理自体を呼び出さない
- 選択ボタンを表示しない
- 回答ボタンを表示しない
- Task007の正誤判定ロジックを維持する
- Task007の騰落率表示形式を維持する
- Task007の将来チャート表示を維持する
- Task008の「次の問題」ボタンを維持する
- 結果画面に必要な3つの将来Figureをすべて生成してから描画する

---

## 11. 次の問題

結果画面でのみ「次の問題」ボタンを表示する。

Task008の安全な切り替え処理を維持する。

処理順：

1. 新しい `GameQuestion` をローカル変数として生成する
2. 新しい問題の3つの表示用Figureをローカルで事前生成する
3. すべて成功した場合だけSession Stateを更新する
4. 次の値へ一括更新する

```text
game_question = 新しい問題
answer_choice = None
selected_label = None
submitted = False
current_view = "question"
```

5. 更新後に `st.rerun()` を実行する

`st.rerun()` 後の問題画面では、既存仕様どおり表示用Figureを再生成する。

事前生成には成功したものの、再実行後のFigure再生成に失敗した場合は、旧結果画面へロールバックしない。

この場合は以下とする。

- 新しい `game_question` をSession Stateに保持する
- `answer_choice=None`、`selected_label=None`、`submitted=False`、`current_view="question"` を維持する
- 問題画面のチャートを部分表示しない
- 「問題データを生成できませんでした。時間をおいて再度お試しください。」だけを表示する
- 次回の通常再実行では、同じ新しい問題のFigure生成を再試行する

問題生成またはFigure事前生成に失敗した場合：

- 5つのSession Stateを変更しない
- `current_view="result"` を維持する
- 結果画面を維持する
- 「次の問題」ボタンを維持する
- 指定エラーメッセージを追加表示する
- `st.rerun()` を呼び出さない

エラーメッセージ：

```text
問題データを生成できませんでした。時間をおいて再度お試しください。
```

---

## 12. エラー処理

### 問題画面のFigure生成失敗

- 新しい問題への切り替え後に発生した場合も、旧結果画面へ戻さない
- 新しい問題と未回答状態をSession Stateに保持する
- チャートを部分表示しない
- 次のメッセージだけを表示する

```text
問題データを生成できませんでした。時間をおいて再度お試しください。
```

### 結果画面のFigure生成失敗

- 正誤・回答ラベル・正解ラベル・騰落率・将来チャートを部分表示しない
- 次のメッセージだけを表示する

```text
結果を表示できませんでした。時間をおいて再度お試しください。
```

### 次の問題生成失敗

- 現在の結果画面を維持する
- エラーメッセージを結果画面へ追加表示する
- 再度「次の問題」を押せる

---

## 13. app.pyの処理順

1. 既存の4状態を初期化し、`current_view` がない場合は `submitted` から移行値を決定する
2. 5状態の整合性を確認し、不正・矛盾状態を仕様の補正規則に従って正常化する
3. `game_question` が存在しない場合だけ初回問題を生成する
4. `current_view == "question"` の場合は問題画面処理を実行する
5. 問題画面では表示用3Figureをすべて生成してから描画する
6. 回答確定時に回答状態と `current_view="result"` を設定して再実行する
7. `current_view == "result"` の場合は結果画面処理を実行する
8. 結果画面では将来3Figureをすべて生成してから描画する
9. 結果画面の最後に「次の問題」を表示する
10. 次の問題生成成功後に5状態を更新して再実行する
11. 次の問題生成失敗時は結果画面を維持する

---

## 14. 既存APIとの整合性

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

Task009では `app.py` 以外を変更しない。

`app.py` からyfinanceを直接呼び出さない。

---

## 15. 実装手順

1. `current_view` をSession Stateへ追加し、既存セッションでは `submitted` から移行値を決定する
2. 5状態の整合性確認と補正処理を追加する
3. 問題画面の描画処理を分離する
4. 回答確定時に `current_view="result"` を設定する
5. 回答確定後に `st.rerun()` を実行する
6. 結果画面の描画処理を分離する
7. 結果画面から表示用チャートと選択UIを除外する
8. 結果画面に正誤・騰落率・将来チャートを表示する
9. 「次の問題」成功時に `current_view="question"` へ戻す
10. 画面ごとのFigure生成失敗時の挙動を確認する
11. 構文チェック、差分チェック、Streamlit起動確認を行う

---

## 16. 受け入れ条件

以下をすべて満たした場合、Task009を完了とする。

- [ ] `st.session_state.current_view` が追加されている
- [ ] Task009で追加するSession Stateキーは `current_view` だけである
- [ ] 初期値が `"question"` である
- [ ] 既存セッションで `current_view` がない場合、`submitted=False` なら `"question"`、`submitted=True` なら `"result"` として移行される
- [ ] 不正な `current_view` が有効な値へ補正される
- [ ] `submitted`・`selected_label`・`current_view` の矛盾状態が仕様どおり補正される
- [ ] `submitted=False` の未回答状態では `selected_label=None` に補正される
- [ ] 結果画面で `answer_choice` と `selected_label` が異なる場合、`selected_label` を正として補正される
- [ ] 回答前は問題画面だけが表示される
- [ ] 問題画面に表示用Chart A/B/Cが表示される
- [ ] 問題画面に選択ボタンと回答ボタンが表示される
- [ ] 問題画面に正解・騰落率・将来チャートが表示されない
- [ ] 問題画面では将来Figure生成処理を呼び出していない
- [ ] 未選択回答時に問題画面が維持される
- [ ] 回答確定時に `current_view="result"` となる
- [ ] 回答確定時に `selected_label`・`submitted`・`current_view` が一括更新される
- [ ] 回答確定後に `st.rerun()` が1回だけ呼ばれる
- [ ] 再実行後に結果画面だけが表示される
- [ ] 結果画面に表示用Chart A/B/Cが表示されない
- [ ] 結果画面では表示用Figure生成処理を呼び出していない
- [ ] 結果画面に選択ボタンと回答ボタンが表示されない
- [ ] 結果画面に回答ラベル・正解ラベル・正誤が表示される
- [ ] 結果画面にA/B/Cの騰落率が表示される
- [ ] 結果画面にA/B/Cの将来チャートが表示される
- [ ] 結果画面だけに「次の問題」ボタンが表示される
- [ ] 次の問題生成成功時に `current_view="question"` へ戻る
- [ ] 次の問題生成成功時に回答状態がリセットされる
- [ ] 新問題の未回答画面に旧結果が残らない
- [ ] 次問題切り替え後のFigure再生成失敗時も新問題と未回答状態が保持される
- [ ] Figure再生成失敗後の通常再実行で、同じ `game_question` を使って再試行する
- [ ] 次問題切り替え後のFigure再生成失敗時に旧結果画面へ戻らない
- [ ] 次の問題生成失敗時は結果画面を維持する
- [ ] 次の問題生成失敗時に5つのSession Stateがすべて不変である
- [ ] 次の問題生成失敗時に `st.rerun()` を呼び出していない
- [ ] 問題画面のFigure生成失敗時に部分表示されない
- [ ] 結果画面のFigure生成失敗時に部分表示されない
- [ ] `app.py` 以外のファイルを変更していない
- [ ] 既存公開APIが維持される
- [ ] `app.py` からyfinanceを直接importしていない
- [ ] 自動テストファイルを新規作成していない
- [ ] Python構文チェックが成功する
- [ ] `git diff --check` が成功する
- [ ] Streamlitが正常起動する

---

## 17. 動作確認

1. 初回起動時に問題画面だけが表示されること
2. 問題画面にChart A/B/Cと選択UIが表示されること
3. 問題画面に正解・騰落率・将来チャートがないこと
4. 未選択で回答した場合に問題画面が維持されること
5. 選択済みで回答した場合に結果画面へ切り替わること
6. 結果画面に表示用チャートがないこと
7. 結果画面に選択ボタン・回答ボタンがないこと
8. 結果画面に正誤・回答・正解ラベルがあること
9. 結果画面にA/B/Cの騰落率と将来チャートがあること
10. 結果画面に「次の問題」があること
11. 「次の問題」で新しい未回答画面へ戻ること
12. 新問題画面に旧正誤・旧騰落率・旧将来チャートが残らないこと
13. 次の問題生成失敗時に旧結果画面とボタンが残ること
14. 問題画面のFigure生成失敗時に部分表示されないこと
15. 結果画面のFigure生成失敗時に部分表示されないこと
16. `current_view` が通常操作で `"question"` または `"result"` のみになること
17. Git差分が `app.py` だけであること
18. `app.py` にyfinanceの直接importがないこと
19. 既存公開APIが維持されていること
20. Python構文チェックが成功すること
21. `git diff --check` が成功すること
22. Streamlitが正常起動すること
23. Task008由来の `current_view` がない未回答Session Stateが `"question"` へ移行されること
24. Task008由来の `current_view` がない回答済みSession Stateが `"result"` へ移行されること
25. 不正な `current_view` が有効な値へ補正されること
26. `submitted=True` かつ `selected_label=None` の不完全状態が未回答の問題画面へ補正されること
27. `submitted=False` かつ `current_view="result"` が問題画面へ補正されること
28. 結果画面で `answer_choice` と `selected_label` が異なる場合、確定回答へ統一されること
29. 回答確定時に3状態がすべて更新された後でだけ `st.rerun()` が呼ばれること
30. 次問題の事前Figure生成成功後、再実行時のFigure生成だけ失敗した場合に新問題と未回答状態が保持されること
31. 上記再生成失敗時に旧結果画面へ戻らず、問題用エラーメッセージだけが表示されること
32. `submitted=False` かつ `selected_label` が設定済みの状態で、`selected_label=None`、`current_view="question"` へ補正されること
33. 上記補正時に `answer_choice` が選択中ラベルとして保持可能であること
34. 問題画面で将来Figure生成処理が呼び出されないこと
35. 結果画面で表示用Figure生成処理が呼び出されないこと
36. 次問題生成失敗時に5つのSession Stateがすべて不変であること
37. 次問題生成失敗時に `st.rerun()` が呼び出されないこと
38. Figure再生成失敗後の通常再実行で、同じ新問題を使ってFigure生成が再試行されること
39. Task009で `current_view` 以外の新しいSession Stateキーが追加されていないこと

---

## 18. 残課題

Task010では、結果画面に以下を追加する予定とする。

- 観察期間の開始日・終了日
- 予測期間の開始日・終了日
- 「過去60共通取引日を見て、次の60共通取引日を予測した」ことの説明
- 騰落率が基準日終値と評価日終値の比較であることの明示
- 基準終値・評価終値

Task011では、回答後に企業名・証券コード・業種を公開する予定とする。

Task012以降では、チャートを判断するための指標解説やAI解説を追加する予定とする。

将来のUI/UX改善Taskでは、チャート全体をカードとして選択できるUIを検討する。