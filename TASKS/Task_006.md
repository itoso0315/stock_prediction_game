# TASK 006 - 回答UIと問題保持を実装する

## 1. Taskの目的

利用者が `Chart A / Chart B / Chart C` の中から、将来最も上昇すると考えるチャートを1つ選択し、回答を確定できるようにする。

Task005で生成した `GameQuestion` を `st.session_state` に保持し、Streamlitの再実行が発生しても同じ問題が表示され続ける状態を実現する。

Task006では、正解・不正解、将来騰落率、将来チャートは表示しない。

---

## 2. ゴール

1問を固定したまま、利用者がChart A/B/Cから1つを選択し、回答を確定できること。

回答確定後は、以下の状態を維持する。

- 同じ問題が表示され続ける
- 選択したChartラベルが保持される
- 回答済み状態が保持される
- 選択内容を変更できない
- 回答ボタンを再度実行できない
- 正解や将来情報はまだ表示されない

---

## 3. 実装対象

- `st.session_state` による問題保持
- 初回のみ `GameQuestion` を生成する処理
- Chart A/B/Cの選択UI
- 選択中のChartが分かる表示
- 「回答する」ボタン
- 未選択時の警告表示
- 回答内容の保持
- 回答済み状態の保持
- 回答後の選択変更防止
- 回答後の二重回答防止
- 回答後も問題を再生成しない処理
- 問題生成失敗時の利用者向けエラー表示
- Task005の問題生成APIとTask004のチャート生成APIの再利用
- 型ヒントとDocstringの維持
- 構文チェックとStreamlit起動確認

---

## 4. 今回の対象外

- 正解表示
- 不正解表示
- `correct_label` の画面表示
- 将来騰落率の画面表示
- 将来チャートの表示
- 証券コード・会社名の公開
- 次の問題ボタン
- スコア
- ランキング
- 連勝記録
- 問題履歴
- 制限時間
- AI解説
- 移動平均線
- ボリンジャーバンド
- UIデザインの作り込み
- スマートフォン最適化
- 永続キャッシュ
- ユーザー登録
- ログイン機能
- 自動テストファイルの新規作成

---

## 5. 作成・変更予定のファイル

変更予定：

- `app.py`

既存APIを変更せず利用：

- `game/question_generator.py`
- `ui/charts.py`
- `data/downloader.py`
- `data/nikkei225.py`

新規ファイル作成・削除は予定しない。

---

## 6. Session State

`app.py` で、次の状態を保持する。

```python
st.session_state.game_question
st.session_state.selected_label
st.session_state.submitted
st.session_state.answer_choice
```

### 6.1 初期状態

```text
game_question = まだ存在しない
selected_label = None
submitted = False
answer_choice = None
```

### 6.2 問題生成後

```text
game_question = 生成済みのGameQuestion
selected_label = None
submitted = False
answer_choice = None
```

### 6.3 回答確定後

例：Chart Bを選択した場合

```text
game_question = 同じGameQuestion
selected_label = "Chart B"
submitted = True
answer_choice = "Chart B"
```

要件：

- `answer_choice` は回答確定前の選択中ラベルを保持する
- `selected_label` は回答確定後のラベルだけを保持する
- `answer_choice` の変更だけでは `submitted` を変更しない
- `selected_label` は回答確定済みの選択ラベルを保持する
- `submitted` は回答確定済みかどうかを保持する
- `game_question` がSession Stateに存在しない場合だけ問題を生成する
- 通常のStreamlit再実行では問題を再生成しない
- 回答確定後も `game_question` を変更しない
- 回答確定後も `selected_label` と `submitted` を維持する
- Session Stateのキー名は上記4つを使用する

---

## 7. 問題生成とエラー処理

初回のみ、以下の順序で問題を生成する。

1. 日経225から3銘柄を選択する
2. 各銘柄の株価を `period="5y"` で取得する
3. `generate_game_question()` を呼び出す
4. 生成した `GameQuestion` を `st.session_state.game_question` に保存する

問題生成に失敗した場合は、Session Stateへ不完全な問題を保存しない。

通常画面には次のメッセージだけを表示する。

