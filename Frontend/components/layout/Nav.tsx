"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

const mainLinks = [
  { href: "/learning", label: "Learning" },
  // { href: "/practice", label: "Voice Test" },
  // { href: "/mock", label: "Mock Test" },
  { href: "/dynamic", label: "Dynamic Learning" },
  // { href: "/feedback", label: "Feedback" },
  { href: "/chatbot", label: "Chatbot" },
];

export function Nav() {
  const pathname = usePathname();
  const { token, user, logout, checked } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 shadow-soft backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6" aria-label="Main">
        <Link
          href="/"
          className="text-xl font-bold text-primary-600 hover:text-primary-700"
        >
          Dyslexia EmpowerHub
        </Link>

        <div className="flex flex-wrap items-center justify-end gap-2 sm:gap-4">
          {mainLinks.map(({ href, label }) => {
            const isActive = pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={`
                  rounded-xl px-3 py-2 text-sm font-medium transition-colors
                  ${isActive ? "bg-primary-100 text-primary-700" : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"}
                `}
              >
                {label}
              </Link>
            );
          })}

          {!checked ? (
            <span className="text-sm text-gray-400">Loading…</span>
          ) : token && user ? (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600" title={user.email}>
                {user.name}
              </span>
              <button
                type="button"
                onClick={logout}
                className="rounded-xl px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              >
                Log out
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="rounded-xl px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              >
                Log in
              </Link>
              <Link
                href="/auth/register"
                className="rounded-2xl bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
