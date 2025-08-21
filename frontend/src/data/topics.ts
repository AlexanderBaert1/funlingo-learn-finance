
export const topics = [
  {
    id: "basics",
    title: "Finance Basics",
    description: "Learn core financial concepts & terminology",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>',
    color: "#2CB674",
    progress: 20,
    locked: false
  },
  {
    id: "budgeting",
    title: "Budgeting",
    description: "Create and stick to effective budgets",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"></rect><path d="M2 10h20"></path></svg>',
    color: "#4ECDC4",
    progress: 0,
    locked: false
  },
  {
    id: "saving",
    title: "Saving",
    description: "Build savings habits & emergency funds",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5c-1.5 0-2.8 1.4-3 2-3.5-1.5-11-.3-11 5 0 1.8 0 3 2 4.5V20h4v-2h3v2h4v-4c1-.5 1.7-1 2-2h2v-4h-2c0-1-.5-1.5-1-2 0-1.2.5-3-1-4Z"></path><path d="M2 9v1c0 1.1.9 2 2 2h1"></path><path d="M16 11h0"></path></svg>',
    color: "#9B87F5", 
    progress: 0,
    locked: true
  },
  {
    id: "investing",
    title: "Investing",
    description: "Learn investment strategies & options",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 16 4-4 4 4 4-4 4 4 4-4"></path><path d="M2 12l4-4 4 4 4-4 4 4 4-4"></path><path d="M2 8l4-4 4 4 4-4 4 4 4-4"></path></svg>',
    color: "#F97316",
    progress: 0,
    locked: true
  },
  {
    id: "credit",
    title: "Credit & Debt",
    description: "Manage credit cards & avoid debt traps",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"></rect><line x1="2" x2="22" y1="10" y2="10"></line></svg>',
    color: "#6E59A5",
    progress: 0,
    locked: true
  },
  {
    id: "taxes",
    title: "Taxes",
    description: "Learn how taxes work & maximize returns",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.29 7 12 12 20.71 7"></polyline><line x1="12" x2="12" y1="22" y2="12"></line></svg>',
    color: "#D946EF",
    progress: 0,
    locked: true
  }
];

export const lessons = {
  "basics": [
    {
      id: "basics-1",
      topicId: "basics",
      title: "Financial Terms 101",
      description: "Learn essential financial vocabulary to build your foundation.",
      duration: 5,
      xp: 10,
      completed: true
    },
    {
      id: "basics-2",
      topicId: "basics",
      title: "Income vs. Expenses",
      description: "Understand the basics of money coming in and going out.",
      duration: 7,
      xp: 15,
      completed: false
    },
    {
      id: "basics-3",
      topicId: "basics",
      title: "Financial Goals",
      description: "Learn how to set and prioritize your financial objectives.",
      duration: 6,
      xp: 15,
      completed: false,
      locked: true
    }
  ],
  "budgeting": [
    {
      id: "budget-1",
      topicId: "budgeting",
      title: "Creating Your First Budget",
      description: "Learn how to create a simple but effective budget.",
      duration: 8,
      xp: 20,
      completed: false
    },
    {
      id: "budget-2",
      topicId: "budgeting",
      title: "Tracking Expenses",
      description: "Techniques to track and categorize your spending.",
      duration: 6,
      xp: 15,
      completed: false,
      locked: true
    },
    {
      id: "budget-3",
      topicId: "budgeting",
      title: "Budget Adjustments",
      description: "Learn when and how to adjust your budget over time.",
      duration: 7,
      xp: 15,
      completed: false,
      locked: true
    }
  ]
};