```text
問題データを生成できませんでした。時間をおいて再度お試しください。
```

例外詳細、会社名、証券コード、ティッカーは通常画面へ表示しない。

Task006では、生成失敗時に自動再試行・銘柄差し替え・再生成ボタンは実装しない。

---

## 8. 画面仕様

画面はTask005までの縦並び表示を維持する。

```text
Stock Trainer

Chart A
［ローソク足＋出来高］
［Chart Aを選ぶ］

Chart B
［ローソク足＋出来高］
［Chart Bを選ぶ］

Chart C
［ローソク足＋出来高］
［Chart Cを選ぶ］

［回答する］
```

要件：

- Chart A/B/Cの順で表示する
- 各チャートの直下に、そのチャートを選択するボタンを1つ配置する
- 3つのうち同時に選択できるのは1つだけとする
- 選択ボタン押下時は対応するChartラベルを `st.session_state.answer_choice` に保存する
- 別のChartの選択ボタンを押すと `answer_choice` をそのChartラベルへ置き換える
- 選択肢の値は `Chart A / Chart B / Chart C` とする
- 会社名・証券コード・将来情報は表示しない
- 選択中のChartが利用者に分かるようにする
- 細かな色、余白、装飾はTask006の対象外とする

選択UIにはStreamlit標準の `st.button()` を使用する。

各チャートの直下に、次の3つのボタンをそれぞれ配置する。

```text
Chart Aを選ぶ
Chart Bを選ぶ
Chart Cを選ぶ
```

要件：

- 各ボタンには一意のkeyを設定する
- ボタン押下時は対応するラベルを `answer_choice` に保存する
- 回答前は別のボタンを押して選択を変更できる
- 現在選択中のChartは `選択中：Chart B` のような表示で分かるようにする
- 回答後は3つの選択ボタンをすべて `disabled=True` とする
- Task006ではチャート全体をクリックして選択するカスタムUIまでは実装しない

---

## 9. 回答処理

### 9.1 未回答時

利用者は各チャート直下の選択ボタンからChart A/B/Cの1つを選択できる。

「回答する」ボタン押下時に選択がない場合は、次の警告を表示する。

```text
1つ選択してください。
```

この場合、`submitted` は `False` のままとする。

### 9.2 回答確定時

選択済みで「回答する」ボタンを押した場合：

- `st.session_state.answer_choice` の値を `st.session_state.selected_label` に保存する
- `st.session_state.submitted = True` とする
- `game_question` は変更しない

回答確定後は、次の情報だけを表示してよい。

```text
回答：Chart B
```

ただし、次は表示しない。

- 正解
- 不正解
- 正解ラベル
- 各Chartの騰落率
- 将来終値
- 将来チャート

---

## 10. 回答後の挙動

`submitted = True` の場合、以下を満たすこと。

- 3つの選択ボタンを `disabled=True` とし、選択内容を変更できない
- 回答ボタンを無効化または非表示にする
- 同じ問題に再回答できない
- 同じ問題とチャートが表示され続ける
- 選択したラベルが表示され続ける
- Streamlitが再実行されても回答状態が維持される
- `correct_label` と比較しない
- 正解・不正解を表示しない

Task006では、回答後に問題をリセットする手段は作らない。

---

## 11. app.pyの処理順

`app.py` は概ね次の順序で処理する。

1. Session Stateの必要なキーを初期化する
2. `game_question` が存在しない場合だけ問題を生成する
3. Session Stateに保持された問題から3つのFigureを生成する
4. 3つのFigureをすべて生成する
5. Chart A/B/Cを縦方向に表示し、各チャート直下に対応する選択ボタンを表示する
6. 未回答なら「回答する」ボタンを表示する
7. 回答ボタン押下時に未選択を検証する
8. `answer_choice` が選択済みなら、その値を `selected_label` へ保存し、`submitted=True` とする
9. 回答済みなら選択UIと回答ボタンを変更不可にする
10. 回答済みラベルだけを表示する

Figure生成に失敗した場合も部分表示せず、問題生成時と同じ利用者向けエラーメッセージを表示する。

