"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Check, Eye, EyeOff, Sparkles } from "lucide-react";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const register = mode === "register";
  const [showPassword, setShowPassword] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  return (
    <div className="min-h-screen bg-[#fbfbfd] lg:grid lg:grid-cols-2">
      <div className="hidden flex-col justify-between bg-slate-950 p-10 text-white lg:flex">
        <Link
          href="/"
          className="flex items-center gap-2.5 text-lg font-semibold"
        >
          <span className="flex size-8 items-center justify-center rounded-lg bg-indigo-600">
            <Sparkles className="size-4" />
          </span>
          cognix
        </Link>
        <div className="max-w-md">
          <p className="text-xs font-bold uppercase tracking-[.2em] text-indigo-300">
            Document intelligence for learning
          </p>
          <h1 className="mt-5 text-5xl font-semibold leading-[1.05] tracking-[-.06em]">
            Make every document a starting point.
          </h1>
          <p className="mt-6 leading-7 text-slate-400">
            Ask better questions, follow the sources, and build knowledge that
            stays with you.
          </p>
        </div>
        <p className="text-xs text-slate-500">© Cognix</p>
      </div>
      <div className="flex min-h-screen items-center justify-center p-6">
        <div className="w-full max-w-[400px]">
          <Link
            href="/"
            className="mb-14 flex items-center gap-2.5 text-lg font-semibold lg:hidden"
          >
            <span className="flex size-8 items-center justify-center rounded-lg bg-indigo-600 text-white">
              <Sparkles className="size-4" />
            </span>
            cognix
          </Link>
          <div className="mb-8">
            <h2 className="text-3xl font-semibold tracking-[-.05em]">
              {register ? "Create your Cognix account" : "Welcome back"}
            </h2>
            <p className="mt-3 text-sm leading-6 text-slate-500">
              {register
                ? "Start turning your documents into knowledge."
                : "Continue learning with Cognix."}
            </p>
          </div>
          {submitted ? (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 text-sm text-emerald-800">
              <Check className="mb-3 size-5" />
              Thanks — your account request is ready to connect to
              authentication.
            </div>
          ) : (
            <form
              className="flex flex-col gap-5"
              onSubmit={(e) => {
                e.preventDefault();
                setSubmitted(true);
              }}
            >
              {register && (
                <label className="flex flex-col gap-2 text-sm font-medium">
                  Name
                  <input
                    required
                    name="name"
                    className="h-11 rounded-xl border border-slate-200 bg-white px-3 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
                    placeholder="Your name"
                  />
                </label>
              )}
              <label className="flex flex-col gap-2 text-sm font-medium">
                Email
                <input
                  required
                  type="email"
                  name="email"
                  className="h-11 rounded-xl border border-slate-200 bg-white px-3 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
                  placeholder="you@example.com"
                />
              </label>
              <label className="flex flex-col gap-2 text-sm font-medium">
                Password
                <div className="relative">
                  <input
                    required
                    minLength={8}
                    type={showPassword ? "text" : "password"}
                    name="password"
                    className="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 pr-11 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
                    placeholder="At least 8 characters"
                  />{" "}
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-slate-400"
                    aria-label="Toggle password visibility"
                  >
                    {showPassword ? (
                      <EyeOff className="size-4" />
                    ) : (
                      <Eye className="size-4" />
                    )}
                  </button>
                </div>
              </label>
              {register && (
                <label className="flex flex-col gap-2 text-sm font-medium">
                  Confirm password
                  <input
                    required
                    minLength={8}
                    type="password"
                    name="confirmPassword"
                    className="h-11 rounded-xl border border-slate-200 bg-white px-3 outline-none transition focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
                    placeholder="Repeat your password"
                  />
                </label>
              )}
              {!register && (
                <div className="-mt-2 text-right">
                  <button
                    type="button"
                    className="text-xs font-medium text-indigo-600"
                  >
                    Forgot password?
                  </button>
                </div>
              )}
              <button
                type="submit"
                className="h-12 rounded-xl bg-indigo-600 text-sm font-semibold text-white transition hover:bg-indigo-700"
              >
                {register ? "Create account" : "Sign in"}{" "}
                <ArrowRight className="ml-1 inline size-4" />
              </button>
              {register && (
                <p className="text-xs leading-5 text-slate-500">
                  By creating an account, you acknowledge that you have read the{" "}
                  <Link
                    href="/privacy"
                    className="font-medium text-indigo-600 hover:underline"
                  >
                    Privacy Policy
                  </Link>{" "}
                  and{" "}
                  <Link
                    href="/terms"
                    className="font-medium text-indigo-600 hover:underline"
                  >
                    Terms of Service
                  </Link>
                  .
                </p>
              )}
            </form>
          )}
          <p className="mt-7 text-center text-sm text-slate-500">
            {register ? "Already have an account?" : "Don't have an account?"}{" "}
            <Link
              href={register ? "/login" : "/register"}
              className="font-semibold text-indigo-600"
            >
              {register ? "Sign in" : "Create account"}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
