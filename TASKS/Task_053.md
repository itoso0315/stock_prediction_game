

# Task 053: Stock Trainerを自分のiPhoneで実機アプリとして遊べる状態にする

## 目的
現在macOSで動作しているFlutter版Stock Trainerを、自分のiPhoneへ実際にインストールして起動し、iPhone上で10問ゲームを最後まで遊べる状態にする。

Taskを細かく分割しすぎず、このTaskでは「iOSビルド準備」だけで終わらせない。
Xcode設定、署名、iPhone実機接続、Flutter実機ビルド、Mac上のFastAPIへの接続、実際のゲーム動作確認まで一気に進める。

App Store公開はこのTaskの対象外。
まずは自分のiPhoneのホーム画面からStock Trainerを起動して遊べることを最優先とする。

## iPhone対応ロードマップ
iPhoneで日常的に遊べる状態まで、Task053〜055の最大3Task程度で完了させる方針とする。

### Task053（このTask）
自分のiPhoneへFlutterアプリをインストールし、同一Wi-Fi上のMacで起動しているFastAPIへ接続してゲームを完走する。

### Task054（予定）
FastAPI Backendをインターネット上へ公開し、Macを起動していなくてもiPhone単独でStock Trainerを遊べる状態にする。

### Task055（必要な場合のみ）
iPhoneアプリとしての仕上げを行う。
例：アプリアイコン、表示名、共有機能のiOS実機調整、起動時設定、本番API設定、安定化など。

Task054までで十分実用的な状態になった場合、Task055を無理に作らなくてよい。

## 現在地
- Flutter版Stock TrainerはmacOS実機で動作している。
- FlutterからFastAPIへHTTP通信できる。
- BackendはMac上でFastAPI / uvicornとして起動している。
- 現在の開発時APIはlocalhost / 127.0.0.1を前提とした箇所がある可能性がある。
- Question / Result / 10問連続プレイ等のゲーム本体はTask052までで実装する。
- FlutterプロジェクトにはiOSディレクトリが存在する前提で、まず現在のiOS設定を確認する。
- ユーザーはMacと自分のiPhoneを利用して実機確認する。

## 完成イメージ

```text
自分のiPhone
┌─────────────────────┐
│ Stock Trainer       │
│                     │
│ Question 1 / 10     │
│ Chart A             │
│ Chart B             │
│ Chart C             │
│ 現金保有             │
└─────────────────────┘
          ↓ Wi-Fi

Mac
FastAPI / yfinance
```

iPhoneのホーム画面にStock Trainerが存在し、通常のアプリと同様にタップして起動できる状態を目指す。

## 実装内容

### 1. 現在のFlutter iOS構成を確認する
まず以下を調査する。

- `frontend/ios/` が正常に存在するか
- Bundle Identifier
- iOS Deployment Target
- Xcode project / workspace
- CocoaPods状態
- FlutterのiOS関連設定
- API URLを定義している場所
- HTTP通信に必要なiOS権限設定

既存コードでそのまま利用できる部分は変更しない。

### 2. Flutter / XcodeのiOSビルド環境を整える
自分のMacでiOS実機ビルドできる状態にする。

必要に応じて以下を対応する。

- `flutter doctor` でiOS開発環境を確認
- Xcode command line toolsの確認
- CocoaPods依存関係の解決
- `flutter pub get`
- iOS project設定の修正

既に正常なら不要な再設定をしない。

### 3. 自分のiPhoneを開発端末として認識させる
MacへiPhoneを接続し、Flutter / Xcodeから実機として認識できる状態にする。

確認事項：

- iPhoneで「このコンピュータを信頼」を完了できる
- 必要であればDeveloper Modeを有効化する
- `flutter devices` に自分のiPhoneが表示される
- XcodeのDevices and Simulatorsでも認識される

端末名やUDIDをコードへハードコードしない。

### 4. iOS署名設定を行う
自分のiPhoneへアプリをインストールできるよう、XcodeのSigning & Capabilitiesを設定する。

要件：

- 自分のApple ID / Development Teamを使用する
- Bundle Identifierが署名可能な一意の値になっている
- Automatic Signingを基本とする
- App Store公開用の複雑な証明書構成はまだ行わない
- 無料Apple IDで実機インストール可能な範囲を優先する

Apple Developer Programへの有料加入がこの段階で必須でない場合は、加入を前提にしない。

### 5. iPhoneからMacのFastAPIへ接続できるようにする
ここがTask053の重要ポイント。

iPhone上の`127.0.0.1` / `localhost`はiPhone自身を指すため、Macで起動しているFastAPIへは接続できない。

同一Wi-Fi上で、MacのLAN IPアドレスを利用して接続する。

概念：

```text
iPhone Flutter
      ↓
http://<MacのLAN IP>:8000
      ↓
Mac FastAPI
```

要件：

- Backendを必要に応じて`0.0.0.0`でlistenさせ、LAN内のiPhoneからアクセスできるようにする
- Macの現在のLAN IPを確認する
- FlutterのAPI Base URLをiPhone実機向けに切り替えられるようにする
- localhostをコード中へ散在させず、API URLを一か所で管理する
- macOS開発時の既存動作も壊さない
- 将来Task054で本番HTTPS API URLへ簡単に切り替えられる構成にする

必要であれば開発環境用の設定クラス・定数・`--dart-define`等を採用してよい。
過剰な環境管理基盤は不要。

### 6. iOSのHTTP通信設定を確認する
Task053ではLAN内の開発用FastAPIがHTTPになる可能性が高い。

iOSのApp Transport Security等により通信が拒否される場合は、開発実機確認に必要な最小限の設定を行う。

要件：

