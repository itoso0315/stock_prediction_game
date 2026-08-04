import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/main.dart';
import 'package:stock_trainer_flutter/widgets/answer_button.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';

void main() {
  testWidgets('Task024で回答履歴を記録して結果画面に回答数を表示できる', (tester) async {
    await tester.pumpWidget(const StockTrainerApp());

    expect(find.text('ゲーム開始'), findsOneWidget);

    await tester.tap(find.text('ゲーム開始'));
    await tester.pumpAndSettle();

    expect(find.text('Question 1 / 10'), findsOneWidget);
    expect(find.byType(ChartCard), findsNWidgets(3));
    expect(find.byType(AnswerButton), findsNWidgets(4));
    expect(find.text('Chart A'), findsNWidgets(2));
    expect(find.text('Chart B'), findsNWidgets(2));
    expect(find.text('Chart C'), findsNWidgets(2));
    expect(find.text('現金保有'), findsOneWidget);
    expect(find.byType(SingleChildScrollView), findsOneWidget);
    expect(
      tester
          .widgetList<FilledButton>(find.byType(FilledButton))
          .every((button) => button.onPressed != null),
      isTrue,
    );

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    expect(find.text('Question 2 / 10'), findsOneWidget);

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    expect(find.text('Question 3 / 10'), findsOneWidget);

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsOneWidget);
    expect(find.text('ゲーム終了です'), findsOneWidget);
    expect(find.text('回答数: 3件'), findsOneWidget);
    expect(find.text('ホームへ戻る'), findsOneWidget);
    expect(find.text('ゲーム開始'), findsNothing);

    await tester.tap(find.text('ホームへ戻る'));
    await tester.pumpAndSettle();

    expect(find.text('ゲーム開始'), findsOneWidget);
    expect(find.byType(ChartCard), findsNothing);
  });
}