---

## 12. 既存APIとの整合性

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

Task006では `app.py` 以外を変更しない。

`app.py` からyfinanceを直接呼び出さない。

---

## 13. 実装手順

1. Session State用キーを初期化する
2. 初回だけ問題を生成して保存する
3. 保存済み問題からFigureを生成する
4. Chart A/B/Cを表示し、各チャート直下に対応する選択ボタンを表示する
5. 単一選択を実現する
6. 回答ボタンを追加する
7. 未選択時の警告を実装する
8. 回答内容と回答済み状態を保存する
9. 回答後の選択変更を防止する
10. 回答後の二重回答を防止する
11. Streamlit再実行時に問題と回答が保持されることを確認する
12. 正解や将来情報が表示されていないことを確認する
13. 構文チェックとStreamlit起動確認を行う

---

## 14. 受け入れ条件

以下をすべて満たした場合、Task006を完了とする。

- [ ] `st.session_state.game_question` が使用されている
- [ ] `st.session_state.selected_label` が使用されている
- [ ] `st.session_state.submitted` が使用されている
- [ ] 初回だけ問題が生成される
- [ ] 通常のStreamlit再実行で問題が変わらない
- [ ] Chart A/B/Cが縦方向に表示される
- [ ] 各チャート直下に対応する選択ボタンが表示される
- [ ] 選択ボタンによりChart A/B/Cから1つだけ選択状態を保持できる
- [ ] 選択中のChartが利用者に分かる
- [ ] 回答前は別の選択ボタンで選択を変更できる
- [ ] 未選択で回答すると「1つ選択してください。」と表示される
- [ ] 未選択時は `submitted` が `False` のままである
- [ ] 選択済みで回答すると選択ラベルが保存される
- [ ] 回答後は `submitted` が `True` となる
- [ ] 回答後は選択を変更できない
- [ ] 回答後は二重回答できない
- [ ] 回答後も同じ問題が表示される
- [ ] 回答済みラベルが表示される
- [ ] 正解・不正解が表示されない
- [ ] 正解ラベル・将来騰落率・将来チャートが表示されない
- [ ] 会社名・証券コード・ティッカーが表示されない
- [ ] 生成またはFigure作成失敗時に部分表示されない
- [ ] `app.py` 以外のファイルを変更していない
- [ ] 既存公開APIが維持されている
- [ ] `app.py` からyfinanceを直接呼び出していない
- [ ] 構文チェックが成功する
- [ ] Streamlitが正常に起動する

---

## 15. 動作確認

1. 初回起動時に問題が1回だけ生成されること
2. 選択操作による再実行後も同じ問題が表示されること
3. 各チャート直下に対応する選択ボタンが表示されること
4. 選択状態として保持される `answer_choice` が常に1つだけであること
5. 回答前は別の選択ボタンを押して選択を変更できること
6. 未選択で回答した場合に警告が表示されること
7. 未選択時に `submitted=False` が維持されること
8. 選択後に回答すると `selected_label` が保存されること
9. 回答後に `submitted=True` となること
10. 回答後に選択を変更できないこと
11. 回答後に回答ボタンを再実行できないこと
12. 回答後の再実行でも問題と回答が変わらないこと
13. 回答済みラベルだけが表示されること
14. 正解・不正解が表示されないこと
15. 将来騰落率・将来終値・将来チャートが表示されないこと
16. 会社名・証券コード・ティッカーが表示されないこと
17. 問題生成失敗時に不完全な問題がSession Stateへ保存されないこと
18. Figure生成失敗時にチャートが部分表示されないこと
19. `app.py` 以外に差分がないこと
20. 既存公開APIが維持されていること
21. `app.py`にyfinanceの直接importがないこと
22. `git diff --check` が成功すること
23. Streamlitが正常起動すること

---

## 16. 残課題

Task007では、`st.session_state.selected_label` と `st.session_state.game_question.correct_label` を比較し、正解・不正解、各Chartの将来騰落率、将来結果を表示する予定とする。

Task008では、「次の問題」操作を追加し、Session Stateをリセットして新しい問題を生成できるようにする予定とする。
