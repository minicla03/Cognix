"use client";

import Link from "next/link";
import {
  ArrowLeft,
  BookOpen,
  FileText,
  Layers3,
  MessageCircle,
  MoreHorizontal,
  Plus,
  Sparkles,
} from "lucide-react";
import { useParams } from "next/navigation";
import { notebooks } from "@/lib/api/notebooks";

const tabs = [
  { label: "Chat", href: "chat", icon: MessageCircle },
  { label: "Documents", href: "documents", icon: FileText },
  { label: "Flashcards", href: "flashcards", icon: Layers3 },
  { label: "Quiz", href: "quiz", icon: Sparkles },
];

export default function NotebookPage() {
  const { id } = useParams<{ id: string }>();
  const notebook = notebooks.find((item) => item.id === id) ?? notebooks[0];
  return (
    <div className="mx-auto max-w-[1240px] px-5 py-8 sm:px-8 sm:py-10">
      <Link
        href="/dashboard"
        className="mb-8 inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"
      >
        <ArrowLeft className="size-4" />
        Back to dashboard
      </Link>
      <div className="flex flex-col justify-between gap-5 border-b border-slate-200 pb-7 sm:flex-row sm:items-end">
        <div className="flex items-start gap-4">
          <span
            className={`mt-1 flex size-12 items-center justify-center rounded-xl ${notebook.color}`}
          >
            <BookOpen className="size-6" />
          </span>
          <div>
            <div className="mb-1 flex items-center gap-2">
              <span className="text-xs font-medium uppercase tracking-wider text-indigo-600">
                Notebook
              </span>
              <span className="size-1 rounded-full bg-slate-300" />
              <span className="text-xs text-slate-400">
                Updated {notebook.updatedAt}
              </span>
            </div>
            <h1 className="text-3xl font-semibold tracking-tight">
              {notebook.name}
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              {notebook.description}
            </p>
          </div>
        </div>
        <button className="inline-flex w-fit items-center gap-2 rounded-lg border border-slate-200 bg-white px-3.5 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
          <MoreHorizontal className="size-4" />
          Manage
        </button>
      </div>
      <nav className="flex gap-1 overflow-x-auto border-b border-slate-200">
        <Link
          href={`/notebooks/${id}`}
          className="border-b-2 border-indigo-600 px-4 py-3 text-sm font-semibold text-indigo-700"
        >
          Overview
        </Link>
        {tabs.map((tab) => (
          <Link
            key={tab.href}
            href={`/notebooks/${id}/${tab.href}`}
            className="flex items-center gap-2 border-b-2 border-transparent px-4 py-3 text-sm font-medium text-slate-500 hover:border-slate-300 hover:text-slate-900"
          >
            <tab.icon className="size-4" />
            {tab.label}
          </Link>
        ))}
      </nav>
      <div className="grid gap-5 pt-8 md:grid-cols-3">
        <Link
          href={`/notebooks/${id}/chat`}
          className="group rounded-xl border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-md md:col-span-2"
        >
          <div className="flex items-center justify-between">
            <span className="flex size-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
              <MessageCircle className="size-5" />
            </span>
            <span className="text-sm font-medium text-indigo-600 opacity-0 transition group-hover:opacity-100">
              Open chat →
            </span>
          </div>
          <h2 className="mt-5 text-lg font-semibold">Ask Cognix anything</h2>
          <p className="mt-1 max-w-md text-sm leading-6 text-slate-500">
            Ask questions across your documents and get answers with page-level
            citations.
          </p>
          <div className="mt-6 rounded-lg bg-slate-50 px-4 py-3 text-sm text-slate-400">
            What would you like to learn today?
          </div>
        </Link>
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <span className="flex size-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
            <FileText className="size-5" />
          </span>
          <p className="mt-5 text-3xl font-semibold">{notebook.documents}</p>
          <p className="text-sm text-slate-500">Documents in notebook</p>
          <Link
            href={`/notebooks/${id}/documents`}
            className="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600"
          >
            View documents <span>→</span>
          </Link>
        </div>
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <span className="flex size-10 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
            <Layers3 className="size-5" />
          </span>
          <p className="mt-5 text-3xl font-semibold">{notebook.flashcards}</p>
          <p className="text-sm text-slate-500">Flashcards ready to review</p>
          <Link
            href={`/notebooks/${id}/flashcards`}
            className="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600"
          >
            Start reviewing <span>→</span>
          </Link>
        </div>
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50/50 p-5 md:col-span-2">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-white text-slate-400 shadow-sm">
              <Plus className="size-4" />
            </div>
            <div>
              <p className="text-sm font-semibold">Add more to this notebook</p>
              <p className="text-xs text-slate-500">
                Upload a document or generate study material.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
