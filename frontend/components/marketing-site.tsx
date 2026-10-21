"use client";

import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  Check,
  FileText,
  Languages,
  MessageSquare,
  Sparkles,
  Brain,
  Layers3,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

const features = [
  {
    icon: MessageSquare,
    title: "Ask your documents",
    copy: "Chat with your documents and get answers grounded in their content.",
  },
  {
    icon: FileText,
    title: "Cited answers",
    copy: "Trace every answer back to the relevant document and source.",
  },
  {
    icon: Layers3,
    title: "Learn with flashcards",
    copy: "Turn dense material into interactive decks you will remember.",
  },
  {
    icon: Brain,
    title: "Test yourself",
    copy: "Generate quizzes that make understanding measurable.",
  },
  {
    icon: BookOpen,
    title: "Organize in notebooks",
    copy: "Keep documents, conversations, and learning material together.",
  },
];

function Logo() {
  return (
    <Link
      href="/"
      className="flex items-center gap-2.5 text-[18px] font-semibold tracking-[-0.03em]"
    >
      <span className="flex size-8 items-center justify-center rounded-[10px] bg-indigo-600 text-white">
        <Sparkles className="size-4" />
      </span>
      cognix
    </Link>
  );
}

function Preview() {
  return (
    <div className="marketing-preview overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-[0_28px_80px_-30px_rgba(45,55,100,.35)]">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div className="flex items-center gap-2.5">
          <span className="flex size-7 items-center justify-center rounded-lg bg-indigo-600 text-white">
            <Sparkles className="size-3.5" />
          </span>
          <span className="text-sm font-semibold">cognix</span>
        </div>
        <span className="rounded-full bg-slate-50 px-3 py-1 text-[11px] text-slate-500">
          Anatomy · Notebook
        </span>
      </div>
      <div className="grid min-h-[330px] grid-cols-[150px_1fr]">
        <div className="border-r border-slate-100 bg-slate-50/70 p-4">
          <p className="mb-5 text-[9px] font-bold uppercase tracking-[.18em] text-slate-400">
            Workspace
          </p>
          <div className="flex flex-col gap-3 text-xs text-slate-500">
            <span className="flex items-center gap-2 rounded-lg bg-indigo-50 px-2.5 py-2 font-medium text-indigo-700">
              <FileText className="size-3.5" /> Documents
            </span>
            <span className="flex items-center gap-2 px-2.5">
              <MessageSquare className="size-3.5" /> Chat
            </span>
            <span className="flex items-center gap-2 px-2.5">
              <Layers3 className="size-3.5" /> Flashcards
            </span>
            <span className="flex items-center gap-2 px-2.5">
              <Brain className="size-3.5" /> Quiz
            </span>
          </div>
          <div className="mt-12 rounded-xl border border-slate-200 bg-white p-3">
            <p className="text-[10px] font-medium">3 sources</p>
            <p className="mt-1 text-[9px] text-slate-400">All in one place</p>
          </div>
        </div>
        <div className="p-6">
          <p className="text-[11px] font-medium text-slate-400">
            Ask your notebook
          </p>
          <p className="mt-3 text-base font-medium tracking-tight text-slate-900">
            What is the function of the adrenal gland?
          </p>
          <div className="mt-5 rounded-2xl bg-indigo-50/70 p-4">
            <div className="mb-2 flex items-center gap-2 text-[11px] font-semibold text-indigo-700">
              <Sparkles className="size-3.5" /> Cognix
            </div>
            <p className="text-xs leading-6 text-slate-600">
              The adrenal glands produce hormones involved in metabolism, immune
              response, blood pressure regulation, and the stress response.
            </p>
            <div className="mt-4 flex items-center gap-2 border-t border-indigo-100 pt-3 text-[10px] text-indigo-700">
              <FileText className="size-3" /> Anatomy.pdf{" "}
              <span className="text-slate-400">· page 42</span>
            </div>
          </div>
          <div className="mt-5 flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2.5 text-[10px] text-slate-400">
            <span className="size-1.5 rounded-full bg-indigo-500" /> Ask a
            follow-up question...
          </div>
        </div>
      </div>
    </div>
  );
}

