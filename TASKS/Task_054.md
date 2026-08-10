

# Task 054: Backendをクラウド公開し、iPhone単体でStock Trainerを動作させる

## 目的

Macを起動していなくても、iPhoneのStock Trainerから問題データを取得してゲームを遊べる状態にする。

現在はFlutterアプリがMac上のFastAPIへLAN経由で接続している。

```text
http://192.168.11.8:8000
```

Task 054ではFastAPI Backendをインターネット上へ公開し、Flutterアプリの接続先を公開Backendへ切り替える。

---

## 現在地

- FlutterのiPhone実機起動に成功済み
- iPhone Developer Mode設定済み
- Xcode署名・実機インストール成功済み
- FastAPIはMac上で起動可能
- iPhone SafariからMacのFastAPIへLAN接続成功済み
- Flutter実機から以下を指定して問題データ取得成功済み

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.11.8:8000
```

- Flutter側は `API_BASE_URL` でAPI接続先を切り替えられる状態
- RenderへFastAPI Backendを公開済み
- 公開URL：`https://stock-prediction-game-api.onrender.com`
- iPhone Safariから公開Backendの `/api/health` が正常応答することを確認済み
- 公開環境の `/api/questions` が実データを返すことを確認済み
- RenderでYahoo Financeの取得件数が不足した場合の追加取得フォールバックを実装済み
- Flutter実機からRender Backendへ接続し、問題画面を表示できることを確認済み

### 実機確認で判明した戦績保存不具合

10問を最後まで回答してホーム画面へ戻っても、以下の戦績が初期値のまま更新されない。

- 挑戦回数
- 平均正答率

Task 054では、10問目回答完了から最終リザルト生成、ゲーム結果保存、永続化、
ホーム画面復帰、保存済み戦績の再読込、表示更新までの経路を確認し、原因を特定した
うえで必要最小限の修正と再発防止テストを行う。

---

## ゴール

以下をすべて満たしたらTask 054完了とする。

1. FastAPI Backendがクラウド上で常時アクセス可能
2. HTTPSの公開URLが発行されている
3. 公開URLの `/docs` または `/api/health` にiPhone Safariからアクセスできる
4. Flutterアプリが公開Backendから問題データを取得できる
5. Mac上のFastAPIを停止してもiPhoneで問題画面を表示できる
6. MacとiPhoneが同じWi-Fiに接続されていなくてもゲームを開始できる
7. 既存のMacローカル開発環境を壊さない
8. 10問プレイ完了時にゲーム結果が端末へ永続化される
9. ホーム画面へ戻った際に、挑戦回数・平均正答率が再読込される

---

## 実装方針

### 1. Backendのクラウドデプロイ

`backend/` のFastAPIをクラウドサービスへデプロイする。

デプロイ先は、Task実装開始時点の料金・無料枠・FastAPI対応状況を確認したうえで、以下を優先して1サービスに決定する。

- 設定が簡単
- GitHub連携が可能
- Python / FastAPIをそのまま実行可能
- HTTPS URLが自動発行される
- 個人開発のMVPとして低コスト

候補例：

- Render
- Railway
- Fly.io

サービス選定自体を目的にせず、最短で安定して公開できるものを採用する。

---

### 2. Backend起動コマンド

クラウド環境ではFastAPIを外部公開可能な設定で起動する。

例：

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

クラウドサービス側が指定する `PORT` 環境変数へ対応すること。

ローカル開発時の既存起動方法は維持する。

---

### 3. Python依存関係

クラウド環境でBackendが再現できるよう、必要なPython依存パッケージを明示する。

最低限、現在Backendで使用している以下を確認する。

- fastapi
- uvicorn
- yfinance
- pandas
- その他Backendがimportしているパッケージ

不足がある場合のみ依存関係ファイルを修正する。

---

### 4. Flutter API URL切り替え

既存の `API_BASE_URL` の仕組みを維持する。

ローカル開発では従来どおりMac Backendを指定可能にする。

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.11.8:8000
```

クラウド動作確認時は公開URLを指定する。

```bash
flutter run --dart-define=API_BASE_URL=https://<公開Backend URL>
```

API URLをWidgetやRepository内へ直接ハードコードしない。

---

### 5. HTTPSを使用する

iPhone単体利用では公開Backendへの通信はHTTPSを使用する。

本番・公開環境でHTTP通信を前提にしない。

既存のLAN内HTTP通信設定はローカル実機開発用として残してよい。

---

## 動作確認

### Backend

公開後、以下を確認する。

```text
https://<公開Backend URL>/docs
```

または

```text
https://<公開Backend URL>/api/health
```

期待結果：HTTP 200。

問題取得APIも確認する。

```text
GET /api/questions
```

期待結果：既存仕様どおり問題データが返る。

---

### Flutter / iPhone

公開Backend URLを指定して実機起動する。

```bash
flutter run --dart-define=API_BASE_URL=https://<公開Backend URL>
```

確認項目：

- トップ画面が表示される
- 「ゲーム開始」を押せる
- 問題データ取得エラーが出ない
- Chart A/B/Cが既存仕様どおり表示される

---

### Mac非依存テスト

最終確認ではMac上のFastAPIを停止する。

その状態でiPhoneからStock Trainerを操作し、問題画面まで遷移できることを確認する。

可能であればiPhoneをWi-Fiから切り離し、モバイル通信でも同様に問題取得できることを確認する。

---

## テスト

既存テストを壊さない。

Backend：

```bash
pytest
```

Flutter：

```bash
flutter analyze
flutter test
```

Task完了時点で既存テストがすべて成功すること。

---

## 対象外

Task 054では以下を実装しない。

- App Store申請
- TestFlight配信
- 独自ドメイン取得
- ユーザー認証
- データベースの大規模変更
- 課金機能
- Push通知
- X / Instagram / LINE共有機能
- UIデザイン変更
- Chart B/Cなど別Taskの機能追加

---

## 実装時の注意

- 既存のローカル開発環境を壊さない
- `192.168.11.8` を本番URLとしてハードコードしない
- API URLは既存の `API_BASE_URL` 経由で管理する
- APIキー、パスワード、秘密情報をGitへcommitしない
- 必要以上のリファクタリングを行わない
- Task 054に関係しないファイルを変更しない
- デプロイサービス固有の設定ファイルを追加する場合は必要最小限とする

---

## 完了条件

- [x] FastAPI Backendの公開URLが発行されている
- [x] 公開URLがHTTPSでアクセス可能
- [x] `/api/health` または同等のヘルスチェックが成功
- [x] `/api/questions` が公開環境で正常応答
- [x] Flutterから公開Backendへ接続成功
- [x] iPhone実機で問題画面まで表示成功
- [ ] Mac上のFastAPI停止中でも動作成功
- [ ] LAN外からも問題取得成功
- [x] 10問プレイ完了時に戦績が端末へ永続化される（コード・自動テスト）
- [x] ホーム画面復帰時に保存済み戦績が再読込される（コード・自動テスト）
- [x] 挑戦回数・平均正答率が正しく表示される（コード・自動テスト）
- [x] 戦績保存からホーム画面更新までの再発防止テストが成功
- [ ] iPhone実機で10問完了後に挑戦回数・平均正答率が更新される
- [x] Backend tests成功
- [x] `flutter analyze` 成功
- [x] `flutter test` 成功

## Task 054 完了状態

**Macを開いていなくても、iPhoneだけでStock Trainerを起動し、クラウドBackendから問題データを取得してゲームを遊べる。**
