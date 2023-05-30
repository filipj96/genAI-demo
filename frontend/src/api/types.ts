export type ChatTurn = {
  question: string;
  answer: string;
};

export type ChatRequest = {
  history: ChatTurn[];
};

export type AskResponse = {
  answer: string;
  searchWords: string | null; // Maybe a list of strings
  products: string[];
  error?: string;
};
