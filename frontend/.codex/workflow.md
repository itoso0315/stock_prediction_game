

# Development Workflow

## 基本フロー

このプロジェクトはTask駆動開発を採用する。

```text
1. ChatGPTがTask仕様書を作成・レビュー
        ↓
2. CodexがTaskどおりに実装
        ↓
3. dart format .
        ↓
4. flutter analyze
        ↓
5. flutter test
        ↓
6. ChatGPTが実装レビュー
        ↓
7. Git Commit
        ↓
8. Git Push
```

## 実装ルール

- Taskを唯一の仕様書とする
- Taskに書かれていない機能は実装しない
- 小さなTask単位で進める
- 変更対象外のファイルは編集しない

## 品質ゲート

すべて満たしたらTask完了とする。

- dart format が成功
- flutter analyze が成功
- flutter test が成功
- Taskの受け入れ条件を満たす
- ChatGPTレビュー完了

## Git運用

Taskが完了したら

- Git Commit
- Git Push

を実施する。

コミット前には必ず動作確認を行う。