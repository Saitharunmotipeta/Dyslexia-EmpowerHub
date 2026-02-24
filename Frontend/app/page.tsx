import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function LandingPage() {
  return (
    <div className="min-h-[80vh]">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-primary-100/50 px-4 py-16 sm:px-6 sm:py-24">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Learn at your pace, your way
          </h1>
          <p className="mt-4 text-lg text-gray-600 prose-readable">
            A dyslexia-friendly platform with level-based learning, voice practice,
            mock tests, and a supportive chatbot.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link href="/auth/register">
              <Button variant="primary" className="min-w-[160px]">
                Get started
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button variant="outline" className="min-w-[160px]">
                Log in
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Module cards */}
      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold text-gray-900">Modules</h2>
        <p className="mt-1 text-gray-600">Choose a module to start learning.</p>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { href: "/learning", title: "Learning", desc: "Level-based words and progress." },
            { href: "/practice", title: "Voice Test", desc: "Record and get feedback on pronunciation." },
            { href: "/mock", title: "Mock Test", desc: "Timed mock tests by level." },
            { href: "/dynamic", title: "Dynamic Learning", desc: "Type or say words and phrases." },
            { href: "/feedback", title: "Feedback", desc: "Trends, patterns, and recommendations." },
            { href: "/chatbot", title: "Chatbot", desc: "Ask questions and get guidance." },
          ].map(({ href, title, desc }) => (
            <Link key={href} href={href}>
              <article className="h-full rounded-2xl border border-gray-200 bg-white p-6 shadow-soft transition-shadow hover:shadow-soft-lg">
                <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
                <p className="mt-2 text-gray-600">{desc}</p>
                <span className="mt-3 inline-block text-sm font-medium text-primary-600">
                  Open →
                </span>
              </article>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
