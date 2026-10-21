"use client";

import Link from "next/link";
import {
  ArrowUpRight,
  BookOpen,
  CheckCircle2,
  FileUp,
  MessageCircle,
  Plus,
  Search,
  Sparkles,
  Trophy,
} from "lucide-react";
import { useState } from "react";
import { notebooks, activity } from "@/lib/api/notebooks";
const icons = {
  upload: FileUp,
  quiz: Trophy,
  cards: CheckCircle2,
  chat: MessageCircle,
};

export default function DashboardPage() {
  const [search, setSearch] = useState("");
  const filtered = notebooks.filter((notebook) =>
    notebook.name.toLowerCase().includes(search.toLowerCase()),
  );
  return (
    <div className="mx-auto max-w-[1240px] px-5 py-8 sm:px-8 sm:py-10">
      <div className="mb-10 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <p className="mb-2 text-sm font-medium text-indigo-600">
            Tuesday, October 21, 2026
          </p>
          <h1 className="text-3xl font-semibold tracking-tight text-slate-950 sm:text-[34px]">
            Good morning, Sarah
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Pick up where you left off.
          </p>
        </div>
        <Link
          href="/notebooks/new"
          className="inline-flex w-fit items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-indigo-200 transition hover:bg-indigo-700"
        >
          <Plus className="size-4" />
          Create notebook
        </Link>
      </div>
      <section>
        <div className="mb-4 flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-base font-semibold">Your notebooks</h2>
            <p className="text-sm text-slate-500">
              Your personal learning spaces
            </p>
          </div>
          <div className="relative w-full sm:w-56">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search notebooks"
              className="h-9 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
            />
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((notebook) => (
            <Link
              key={notebook.id}
              href={`/notebooks/${notebook.id}`}
              className="group rounded-xl border border-slate-200/80 bg-white p-5 shadow-[0_2px_8px_rgba(15,23,42,0.02)] transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-md"
            >
              <div className="mb-7 flex items-start justify-between">
                <span
                  className={`flex size-10 items-center justify-center rounded-xl ${notebook.color}`}
                >
                  <BookOpen className="size-5" />
                </span>
                <ArrowUpRight className="size-4 text-slate-300 transition group-hover:text-indigo-500" />
              </div>
              <h3 className="font-semibold text-slate-900">{notebook.name}</h3>
              <p className="mt-1 line-clamp-1 text-sm text-slate-500">
                {notebook.description}
              </p>
              <div className="mt-6 flex items-center gap-4 text-xs text-slate-500">
                <span>{notebook.documents} documents</span>
                <span>{notebook.flashcards} cards</span>
                <span>{notebook.quizzes} quizzes</span>
              </div>
              <p className="mt-4 text-[11px] text-slate-400">
                Updated {notebook.updatedAt}
              </p>
            </Link>
          ))}
        </div>
      </section>
      <section className="mt-12">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold">Recent activity</h2>
            <p className="text-sm text-slate-500">
              Your latest learning progress
            </p>
          </div>
          <button className="text-sm font-medium text-indigo-600 hover:text-indigo-700">
            View all
          </button>
        </div>
        <div className="rounded-xl border border-slate-200/80 bg-white px-5">
          {activity.map((item, index) => {
            const Icon = icons[item.icon];
            return (
              <div
                key={item.id}
                className={`flex items-center gap-4 py-4 ${index < activity.length - 1 ? "border-b border-slate-100" : ""}`}
              >
                <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-slate-50 text-slate-500">
                  <Icon className="size-4" />
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-800">
                    {item.title}
                  </p>
                  <p className="truncate text-xs text-slate-500">
                    {item.detail}
                  </p>
                </div>
                <span className="text-xs text-slate-400">{item.time}</span>
              </div>
            );
          })}
        </div>
      </section>
      <div className="mt-10 flex items-start gap-3 rounded-xl border border-indigo-100 bg-indigo-50/60 p-4">
        <Sparkles className="mt-0.5 size-4 shrink-0 text-indigo-600" />
        <div>
          <p className="text-sm font-medium text-indigo-950">
            Make your next review count
          </p>
          <p className="mt-0.5 text-sm text-indigo-700/80">
            You have 8 flashcards due for review today.
          </p>
        </div>
        <Link
          href="/notebooks/anatomy/flashcards"
          className="ml-auto whitespace-nowrap text-sm font-semibold text-indigo-700 hover:text-indigo-900"
        >
          Review now <span aria-hidden="true">→</span>
        </Link>
      </div>
    </div>
  );
}
