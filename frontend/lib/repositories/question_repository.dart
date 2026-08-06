import '../models/question.dart';
import '../models/answer.dart';

class QuestionRepository {
  const QuestionRepository();

  List<Question> getQuestions() {
    return const [
      Question(
        currentNumber: 1,
        totalQuestions: 3,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answers: [
          Answer(
            label: 'Chart A',
            type: AnswerType.stock,
            ticker: '3099',
            companyName: '三越伊勢丹ホールディングス',
            baseClose: 2733.5,
            evaluationClose: 2631.5,
            returnRate: -3.73,
          ),
          Answer(
            label: 'Chart B',
            type: AnswerType.stock,
            ticker: '6723',
            companyName: 'ルネサスエレクトロニクス',
            baseClose: 1662.5,
            evaluationClose: 1871.0,
            returnRate: 12.54,
          ),
          Answer(
            label: 'Chart C',
            type: AnswerType.stock,
            ticker: '7186',
            companyName: '横浜フィナンシャルグループ',
            baseClose: 1118.0,
            evaluationClose: 1109.5,
            returnRate: -0.76,
          ),
          Answer(label: '現金保有', type: AnswerType.cash, returnRate: 0),
        ],
        correctAnswerLabel: 'Chart A',
      ),
      Question(
        currentNumber: 2,
        totalQuestions: 3,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answers: [
          Answer(
            label: 'Chart A',
            type: AnswerType.stock,
            ticker: '9432',
            companyName: '日本電信電話',
            baseClose: 153.2,
            evaluationClose: 149.1,
            returnRate: -2.68,
          ),
          Answer(
            label: 'Chart B',
            type: AnswerType.stock,
            ticker: '8306',
            companyName: '三菱UFJフィナンシャル・グループ',
            baseClose: 1620.0,
            evaluationClose: 1735.5,
            returnRate: 7.13,
          ),
          Answer(
            label: 'Chart C',
            type: AnswerType.stock,
            ticker: '2914',
            companyName: '日本たばこ産業',
            baseClose: 3950.0,
            evaluationClose: 4015.0,
            returnRate: 1.65,
          ),
          Answer(label: '現金保有', type: AnswerType.cash, returnRate: 0),
        ],
        correctAnswerLabel: 'Chart B',
      ),
      Question(
        currentNumber: 3,
        totalQuestions: 3,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answers: [
          Answer(
            label: 'Chart A',
            type: AnswerType.stock,
            ticker: '6758',
            companyName: 'ソニーグループ',
            baseClose: 13200.0,
            evaluationClose: 13080.0,
            returnRate: -0.91,
          ),
          Answer(
            label: 'Chart B',
            type: AnswerType.stock,
            ticker: '7974',
            companyName: '任天堂',
            baseClose: 8120.0,
            evaluationClose: 8260.0,
            returnRate: 1.72,
          ),
          Answer(
            label: 'Chart C',
            type: AnswerType.stock,
            ticker: '8035',
            companyName: '東京エレクトロン',
            baseClose: 24300.0,
            evaluationClose: 26320.0,
            returnRate: 8.31,
          ),
          Answer(label: '現金保有', type: AnswerType.cash, returnRate: 0),
        ],
        correctAnswerLabel: 'Chart C',
      ),
    ];
  }

  Question getQuestion(int index) {
    return getQuestions()[index];
  }
}
