"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";
import { assetUrl } from "@/constants/assets";

const mainLinks = [
  { href: "/learning", label: "Learning", icon: ICON_NAMES.BOOK },
  { href: "/dynamic", label: "Dynamic", icon: ICON_NAMES.LIGHTBULB },
  { href: "/chatbot", label: "Chatbot", icon: ICON_NAMES.HELP },
];

export function Nav() {
  const pathname = usePathname();
  const { token, user, logout, checked } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b border-[#E8E4DC] bg-dyslexia-bg-primary/95 shadow-soft backdrop-blur transition-all duration-300 ease-out">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6" aria-label="Main">
      <Link
        href="/"
        className="flex items-center gap-2 group"
      >
        <img
          src={assetUrl("logo.png")}
          alt="logo"
          className="h-20 w-auto object-contain transition-transform duration-300 group-hover:scale-105"
        />

        <span className="text-lg font-bold text-[#4A6FA5] group-hover:text-[#6B8CA3] transition">
          Dyslexia EmpowerHub
        </span>
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
                      rounded-xl px-3 py-2 text-sm font-medium transition-all duration-200 ease-out inline-flex items-center gap-1 leading-relaxed tracking-wide
                      ${isActive ? "bg-[#6B8CA3]/15 text-dyslexia-accent-blue" : "text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary"}
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
            <span className="text-sm text-dyslexia-text-secondary">Loading…</span>
          ) : token && user ? (
            <div className="flex items-center gap-3">
              <Link
                href="/dashboard/profile"
                className="rounded-xl px-3 py-2 text-sm font-medium text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary transition-all duration-200 inline-flex items-center gap-1 leading-relaxed tracking-wide"
              >
                <Icon name={ICON_NAMES.USER} size="sm" />
                <span className="hidden sm:inline">{user.name}</span>
              </Link>
              <button
                type="button"
                onClick={logout}
                className="rounded-xl p-2 text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary transition-all duration-200"
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
                className="rounded-xl px-3 py-2 text-sm font-medium text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary transition-all duration-200 inline-flex items-center gap-1 leading-relaxed tracking-wide"
              >
                <Icon name={ICON_NAMES.LOGIN} size="sm" />
                Sign In
              </Link>
              <Link
                href="/auth/register"
                className="rounded-2xl bg-dyslexia-accent-blue px-4 py-2 text-sm font-medium text-white hover:opacity-90 flex items-center gap-1 transition-all duration-200 leading-relaxed tracking-wide"
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
