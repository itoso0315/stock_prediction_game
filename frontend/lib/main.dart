import 'package:flutter/material.dart';
import 'repositories/question_api_repository.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const StockTrainerApp());
}

class StockTrainerApp extends StatelessWidget {
  const StockTrainerApp({
    super.key,
    this.questionRepository,
  });

  final QuestionApiRepository? questionRepository;

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
        useMaterial3: true,
      ),
      home: HomeScreen(
        questionRepository: questionRepository,
      ),
    );
  }
}
