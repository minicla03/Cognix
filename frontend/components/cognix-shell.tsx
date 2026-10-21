"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  ChevronLeft,
  ChevronRight,
  Command,
  FileText,
  LayoutDashboard,
  Menu,
  Plus,
  Settings,
  Sparkles,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Notebooks", href: "/notebooks", icon: BookOpen },
];
const settingsNavigation = [
  { label: "Privacy & Data", href: "/settings/privacy" },
  { label: "Security", href: "/settings/security" },
];

export function CognixShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isPublicRoute =
    pathname === "/" ||
    pathname === "/login" ||
    pathname === "/register" ||
    pathname === "/privacy" ||
    pathname === "/terms" ||
    pathname === "/cookies";
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  if (isPublicRoute) return <>{children}</>;

  return (
    <div className="min-h-screen bg-[#f8f9fb] text-slate-950">
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-[248px] flex-col border-r border-slate-200/80 bg-white transition-transform duration-200 lg:translate-x-0",
          collapsed && "lg:w-[76px]",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-[76px] items-center justify-between border-b border-slate-100 px-5">
          <Link
            href="/dashboard"
            className={cn("flex items-center gap-3", collapsed && "lg:mx-auto")}
            onClick={() => setMobileOpen(false)}
          >
            <span className="flex size-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm">
              <Sparkles className="size-4" />
            </span>
            <span
              className={cn(
                "text-[17px] font-semibold tracking-tight",
                collapsed && "lg:hidden",
              )}
            >
              cognix
            </span>
          </Link>
          <button
            aria-label="Close menu"
            className="lg:hidden"
            onClick={() => setMobileOpen(false)}
          >
            <X className="size-5 text-slate-400" />
          </button>
        </div>
        <div className="flex flex-1 flex-col px-3 py-6">
          <div
            className={cn(
              "mb-7 flex items-center justify-between px-3",
              collapsed && "lg:justify-center",
            )}
          >
            <span
              className={cn(
                "text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400",
                collapsed && "lg:hidden",
              )}
            >
              Workspace
            </span>
            <button
              className="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
              aria-label="Create notebook"
            >
              <Plus className="size-4" />
            </button>
          </div>
          <nav className="flex flex-col gap-1">
            {navigation.map((item) => {
              const active =
                pathname === item.href ||
                (item.href === "/notebooks" &&
                  pathname.startsWith("/notebooks/"));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    active
                      ? "bg-indigo-50 text-indigo-700"
                      : "text-slate-500 hover:bg-slate-50 hover:text-slate-900",
                    collapsed && "lg:justify-center lg:px-0",
                  )}
                >
                  <item.icon className="size-[18px]" />
                  <span className={cn(collapsed && "lg:hidden")}>
                    {item.label}
                  </span>
                </Link>
              );
            })}
          </nav>
          <div
            className={cn(
              "mb-3 mt-auto flex items-center justify-between px-3",
              collapsed && "lg:justify-center",
            )}
          >
            <span
              className={cn(
                "text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400",
                collapsed && "lg:hidden",
              )}
            >
              Manage
            </span>
          </div>
          <Link
            href="/settings/privacy"
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-500 hover:bg-slate-50 hover:text-slate-900",
              collapsed && "lg:justify-center lg:px-0",
            )}
          >
            <Settings className="size-[18px]" />
            <span className={cn(collapsed && "lg:hidden")}>Settings</span>
          </Link>
          <div
            className={cn(
              "mt-2 flex flex-col gap-1 border-l border-slate-100 pl-3",
              collapsed && "lg:hidden",
            )}
          >
            {settingsNavigation.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "rounded-lg px-3 py-2 text-xs font-medium",
                  pathname === item.href
                    ? "bg-indigo-50 text-indigo-700"
                    : "text-slate-400 hover:bg-slate-50 hover:text-slate-700",
                )}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
        <div
          className={cn("border-t border-slate-100 p-4", collapsed && "lg:p-3")}
        >
          <div
            className={cn(
              "flex items-center gap-3 rounded-xl bg-slate-50 p-2.5",
              collapsed && "lg:justify-center lg:bg-transparent",
            )}
          >
            <div className="flex size-8 items-center justify-center rounded-full bg-indigo-100 text-xs font-semibold text-indigo-700">
              SC
            </div>
            <div className={cn("min-w-0", collapsed && "lg:hidden")}>
              <p className="truncate text-sm font-medium">Sarah Chen</p>
              <p className="truncate text-xs text-slate-400">Free plan</p>
            </div>
          </div>
        </div>
      </aside>
      {mobileOpen && (
        <button
          aria-label="Close navigation"
          className="fixed inset-0 z-30 bg-slate-950/20 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}
      <div
        className={cn(
          "transition-[padding] duration-200 lg:pl-[248px]",
          collapsed && "lg:pl-[76px]",
        )}
      >
        <header className="sticky top-0 z-20 flex h-[76px] items-center justify-between border-b border-slate-200/80 bg-white/90 px-5 backdrop-blur-md sm:px-8">
          <div className="flex items-center gap-3">
            <button
              className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
              onClick={() => setMobileOpen(true)}
              aria-label="Open navigation"
            >
              <Menu className="size-5" />
            </button>
            <button className="hidden items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-400 hover:bg-slate-50 sm:flex">
              <Command className="size-4" />
              <span>Search anything...</span>
              <kbd className="ml-10 rounded border border-slate-200 bg-slate-50 px-1.5 py-0.5 text-[10px]">
                ⌘ K
              </kbd>
            </button>
            <button
              className="rounded-lg p-2 text-slate-500 sm:hidden"
              aria-label="Search"
            >
              <Command className="size-5" />
            </button>
          </div>
          <div className="flex items-center gap-3">
            <button
              className="hidden rounded-lg p-2 text-slate-400 hover:bg-slate-100 sm:block"
              aria-label="Toggle sidebar"
              onClick={() => setCollapsed(!collapsed)}
            >
              {collapsed ? (
                <ChevronRight className="size-4" />
              ) : (
                <ChevronLeft className="size-4" />
              )}
            </button>
            <div className="flex size-8 items-center justify-center rounded-full bg-indigo-100 text-xs font-semibold text-indigo-700">
              SC
            </div>
          </div>
        </header>
        <main>{children}</main>
      </div>
    </div>
  );
}
