"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";

const mainLinks = [
  { href: "/learning", label: "Learning", icon: ICON_NAMES.BOOK },
  { href: "/dynamic", label: "Dynamic", icon: ICON_NAMES.LIGHTBULB },
  { href: "/chatbot", label: "Chatbot", icon: ICON_NAMES.HELP },
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
          Dyslexia Smart EmpowerHub using AI
        </Link>

        <div className="flex flex-wrap items-center justify-end gap-2 sm:gap-4">
          {token && user && (
            <>
              {mainLinks.map(({ href, label, icon }) => {
                const isActive = pathname.startsWith(href);
                return (
                  <Link
                    key={href}
                    href={href}
                    className={`
                      rounded-xl px-3 py-2 text-sm font-medium transition-colors inline-flex items-center gap-1
                      ${isActive ? "bg-primary-100 text-primary-700" : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"}
                    `}
                  >
                    <Icon name={icon} size="sm" />
                    {label}
                  </Link>
                );
              })}
            </>
          )}

          {!checked ? (
            <span className="text-sm text-gray-400">Loading…</span>
          ) : token && user ? (
            <div className="flex items-center gap-3">
              <Link
                href="/dashboard/profile"
                className="rounded-xl px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 inline-flex items-center gap-1"
              >
                <Icon name={ICON_NAMES.USER} size="sm" />
                <span className="hidden sm:inline">{user.name}</span>
              </Link>
              <button
                type="button"
                onClick={logout}
                className="rounded-xl p-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
                title="Log out"
                aria-label="Log out"
              >
                <Icon name={ICON_NAMES.LOGOUT} size="base" />
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="rounded-xl px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 inline-flex items-center gap-1"
              >
                <Icon name={ICON_NAMES.LOGIN} size="sm" />
                Sign In
              </Link>
              <Link
                href="/auth/register"
                className="rounded-2xl bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600 flex items-center gap-1"
              >
                <Icon name={ICON_NAMES.USER} size="sm" />
                Sign Up
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