export function MarketingSite() {
  const [open, setOpen] = useState(false);
  return (
    <div className="marketing min-h-screen bg-[#fbfbfd] text-slate-950">
      <header className="mx-auto flex h-20 max-w-6xl items-center justify-between px-5 lg:px-8">
        <Logo />
        <nav className="hidden items-center gap-8 text-sm text-slate-500 md:flex">
          <a href="#features">Product</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </nav>
        <div className="hidden items-center gap-5 md:flex">
          <Link href="/login" className="text-sm font-medium text-slate-600">
            Sign in
          </Link>
          <Link
            href="/register"
            className="rounded-full bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-700"
          >
            Get started <ArrowRight className="ml-1 inline size-4" />
          </Link>
        </div>
        <button
          className="md:hidden"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X /> : <Menu />}
        </button>
      </header>
      {open && (
        <div className="border-b border-slate-200 bg-white px-5 py-4 md:hidden">
          <div className="flex flex-col gap-4 text-sm">
            <a href="#features" onClick={() => setOpen(false)}>
              Features
            </a>
            <a href="#how-it-works" onClick={() => setOpen(false)}>
              How it works
            </a>
            <Link href="/login">Sign in</Link>
            <Link href="/register" className="font-semibold text-indigo-600">
              Get started
            </Link>
          </div>
        </div>
      )}
      <main>
        <section className="mx-auto grid max-w-6xl items-center gap-14 px-5 pb-24 pt-16 lg:grid-cols-[.86fr_1.14fr] lg:px-8 lg:pb-32 lg:pt-24">
          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[.16em] text-indigo-700">
              <Sparkles className="size-3" /> Document intelligence for learning
            </div>
            <h1 className="max-w-xl text-5xl font-semibold leading-[1.03] tracking-[-.065em] text-slate-950 sm:text-6xl">
              Turn your documents into{" "}
              <span className="text-indigo-600">knowledge.</span>
            </h1>
            <p className="mt-7 max-w-lg text-lg leading-8 text-slate-500">
              Upload your documents, ask questions, explore cited answers, and
              transform your material into interactive learning experiences.
            </p>
            <div className="mt-9 flex flex-wrap items-center gap-4">
              <Link
                href="/register"
                className="rounded-full bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_12px_25px_-10px_#4f46e5] transition hover:bg-indigo-700"
              >
                Start learning <ArrowRight className="ml-2 inline size-4" />
              </Link>
              <a
                href="#how-it-works"
                className="rounded-full border border-slate-200 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700"
              >
                See how it works
              </a>
            </div>
            <p className="mt-5 text-xs text-slate-400">
              Built for curious minds, serious study, and better questions.
            </p>
          </div>
          <Preview />
        </section>
        <section
          id="features"
          className="border-y border-slate-200/70 bg-white"
        >
          <div className="mx-auto max-w-6xl px-5 py-24 lg:px-8">
            <div className="max-w-xl">
              <p className="text-xs font-bold uppercase tracking-[.2em] text-indigo-600">
                One intelligent workspace
              </p>
              <h2 className="mt-4 text-4xl font-semibold tracking-[-.05em]">
                From reading to remembering.
              </h2>
              <p className="mt-4 leading-7 text-slate-500">
                Cognix connects the parts of learning that usually live in
                separate tabs.
              </p>
            </div>
            <div className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-slate-200 bg-slate-200 sm:grid-cols-2 lg:grid-cols-5">
              {features.map(({ icon: Icon, title, copy }) => (
                <article key={title} className="bg-white p-6">
                  <Icon className="size-5 text-indigo-600" />
                  <h3 className="mt-10 text-sm font-semibold">{title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {copy}
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>
        <section
          id="how-it-works"
          className="mx-auto max-w-6xl px-5 py-24 lg:px-8"
        >
          <div className="grid gap-14 lg:grid-cols-[.72fr_1.28fr]">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.2em] text-indigo-600">
                How it works
              </p>
              <h2 className="mt-4 text-4xl font-semibold tracking-[-.05em]">
                A clearer way to learn.
              </h2>
            </div>
            <div className="grid gap-8 sm:grid-cols-3">
              {[
                ["01", "Upload", "Upload your study or research material."],
                [
                  "02",
                  "Understand",
                  "Ask questions and explore grounded answers.",
                ],
                [
                  "03",
                  "Learn",
                  "Generate flashcards and quizzes to reinforce knowledge.",
                ],
              ].map(([num, title, copy]) => (
                <div key={num} className="border-t-2 border-indigo-600 pt-5">
                  <span className="text-xs font-bold text-indigo-600">
                    {num}
                  </span>
                  <h3 className="mt-8 text-xl font-semibold">{title}</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-500">
                    {copy}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
        <section className="bg-slate-950 text-white">
          <div className="mx-auto grid max-w-6xl items-center gap-12 px-5 py-24 lg:grid-cols-2 lg:px-8">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.2em] text-indigo-300">
                Grounded by sources
              </p>
              <h2 className="mt-4 text-4xl font-semibold tracking-[-.05em]">
                Know where your answer comes from.
              </h2>
              <p className="mt-5 max-w-md leading-7 text-slate-400">
                Cognix helps you explore your own material with context you can
                trace, revisit, and trust.
              </p>
              <div className="mt-8 flex flex-col gap-3 text-sm text-slate-300">
                <span className="flex items-center gap-3">
                  <Check className="size-4 text-indigo-300" /> Answers grounded
                  in your documents
                </span>
                <span className="flex items-center gap-3">
                  <Check className="size-4 text-indigo-300" /> Relevant sources
                  alongside every response
                </span>
                <span className="flex items-center gap-3">
                  <Check className="size-4 text-indigo-300" /> Conversations
                  organized by notebook
                </span>
              </div>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/[.06] p-6">
              <div className="text-xs text-slate-500">QUESTION</div>
              <p className="mt-3 text-lg">
                What is the function of the adrenal gland?
              </p>
              <div className="mt-7 rounded-xl bg-white p-5 text-slate-800">
                <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600">
                  <Sparkles className="size-3.5" /> Cognix answer
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  The adrenal glands produce hormones involved in metabolism,
                  immune response, and stress regulation.
                </p>
                <div className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-500">
                  <FileText className="mr-1 inline size-3.5 text-indigo-500" />{" "}
                  Anatomy.pdf <span className="text-slate-400">· p. 42</span>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="mx-auto max-w-6xl px-5 py-24 lg:px-8">
          <div className="rounded-[28px] bg-indigo-50 px-7 py-16 text-center sm:px-12">
            <Languages className="mx-auto size-6 text-indigo-600" />
            <h2 className="mt-5 text-4xl font-semibold tracking-[-.05em]">
              Learn in the language that feels like you.
            </h2>
            <p className="mx-auto mt-4 max-w-lg leading-7 text-slate-500">
              Interact with your documents across Italian, English, Spanish,
              French, and German.
            </p>
            <div className="mt-7 flex flex-wrap justify-center gap-2 text-xs font-medium text-indigo-700">
              {["Italian", "English", "Spanish", "French", "German"].map(
                (x) => (
                  <span key={x} className="rounded-full bg-white px-4 py-2">
                    {x}
                  </span>
                ),
              )}
            </div>
          </div>
        </section>
        <section className="border-t border-slate-200 bg-white">
          <div className="mx-auto max-w-6xl px-5 py-24 text-center lg:px-8">
            <h2 className="text-4xl font-semibold tracking-[-.05em]">
              Your documents already contain the knowledge.
            </h2>
            <p className="mt-4 text-slate-500">Cognix helps you explore it.</p>
            <Link
              href="/register"
              className="mt-8 inline-block rounded-full bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white"
            >
              Create your notebook <ArrowRight className="ml-2 inline size-4" />
            </Link>
          </div>
        </section>
      </main>
      <footer className="bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-8 border-t border-slate-200 px-5 py-10 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <Logo />
          <div className="flex flex-wrap gap-6">
            <a href="#features">Product</a>
            <a href="#how-it-works">How it works</a>
            <span>Documentation</span>
            <span>Privacy</span>
            <span>Terms</span>
          </div>
          <span>© Cognix</span>
        </div>
      </footer>
    </div>
  );
}
