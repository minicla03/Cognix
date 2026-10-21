"use client";
import { useState } from "react";
import { LockKeyhole, ShieldCheck } from "lucide-react";
export function SecuritySettings() {
  const [saved, setSaved] = useState(false);
  return (
    <div className="mx-auto max-w-5xl px-5 py-10 sm:px-8">
      <p className="text-xs font-bold uppercase tracking-[.18em] text-indigo-600">
        Settings
      </p>
      <h1 className="mt-3 text-3xl font-semibold tracking-[-.04em]">
        Security
      </h1>
      <p className="mt-2 text-sm text-slate-500">
        Manage your password and active sessions.
      </p>
      <div className="mt-10 grid gap-5 lg:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <LockKeyhole className="size-5 text-indigo-600" />
            <h2 className="font-semibold">Password</h2>
          </div>
          <div className="mt-5 flex flex-col gap-4">
            <label className="text-sm font-medium">
              Current password
              <input
                type="password"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
              />
            </label>
            <label className="text-sm font-medium">
              New password
              <input
                type="password"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
              />
            </label>
            <label className="text-sm font-medium">
              Confirm password
              <input
                type="password"
                className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
              />
            </label>
            <div className="text-xs text-slate-500">
              Password strength:{" "}
              <span className="font-medium text-slate-700">
                Enter a password to check
              </span>
            </div>
            <button
              onClick={() => setSaved(true)}
              className="w-fit rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white"
            >
              {saved ? "Password change queued" : "Change password"}
            </button>
          </div>
        </section>
        <section className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="flex items-center gap-3">
            <ShieldCheck className="size-5 text-indigo-600" />
            <h2 className="font-semibold">Active sessions</h2>
          </div>
          <div className="mt-5 rounded-xl bg-slate-50 p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Chrome · Windows</p>
                <p className="mt-1 text-xs text-slate-500">
                  Last active: recently · Current session
                </p>
              </div>
              <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-[11px] font-medium text-emerald-700">
                Current
              </span>
            </div>
          </div>
          <button className="mt-5 rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium hover:bg-slate-50">
            Sign out other sessions
          </button>
          <div className="mt-10 border-t border-slate-100 pt-6">
            <h2 className="font-semibold">Two-factor authentication</h2>
            <p className="mt-2 text-sm text-slate-500">Not enabled</p>
            <button
              disabled
              className="mt-4 rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-400"
            >
              Set up 2FA
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}
