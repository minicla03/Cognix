"use client";
import { useState } from "react";
import Link from "next/link";
import {
  AlertTriangle,
  Check,
  Download,
  Info,
  LockKeyhole,
  ShieldCheck,
  Trash2,
  X,
} from "lucide-react";
import { requestDataExport } from "@/lib/api/privacy";
const summary = [
  { label: "Documents", value: "12" },
  { label: "Conversations", value: "48" },
  { label: "Flashcards", value: "124" },
  { label: "Quizzes", value: "8" },
  { label: "Storage", value: "245 MB" },
];
function ConfirmDialog({
  title,
  children,
  onClose,
  onConfirm,
}: {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
  onConfirm: () => void;
}) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/30 p-5"
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl"
      >
        <div className="flex items-start justify-between">
          <h2 id="confirm-title" className="text-lg font-semibold">
            {title}
          </h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100"
          >
            <X className="size-4" />
          </button>
        </div>
        <p className="mt-3 text-sm leading-6 text-slate-500">{children}</p>
        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="rounded-lg bg-slate-950 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
export function PrivacyDashboard() {
  const [dialog, setDialog] = useState<
    "documents" | "conversations" | "account" | null
  >(null);
  const [exportStatus, setExportStatus] = useState("idle");
  const [aiOpen, setAiOpen] = useState(false);
  const startExport = async () => {
    setExportStatus("requesting");
    try {
      await requestDataExport();
      setExportStatus("processing");
      window.setTimeout(() => setExportStatus("ready"), 1200);
    } catch {
      setExportStatus("error");
    }
  };
  return (
    <div className="mx-auto max-w-5xl px-5 py-10 sm:px-8">
      <div className="mb-10">
        <p className="text-xs font-bold uppercase tracking-[.18em] text-indigo-600">
          Settings
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-[-.04em]">
          Privacy & Data
        </h1>
        <p className="mt-2 max-w-xl text-sm leading-6 text-slate-500">
          Manage your data, export a copy, and review privacy preferences. These
          controls will connect to your account services.
        </p>
      </div>
      <section>
        <h2 className="text-lg font-semibold">Your data</h2>
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-5">
          {summary.map((item) => (
            <div
              key={item.label}
              className="rounded-2xl border border-slate-200 bg-white p-4"
            >
              <p className="text-2xl font-semibold tracking-tight">
                {item.value}
              </p>
              <p className="mt-1 text-xs text-slate-500">{item.label}</p>
            </div>
          ))}
        </div>
      </section>
      <div className="mt-8 grid gap-5 lg:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="font-semibold">Export your data</h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                Request a copy of the data associated with your Cognix account.
              </p>
            </div>
            <Download className="size-5 text-indigo-600" />
          </div>
          <button
            onClick={startExport}
            disabled={
              exportStatus === "requesting" || exportStatus === "processing"
            }
            className="mt-5 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white disabled:opacity-60"
          >
            {exportStatus === "idle"
              ? "Request data export"
              : exportStatus === "ready"
                ? "Download export"
                : exportStatus === "error"
                  ? "Try again"
                  : exportStatus[0].toUpperCase() + exportStatus.slice(1)}
          </button>
          {exportStatus === "ready" && (
            <p className="mt-3 flex items-center gap-2 text-xs text-emerald-700">
              <Check className="size-3.5" /> Your export is ready.
            </p>
          )}
        </section>
        <section className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="font-semibold">Privacy preferences</h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                Optional categories are not configured.
              </p>
            </div>
            <ShieldCheck className="size-5 text-indigo-600" />
          </div>
          <div className="mt-5 flex flex-col gap-3 text-sm">
            <div className="flex justify-between">
              <span>Necessary cookies</span>
              <span className="text-xs font-medium text-slate-400">
                Always active
              </span>
            </div>
            <div className="flex justify-between">
              <span>Analytics</span>
              <span className="text-xs text-slate-400">Not configured</span>
            </div>
            <div className="flex justify-between">
              <span>Marketing</span>
              <span className="text-xs text-slate-400">Not configured</span>
            </div>
          </div>
        </section>
      </div>
      <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="font-semibold">Your documents</h2>
        <p className="mt-2 text-sm text-slate-500">
          12 documents · 245 MB used
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link
            href="/notebooks"
            className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium hover:bg-slate-50"
          >
            View documents
          </Link>
          <button
            onClick={() => setDialog("documents")}
            className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50"
          >
            Delete selected
          </button>
          <button
            onClick={() => setDialog("documents")}
            className="rounded-lg px-4 py-2.5 text-sm font-medium text-slate-500 hover:bg-slate-100"
          >
            Delete all documents
          </button>
        </div>
      </section>
      <section className="mt-5 rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="font-semibold">Conversation history</h2>
        <p className="mt-2 text-sm text-slate-500">48 conversations</p>
        <div className="mt-5 flex flex-wrap gap-3">
          <button
            onClick={() => setDialog("conversations")}
            className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50"
          >
            Delete conversation
          </button>
          <button
            onClick={() => setDialog("conversations")}
            className="rounded-lg px-4 py-2.5 text-sm font-medium text-slate-500 hover:bg-slate-100"
          >
            Delete all conversations
          </button>
        </div>
      </section>
      <section className="mt-5 rounded-2xl border border-red-200 bg-red-50/40 p-6">
        <div className="flex gap-3">
          <AlertTriangle className="mt-0.5 size-5 text-red-600" />
          <div>
            <h2 className="font-semibold">Danger Zone</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Permanently delete your Cognix account and associated data.
            </p>
            <button
              onClick={() => setDialog("account")}
              className="mt-5 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-red-700"
            >
              Delete account
            </button>
          </div>
        </div>
      </section>
      <div className="mt-6 flex flex-wrap gap-4 text-xs text-slate-500">
        <button
          onClick={() => setAiOpen(true)}
          className="flex items-center gap-1.5 hover:text-indigo-600"
        >
          <Info className="size-3.5" /> About AI processing
        </button>
        <Link href="/privacy" className="hover:text-indigo-600">
          Learn more about data handling
        </Link>
      </div>
      {aiOpen && (
        <ConfirmDialog
          title="About AI processing"
          onClose={() => setAiOpen(false)}
          onConfirm={() => setAiOpen(false)}
        >
          Information about how your content is processed by AI services will be
          provided here.
        </ConfirmDialog>
      )}
      {dialog && (
        <ConfirmDialog
          title={dialog === "account" ? "Delete account?" : `Delete ${dialog}?`}
          onClose={() => setDialog(null)}
          onConfirm={() => setDialog(null)}
        >
          This action will permanently remove the selected data. The final
          behavior and processing details will be defined by the connected
          backend.
        </ConfirmDialog>
      )}
    </div>
  );
}
