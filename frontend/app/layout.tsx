import type { Metadata } from "next";
import "./globals.css";
import { CognixShell } from "@/components/cognix-shell";

export const metadata: Metadata = {
  title: "Cognix — Turn your documents into knowledge",
  description:
    "Upload documents, ask questions, explore cited answers, and create flashcards and quizzes with Cognix.",
  openGraph: {
    title: "Cognix — Turn your documents into knowledge",
    description:
      "Upload documents, ask questions, explore cited answers, and create flashcards and quizzes with Cognix.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <CognixShell>{children}</CognixShell>
      </body>
    </html>
  );
}
