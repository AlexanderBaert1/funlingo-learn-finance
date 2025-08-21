
import { Question } from "@/components/question-card";

export const questionData: Record<string, Question[]> = {
  "basics-1": [
    {
      id: "basics-1-1",
      type: "multiple-choice",
      question: "What is a budget?",
      options: [
        "A plan for spending and saving money",
        "A type of bank account",
        "A credit card limit",
        "A loan payment"
      ],
      correctAnswer: "A plan for spending and saving money",
      explanation: "A budget is a financial plan that helps you track income and expenses to manage your money effectively."
    },
    {
      id: "basics-1-2",
      type: "fill-blank",
      question: "Money coming into your account is called _____.",
      correctAnswer: "income",
      explanation: "Income is money you receive from work, investments, or other sources."
    },
    {
      id: "basics-1-3",
      type: "true-false",
      question: "Assets are things you own that have value.",
      correctAnswer: "True",
      explanation: "Assets include things like cash, property, investments, and other valuable items you own."
    },
    {
      id: "basics-1-4",
      type: "multiple-choice",
      question: "Which of these is considered a liability?",
      options: [
        "Your savings account",
        "Your car loan",
        "Your house",
        "Your investment portfolio"
      ],
      correctAnswer: "Your car loan",
      explanation: "A liability is money you owe to others. Car loans, credit card debt, and mortgages are common liabilities."
    },
    {
      id: "basics-1-5",
      type: "fill-blank",
      question: "Your _____ worth is calculated by subtracting your liabilities from your assets.",
      correctAnswer: "net",
      explanation: "Net worth = Assets - Liabilities. It's a key measure of your overall financial health."
    }
  ],

  "basics-2": [
    {
      id: "basics-2-1",
      type: "multiple-choice",
      question: "What's the difference between income and expenses?",
      options: [
        "Income is money coming in, expenses are money going out",
        "They are the same thing",
        "Income is yearly, expenses are monthly",
        "Income is from jobs, expenses are from investments"
      ],
      correctAnswer: "Income is money coming in, expenses are money going out",
      explanation: "Income is money you receive (salary, tips, etc.) while expenses are money you spend (rent, food, etc.)."
    },
    {
      id: "basics-2-2",
      type: "true-false",
      question: "Fixed expenses stay the same each month.",
      correctAnswer: "True",
      explanation: "Fixed expenses like rent, insurance, and loan payments typically remain constant each month."
    },
    {
      id: "basics-2-3",
      type: "fill-blank",
      question: "Expenses that change from month to month are called _____ expenses.",
      correctAnswer: "variable",
      explanation: "Variable expenses include things like groceries, entertainment, and utilities that can fluctuate."
    },
    {
      id: "basics-2-4",
      type: "multiple-choice",
      question: "Which is an example of a fixed expense?",
      options: [
        "Groceries",
        "Entertainment",
        "Rent",
        "Gas for your car"
      ],
      correctAnswer: "Rent",
      explanation: "Rent is typically the same amount each month, making it a fixed expense."
    }
  ],

  "budget-1": [
    {
      id: "budget-1-1",
      type: "multiple-choice",
      question: "What's the first step in creating a budget?",
      options: [
        "Cut all expenses",
        "Track your income and expenses",
        "Open a savings account",
        "Pay off debt"
      ],
      correctAnswer: "Track your income and expenses",
      explanation: "Before you can make a plan, you need to know how much money comes in and where it goes."
    },
    {
      id: "budget-1-2",
      type: "fill-blank",
      question: "The 50/30/20 rule suggests spending 50% on _____, 30% on wants, and 20% on savings.",
      correctAnswer: "needs",
      explanation: "The 50/30/20 rule is a simple budgeting framework: 50% needs, 30% wants, 20% savings and debt repayment."
    },
    {
      id: "budget-1-3",
      type: "true-false",
      question: "You should review and adjust your budget regularly.",
      correctAnswer: "True",
      explanation: "Budgets should be living documents that you review and adjust as your income and expenses change."
    },
    {
      id: "budget-1-4",
      type: "multiple-choice",
      question: "What should you do if your expenses exceed your income?",
      options: [
        "Ignore it",
        "Use credit cards",
        "Reduce expenses or increase income",
        "Stop budgeting"
      ],
      correctAnswer: "Reduce expenses or increase income",
      explanation: "When expenses exceed income, you need to either cut spending or find ways to earn more money."
    }
  ]
};
