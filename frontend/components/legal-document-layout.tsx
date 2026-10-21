import Link from "next/link";
import { ArrowLeft, ArrowUpRight, Sparkles } from "lucide-react";

type Section = { title: string; body?: string };

export function LegalDocumentLayout({
  title,
  intro,
  sections,
}: {
  title: string;
  intro: string;
  sections: Section[];
}) {
  return (
    <div className="min-h-screen bg-[#fbfbfd] text-slate-950">
      <header className="mx-auto flex h-20 max-w-6xl items-center justify-between px-5 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2.5 text-[18px] font-semibold"
        >
          <span className="flex size-8 items-center justify-center rounded-[10px] bg-indigo-600 text-white">
            <Sparkles className="size-4" />
          </span>
          cognix
        </Link>
        <Link
          href="/dashboard"
          className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-indigo-600"
        >
          <ArrowLeft className="size-4" /> Open app
        </Link>
      </header>
      <main className="mx-auto max-w-6xl px-5 pb-24 pt-12 lg:px-8">
        <div className="max-w-3xl">
          <p className="text-xs font-bold uppercase tracking-[.2em] text-indigo-600">
            Cognix policies
          </p>
          <h1 className="mt-5 text-5xl font-semibold tracking-[-.06em] text-slate-950 sm:text-6xl">
            {title}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-500">
            {intro}
          </p>
          <p className="mt-5 text-xs font-medium uppercase tracking-[.14em] text-slate-400">
            Last updated: [Date to be added]
          </p>
        </div>
        <div className="mt-16 grid gap-12 lg:grid-cols-[190px_1fr] lg:gap-20">
          <aside className="lg:sticky lg:top-8 lg:self-start">
            <p className="text-xs font-bold uppercase tracking-[.16em] text-slate-400">
              On this page
            </p>
            <nav className="mt-4 flex flex-col gap-2 border-l border-slate-200 pl-4">
              {sections.map((section, index) => (
                <a
                  key={section.title}
                  href={`#section-${index + 1}`}
                  className="text-sm leading-6 text-slate-500 hover:text-indigo-600"
                >
                  {index + 1}. {section.title}
                </a>
              ))}
            </nav>
          </aside>
          <article className="max-w-2xl">
            {sections.map((section, index) => (
              <section
                id={`section-${index + 1}`}
                key={section.title}
                className="scroll-mt-8 border-t border-slate-200 py-8 first:border-t-0 first:pt-0"
              >
                <h2 className="text-xl font-semibold tracking-tight">
                  {index + 1}. {section.title}
                </h2>
                <p className="mt-4 rounded-2xl border border-dashed border-slate-200 bg-white p-5 text-sm leading-7 text-slate-500">
                  {section.body ??
                    "[This section will be provided after legal review.]"}
                </p>
              </section>
            ))}
          </article>
        </div>
      </main>
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-8 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <p>© Cognix</p>
          <nav className="flex gap-5">
            <Link href="/privacy" className="hover:text-indigo-600">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-indigo-600">
              Terms
            </Link>
            <Link href="/cookies" className="hover:text-indigo-600">
              Cookies
            </Link>
            <Link
              href="/"
              className="flex items-center gap-1 hover:text-indigo-600"
            >
              Home <ArrowUpRight className="size-3" />
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  );
}
