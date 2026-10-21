export type Notebook = {
  id: string;
  name: string;
  description: string;
  documents: number;
  flashcards: number;
  quizzes: number;
  updatedAt: string;
  color: string;
};

export type Activity = {
  id: string;
  title: string;
  detail: string;
  time: string;
  icon: "upload" | "quiz" | "cards" | "chat";
};
