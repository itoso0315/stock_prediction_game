import 'package:flutter/material.dart';
import 'repositories/question_api_repository.dart';
import 'repositories/game_stats_repository.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const StockTrainerApp());
}

class StockTrainerApp extends StatelessWidget {
  const StockTrainerApp({
    super.key,
    this.questionRepository,
    this.gameStatsRepository,
  });

  final QuestionApiRepository? questionRepository;
  final GameStatsRepository? gameStatsRepository;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stock Trainer',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF101214),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFFD4AF37),
          onPrimary: Color(0xFF171717),
          secondary: Color(0xFFBFA76A),
          surface: Color(0xFF1A1D21),
          onSurface: Color(0xFFF4F1E8),
          outline: Color(0xFF3A3D42),
          outlineVariant: Color(0xFF2A2D32),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF101214),
          foregroundColor: Color(0xFFF4F1E8),
          elevation: 0,
          centerTitle: true,
        ),
        cardTheme: CardThemeData(
          color: const Color(0xFF1A1D21),
          elevation: 0,
          margin: EdgeInsets.zero,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
            side: const BorderSide(color: Color(0xFF2A2D32)),
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: const Color(0xFFD4AF37),
            foregroundColor: const Color(0xFF171717),
            disabledBackgroundColor: const Color(0xFF3A3D42),
            disabledForegroundColor: const Color(0xFF8A8D93),
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
          ),
        ),
        textTheme: const TextTheme(
          headlineMedium: TextStyle(
            color: Color(0xFFF4F1E8),
            fontWeight: FontWeight.w700,
          ),
          titleMedium: TextStyle(
            color: Color(0xFFF4F1E8),
            fontWeight: FontWeight.w600,
          ),
          bodyLarge: TextStyle(color: Color(0xFFE7E1D1)),
          bodyMedium: TextStyle(color: Color(0xFFB8B2A4)),
        ),
        pageTransitionsTheme: const PageTransitionsTheme(
          builders: {
            TargetPlatform.android: _ForwardPageTransitionsBuilder(),
            TargetPlatform.iOS: _ForwardPageTransitionsBuilder(),
            TargetPlatform.macOS: _ForwardPageTransitionsBuilder(),
            TargetPlatform.windows: _ForwardPageTransitionsBuilder(),
            TargetPlatform.linux: _ForwardPageTransitionsBuilder(),
            TargetPlatform.fuchsia: _ForwardPageTransitionsBuilder(),
          },
        ),
        useMaterial3: true,
      ),
      home: HomeScreen(
        questionRepository: questionRepository,
        gameStatsRepository: gameStatsRepository,
      ),
    );
  }
}

class _ForwardPageTransitionsBuilder extends PageTransitionsBuilder {
  const _ForwardPageTransitionsBuilder();

  @override
  Widget buildTransitions<T>(
    PageRoute<T> route,
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    return AnimatedBuilder(
      animation: animation,
      child: child,
      builder: (context, child) {
        final progress = Curves.easeInOut.transform(animation.value);
        return FractionalTranslation(
          translation: Offset(1 - progress, 0),
          child: child,
        );
      },
    );
  }
}
