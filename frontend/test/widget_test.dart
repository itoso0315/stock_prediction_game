import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/main.dart';
import 'package:stock_trainer_flutter/widgets/answer_button.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';

void main() {
  testWidgets('Task022で回答後に次の問題へ進める', (tester) async {
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

    expect(find.text('Question 3 / 10'), findsOneWidget);
    expect(find.text('ゲーム開始'), findsNothing);

    await tester.pageBack();
    await tester.pumpAndSettle();

    expect(find.text('ゲーム開始'), findsOneWidget);
    expect(find.byType(ChartCard), findsNothing);
  });
}