- 必要以上に広い通信許可を入れない
- 開発用設定であることを明確にする
- Task054のHTTPS Backend公開後に不要になる設定は整理しやすい形にする
- iOS実機でQuestion API / Result API等が通信できることを確認する

### 7. FastAPIをiPhone実機確認用に起動できるようにする
Task053ではユーザーが迷わず起動できることも重要。

実機確認時のBackend起動例：

```bash
cd ~/Python/stock_prediction_game/backend
source ../.venv-1/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

現在の仮想環境名・ディレクトリ構成が異なる場合は、実際のリポジトリを正として適切なコマンドを提示する。

### 8. Flutterを自分のiPhoneへインストールする
Flutterから認識済みのiPhoneを指定して実行する。

例：

```bash
cd ~/Python/stock_prediction_game/frontend
flutter run -d <自分のiPhone>
```

必要であれば最初の署名エラー等をXcode側で修正する。

最終的に、Flutter runから自分のiPhoneへStock Trainerがインストールされ起動すること。

### 9. iPhoneホーム画面からアプリを起動できることを確認する
Flutterデバッグ実行中だけでなく、iPhone上にStock Trainerアプリがインストールされていることを確認する。

最低限：

- iPhoneのホーム画面 / App Libraryにアプリが存在する
- アプリをタップして起動できる
- 開発者信頼設定が必要な場合は適切に設定する

Task053ではアプリアイコンの完成デザインは必須ではない。

### 10. iPhone実機でゲームを10問完走する
単にHome画面が開くだけではTask053完了としない。

iPhone上で実際に以下を確認する。

- Home画面表示
- ゲーム開始
- Question 1 / 10〜10 / 10
- Chart A / B / C表示
- ローソク足
- 出来高
- 移動平均線ON/OFF
- 現金保有
- 回答確定
- 各QuestionのResult
- 10問終了後の最終Result
- 正答数 / 正答率
- 共有UI
- X / Instagram / LINE / URL共有導線がiOSでクラッシュしない

Task052が未完の機能については、その時点で存在する最新版ゲームフロー全体を確認する。

### 11. iPhoneの画面サイズでUI崩れを確認する
macOSウィンドウでは問題なくても、iPhoneでは縦幅・横幅が異なる。

確認事項：

- 横スクロールが不自然に発生しない
- Chartカードが画面幅からはみ出さない
- 120営業日のローソク足が視認できる
- 出来高が潰れすぎない
- MA切替UIを操作できる
- Question / Resultのテキストが見切れない
- 共有ボタンが押せる
- Safe AreaにUIが食い込まない

重大な崩れがある場合はTask053内で必要なレスポンシブ修正を行ってよい。
ただしUI全体のデザイン刷新はしない。

### 12. iPhone実機特有の問題を修正する
以下のようなiOS実機固有エラーが発生した場合は、Task053内で原因調査・修正まで行う。

例：

- Signingエラー
- Provisioning Profileエラー
- Developer Mode
- HTTP通信拒否
- Macへの接続失敗
- Local Network権限
- iOS固有の共有機能エラー
- Safe Area / レイアウト崩れ

レビューだけで止まらず、可能な範囲で実機起動可能な状態まで進める。

## 開発環境と本番環境の考え方
Task053では開発環境として以下を許容する。

```text
iPhone
 ↓ 同一Wi-Fi
Mac FastAPI
```

これは最終形ではない。

Task054で以下へ移行する。

```text
iPhone
 ↓ HTTPS / Internet
公開FastAPI
```

そのためTask053でAPI URL周りを変更する場合、将来の本番URL切替を難しくしない。

## Task053でやらないこと

- App Store申請
- TestFlight一般配布
- Backendの本番クラウド公開
- 独自ドメイン取得
- 本番運用監視
- Push通知
- iPad専用最適化
- Android実機対応
- 大規模なUIデザイン刷新

## テスト・検証
Codexで可能な範囲で以下を実行する。

- `flutter analyze`
- `flutter test`
- `flutter devices`
- iOS build確認
- 必要に応じて`flutter build ios`または実機向けbuild
- Backendテスト
- `git diff --check`

署名や物理iPhone上の操作などCodex単独で完了できない項目は、ユーザーが行う操作を最小限・具体的な手順で提示する。

「Xcodeを開いて適当に設定してください」のような曖昧な案内は避け、どの画面の何を選ぶか明確にする。

## 完了条件

- 自分のiPhoneがFlutter開発端末として認識される。
- Xcode署名が設定され、自分のiPhoneへアプリをインストールできる。
- iPhoneホーム画面 / App LibraryにStock Trainerが存在する。
- iPhoneからMac上のFastAPIへ同一Wi-Fi経由で通信できる。
- iPhone上で実データのChart A / B / Cを表示できる。
- iPhone上でゲームの最新版フローを最初から最後までプレイできる。
- 10問仕様が実装済みなら10問完走できる。
- Result画面まで正常に遷移できる。
- 最終Resultの共有UIが実装済みならiOS上でも操作できる。
- iPhone画面で致命的なレイアウト崩れがない。
- macOS版の既存動作を不必要に壊していない。
- `flutter analyze`が成功する。
- `flutter test`が成功する。
- Backendテストが成功する。
- `git diff --check`が成功する。

## 制約

- Taskを細かく分割しすぎない。
- iPhone実機インストールまでをTask053のスコープに含める。
- ユーザー確認が本当に必要なApple ID・署名・物理端末操作以外は、軽微な判断で停止しない。
- 致命的な仕様矛盾がなければ、調査 → 実装 → テストまで一気に進める。
- 不要な大規模リファクタリングはしない。
- Git commit / Git pushは行わない。