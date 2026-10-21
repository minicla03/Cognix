import Link from "next/link";
import {
  ArrowLeft,
  FileText,
  Layers3,
  MessageCircle,
  Sparkles,
} from "lucide-react";

const content = {
  chat: {
    title: "Ask Cognix",
    description: "Start a conversation with your documents.",
    icon: MessageCircle,
    action: "Ask your first question",
  },
  documents: {
    title: "Documents",
    description: "Upload and manage the sources for this notebook.",
    icon: FileText,
    action: "Upload document",
  },
  flashcards: {
    title: "Flashcards",
    description: "Review concepts at your own pace.",
    icon: Layers3,
    action: "Generate flashcards",
  },
  quiz: {
    title: "Quiz",
    description: "Test your understanding with a focused quiz.",
    icon: Sparkles,
    action: "Start a quiz",
  },
};

export default async function SectionPage({
  params,
}: {
  params: Promise<{ id: string; section: string }>;
}) {
  const { id, section } = await params;
  const item = content[section as keyof typeof content] ?? content.chat;
  const Icon = item.icon;
  return (
    <div className="mx-auto max-w-[1000px] px-5 py-10 sm:px-8">
      <Link
        href={`/notebooks/${id}`}
        className="mb-10 inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"
      >
        <ArrowLeft className="size-4" />
        Back to notebook
      </Link>
      <div className="flex min-h-[55vh] flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white px-6 text-center">
        <span className="flex size-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
          <Icon className="size-7" />
        </span>
        <h1 className="mt-6 text-2xl font-semibold">{item.title}</h1>
        <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
          {item.description}
        </p>
        <button className="mt-7 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700">
          {item.action}
        </button>
        <p className="mt-4 text-xs text-slate-400">
          This workspace is ready to connect to your Python backend.
        </p>
      </div>
    </div>
  );
}
