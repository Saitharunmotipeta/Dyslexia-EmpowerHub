"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";

const features = [
  {
    icon: ICON_NAMES.BOOK,
    title: "Level-Based Learning",
    desc: "Progress through carefully structured levels with words and meanings suited to your pace.",
    definition: "Dyslexia is a specific learning disability affecting word recognition. Our sequential, spaced-repetition approach helps build solid reading foundations.",
  },
  {
    icon: ICON_NAMES.MICROPHONE,
    title: "Voice Practice",
    desc: "Record yourself, hear playback, and get real-time feedback on your pronunciation.",
    definition: "Many dyslexic learners benefit from multisensory engagement. Audio feedback strengthens phonetic awareness and builds fluency.",
  },
  {
    icon: ICON_NAMES.TARGET,
    title: "Mock Tests",
    desc: "Assess your skills with timed tests designed to build confidence and fluency.",
    definition: "Self-assessment in low-pressure environments helps dyslexic learners track progress and build confidence without shame.",
  },
  {
    icon: ICON_NAMES.LIGHTBULB,
    title: "Dynamic Learning",
    desc: "Learn through interactive exercises—type, speak, and see instant analysis.",
    definition: "Active, multisensory learning—combining visual, auditory, and kinesthetic input—is proven to improve retention for dyslexic readers.",
  },
  {
    icon: ICON_NAMES.TRENDING_UP,
    title: "Progress Insights",
    desc: "Understand your patterns and get personalized recommendations to improve.",
    definition: "Visual progress tracking and pattern recognition help dyslexic learners see improvement they might otherwise miss.",
  },
  {
    icon: ICON_NAMES.HELP,
    title: "Supportive Chatbot",
    desc: "Ask questions anytime and get guidance from our intelligent learning assistant.",
    definition: "24/7 support without judgment provides the encouragement dyslexic learners often need to persist through challenges.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen w-full">
      {/* ===== HERO SECTION ===== */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-primary-100/50 px-4 py-20 sm:px-6 sm:py-32">
        {/* Animated background blur elements */}
        <div className="absolute -left-40 -top-40 h-80 w-80 rounded-full bg-primary-300/20 blur-3xl animate-pulse" />
        <div className="absolute -right-40 -bottom-40 h-80 w-80 rounded-full bg-success-300/20 blur-3xl animate-pulse" />

        <div className="relative mx-auto max-w-4xl text-center">
          {/* Badge */}
          <div className="mb-6 inline-block">
            <span className="rounded-full bg-primary-100 px-4 py-2 text-sm font-medium text-primary-700 border border-primary-200">
              ✨ Dyslexia-Friendly Learning Platform
            </span>
          </div>

          {/* Main headline */}
          <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-7xl leading-tight">
            Learn to Read{" "}
            <span className="relative">
              <span className="absolute -inset-1 -skew-y-3 bg-primary-300/30" aria-hidden />
              <span className="relative text-primary-600">Your Way</span>
            </span>
          </h1>

          {/* Subheading */}
          <p className="prose-readable mt-8 text-lg sm:text-xl text-gray-600 mx-auto max-w-2xl">
            A comprehensive, AI-powered platform designed specifically for dyslexic learners. 
            Enjoy level-based lessons, voice practice, instant feedback, and personalized guidance 
            in a completely dyslexia-friendly environment.
          </p>

          {/* CTA Button */}
          <div className="mt-12">
            <Link href="/auth/login">
              <Button
                variant="outline"
                className="min-w-[200px] text-lg px-8 py-3 shadow-soft hover:shadow-soft-lg font-semibold border-2 border-primary-600 text-primary-600 hover:bg-primary-50"
                rightIcon={ICON_NAMES.ARROW_RIGHT}
              >
                Get Started
              </Button>
            </Link>
            <p className="mt-4 text-sm text-gray-500">
              No credit card required. Start learning in seconds.
            </p>
          </div>
        </div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-white">
        <div className="mx-auto max-w-6xl">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
              Everything You Need to Succeed
            </h2>
            <p className="prose-readable text-lg text-gray-600 max-w-2xl mx-auto">
              Our platform combines evidence-based learning strategies with cutting-edge AI 
              to create a truly accessible learning experience.
            </p>
          </div>

          {/* Feature cards grid */}
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative h-full rounded-2xl border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-8 shadow-soft transition-all duration-300 hover:shadow-soft-lg hover:border-primary-300 hover:-translate-y-1"
              >
                {/* Decorative top border accent */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-400 via-primary-500 to-transparent rounded-t-2xl opacity-0 group-hover:opacity-100 transition-opacity" />

                {/* Icon container */}
                <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-xl bg-primary-100 text-primary-600 group-hover:bg-primary-200 transition-colors">
                  <Icon name={feature.icon} size="lg" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="prose-readable text-gray-600">
                  {feature.desc}
                </p>

                {/* Hover indicator */}
                <div className="mt-6 pt-6 border-t border-gray-200 opacity-0 group-hover:opacity-100 transition-opacity">
                  <p className="text-sm text-primary-600 italic prose-readable">
                    {feature.definition}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== ABOUT US SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-gray-50 via-white to-gray-50">
        <div className="mx-auto max-w-5xl">
          <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
            {/* Left: Content */}
            <div>
              <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-6">
                Built for Every Learner
              </h2>
              <p className="prose-readable text-lg text-gray-600 mb-6">
                Dyslexia affects 1 in 5 individuals, yet most learning platforms aren't designed 
                with them in mind. We changed that.
              </p>
              <p className="prose-readable text-lg text-gray-600 mb-6">
                Our platform is built on years of research in dyslexia-friendly design:
              </p>
              
              {/* Features list with icons */}
              <ul className="space-y-4">
                {[
                  "Open Dyslexic font for maximum readability",
                  "Optimized spacing, contrast, and line height",
                  "Voice-first interactions with real-time feedback",
                  "Visual progress tracking and personalized insights",
                  "AI-powered guidance and adaptive learning paths",
                ].map((item, idx) => (
                  <li key={idx} className="flex items-start gap-3 prose-readable">
                    <Icon name={ICON_NAMES.CHECK} size="base" className="text-success-500 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Right: Why it works */}
            <div className="space-y-6">
              <div className="rounded-2xl border border-primary-200 bg-primary-50 p-8">
                <h3 className="text-lg font-semibold text-primary-900 mb-3">🧠 Evidence-Based Design</h3>
                <p className="prose-readable text-primary-800 text-sm">
                  Our approach is grounded in decades of dyslexia research. Every feature—from font choice to spacing to feedback mechanism—is informed by what actually works.
                </p>
              </div>

              <div className="rounded-2xl border border-success-200 bg-success-50 p-8">
                <h3 className="text-lg font-semibold text-success-900 mb-3">✨ Accessibility First</h3>
                <p className="prose-readable text-success-800 text-sm">
                  High contrast, customizable fonts, generous spacing, and multisensory engagement aren't afterthoughts—they're baked into every interaction.
                </p>
              </div>

              <div className="rounded-2xl border border-warning-200 bg-warning-50 p-8">
                <h3 className="text-lg font-semibold text-warning-900 mb-3">💪 Built on Courage</h3>
                <p className="prose-readable text-warning-800 text-sm">
                  We understand the frustration and shame that often accompany dyslexia. Our platform celebrates small wins, removes judgment, and builds genuine confidence.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== HOW IT WORKS SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-white">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="prose-readable text-lg text-gray-600 max-w-2xl mx-auto">
              A learning experience designed around you, not against you.
            </p>
          </div>

          <div className="grid gap-8 sm:grid-cols-3">
            {[
              {
                step: "1",
                title: "Start at Your Level",
                desc: "No pressure to keep up with others. Begin with foundational words and progress at your own pace through carefully structured levels.",
                icon: ICON_NAMES.TARGET,
              },
              {
                step: "2",
                title: "Learn Multisensorially",
                desc: "See it, hear it, say it, type it. Our platform engages multiple senses because that's how dyslexic brains learn best.",
                icon: ICON_NAMES.LIGHTBULB,
              },
              {
                step: "3",
                title: "Get Instant Feedback",
                desc: "Understand what you did well and what to improve—without judgment. Real-time feedback builds confidence and drives progress.",
                icon: ICON_NAMES.CHECK,
              },
            ].map((item, idx) => (
              <div key={idx} className="relative">
                {idx < 2 && (
                  <div className="hidden sm:block absolute top-16 -right-4 w-8 h-0.5 bg-gradient-to-r from-primary-400 to-transparent" />
                )}
                
                <div className="rounded-2xl border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-8 shadow-soft relative z-10">
                  <div className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-primary-600 text-white font-bold mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Icon name={item.icon} size="lg" className="text-primary-600" />
                    {item.title}
                  </h3>
                  <p className="prose-readable text-gray-600">
                    {item.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== WHY DIFFERENT SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-primary-50 via-white to-gray-50">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-12 text-center">
            Why We're Different
          </h2>

          <div className="grid gap-8 md:grid-cols-2">
            {[
              {
                title: "💚 Compassionate Design",
                desc: "We don't view dyslexia as a deficit—we see different strengths. Every feature celebrates how dyslexic brains actually work.",
              },
              {
                title: "🔍 Research-Backed",
                desc: "Our approach is grounded in decades of cognitive science and dyslexia research. We follow the evidence, not trends.",
              },
              {
                title: "🎯 No One-Size-Fits-All",
                desc: "Dyslexia looks different for everyone. Customizable fonts, spacing, and learning paths ensure you get what YOU need.",
              },
              {
                title: "🚀 Built for Growth",
                desc: "We don't just teach words—we build fluency, confidence, and genuine love for reading over time.",
              },
            ].map((item, idx) => (
              <div key={idx} className="rounded-2xl border border-gray-200 bg-white p-8 shadow-soft hover:shadow-soft-lg transition-shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {item.title}
                </h3>
                <p className="prose-readable text-gray-600">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== CONTACT/CTA SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-primary-600 via-primary-500 to-primary-700 text-white">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-4xl sm:text-5xl font-bold mb-6">
            Ready to Transform Your Learning?
          </h2>
          <p className="prose-readable text-lg text-primary-100 mb-12 max-w-2xl mx-auto">
            Join thousands of dyslexic learners who are building confidence and fluency 
            through personalized, accessible learning.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link href="/auth/login">
              <Button
                variant="primary"
                className="min-w-[200px] text-lg px-8 py-3 bg-white text-primary-600 hover:bg-gray-100"
                rightIcon={ICON_NAMES.ARROW_RIGHT}
              >
                Start Learning Now
              </Button>
            </Link>
          </div>

          {/* Contact information */}
          <div className="grid gap-8 sm:grid-cols-3 pt-12 border-t border-primary-400/30">
            {[
              { icon: ICON_NAMES.HELP, label: "Need Help?", value: "support@empowerhub.com" },
              { icon: ICON_NAMES.USER, label: "Partnership", value: "partners@empowerhub.com" },
              { icon: ICON_NAMES.LOCK, label: "Privacy", value: "privacy policy" },
            ].map((item, idx) => (
              <div key={idx} className="text-center">
                <Icon name={item.icon} size="lg" className="mx-auto mb-3 text-primary-100" />
                <p className="text-sm text-primary-100 mb-2">{item.label}</p>
                <p className="font-medium text-white hover:text-primary-100 cursor-pointer transition-colors">
                  {item.value}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="bg-gray-900 text-gray-400 px-4 py-12 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-8 sm:grid-cols-4 mb-8">
            <div>
              <h3 className="font-bold text-white mb-4">Product</h3>
              <ul className="space-y-2 text-sm">
                {["Learning", "Practice", "Mock Tests", "Feedback"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Company</h3>
              <ul className="space-y-2 text-sm">
                {["About", "Blog", "Careers", "Press"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Legal</h3>
              <ul className="space-y-2 text-sm">
                {["Privacy", "Terms", "Security", "Contact"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4">Connect</h3>
              <ul className="space-y-2 text-sm">
                {["Twitter", "LinkedIn", "Facebook", "Instagram"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 flex flex-col sm:flex-row justify-between items-center">
            <p className="text-sm mb-4 sm:mb-0">
              © 2026 Dyslexia EmpowerHub. All rights reserved.
            </p>
            <p className="text-sm">
              Built with <Icon name={ICON_NAMES.ZAPS} size="sm" className="inline text-yellow-400" /> for dyslexic learners
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
