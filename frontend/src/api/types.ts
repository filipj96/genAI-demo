export type ChatTurn = {
  question: string;
  answer: string;
  followUpQuestions?: string[]; // Now an array, optional follow up question, probably should be a part of a answer object
};

export type ChatRequest = {
  history: ChatTurn[];
};

export type AskResponse = {
  answer: string;
  thoughts: string | null;
  data_points: string[];
  error?: string;
};
