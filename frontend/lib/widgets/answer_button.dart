import 'package:flutter/material.dart';

class AnswerButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;

  const AnswerButton({super.key, required this.label, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton(onPressed: onPressed, child: Text(label)),
    );
  }
}
