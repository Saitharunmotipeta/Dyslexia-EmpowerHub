"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";
import { assetUrl } from "@/constants/assets";

const features = [
  { icon: ICON_NAMES.BOOK, title: "Start Small" },
  { icon: ICON_NAMES.MICROPHONE, title: "Speak & Hear" },
  { icon: ICON_NAMES.TARGET, title: "No Stress" },
  { icon: ICON_NAMES.LIGHTBULB, title: "Learn by Doing" },
  { icon: ICON_NAMES.TRENDING_UP, title: "See Progress" },
  { icon: ICON_NAMES.HELP, title: "Always Help" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen w-full">
      {/* ===== HERO SECTION ===== */}
      <section className="relative overflow-hidden bg-gradient-to-br from-[#FDF6EC] via-[#EEF3FF] to-[#EAFBF5] px-4 py-20 sm:px-6 sm:py-32">
        {/* Soft background blur elements */}
        <div className="absolute -left-40 -top-40 h-80 w-80 rounded-full bg-[#6B8CA3]/10 blur-3xl transition-opacity duration-300" />
        <div className="absolute -right-40 -bottom-40 h-80 w-80 rounded-full bg-[#7FB77E]/10 blur-3xl transition-opacity duration-300" />

        <div className="relative mx-auto max-w-6xl">
          <div className="flex flex-col items-center gap-10 lg:flex-row lg:items-center lg:gap-12">
            {/* Left: study.gif — stacks below on mobile */}
            <div className="flex-shrink-0 w-full max-w-xs lg:max-w-sm lg:order-first animate-fade-rise">
              <img
                src={assetUrl("study.gif")}
                alt="Study"
                className="w-full h-auto object-contain rounded-xl shadow-sm transition-opacity duration-300"
              />
            </div>
            <div className="relative flex-1 mx-auto max-w-4xl text-center lg:text-left">
          {/* Badge */}
          <div className="mb-6 inline-block">
            <span className="rounded-full bg-[#E6E6FA]/60 px-4 py-2 text-sm font-medium text-[#6B8CA3] border border-[#6B8CA3]/30 leading-relaxed tracking-wide">
              ✨ Dyslexia-Friendly Learning Platform
            </span>
          </div>

          {/* Main headline */}
          <h1 className="text-5xl font-bold tracking-wide text-[#1A1A1A] sm:text-6xl lg:text-7xl leading-tight">
            Learn to Read{" "}
            <span className="relative">
              <span className="absolute -inset-1 -skew-y-3 bg-[#6B8CA3]/20" aria-hidden />
              <span className="relative text-[#6B8CA3]">Your Way</span>
            </span>
          </h1>

          {/* Subheading */}
          <p className="prose-readable mt-8 text-lg sm:text-xl text-[#333333] mx-auto max-w-2xl">
            A comprehensive, AI-powered platform designed specifically for dyslexic learners. 
            Enjoy level-based lessons, voice practice, instant feedback, and personalized guidance 
            in a completely dyslexia-friendly environment.
          </p>

          {/* CTA Button */}
          <div className="mt-12">
            <Link href="/auth/login">
              <Button
                variant="outline"
                className="min-w-[200px] text-lg px-8 py-3 shadow-soft font-semibold border-2 border-[#6B8CA3] text-[#6B8CA3] hover:bg-[#FAF3DD]/80 hover:scale-105 transition-all duration-200"
                rightIcon={ICON_NAMES.ARROW_RIGHT}
              >
                Get Started
              </Button>
            </Link>
            <p className="mt-4 text-sm text-[#333333] leading-relaxed">
              No credit card required. Start learning in seconds.
            </p>
          </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-[#F7F8FA]">
        <div className="mx-auto max-w-6xl">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-dyslexia-text-primary mb-4 leading-relaxed tracking-wide">
              Everything You Need to Succeed
            </h2>
            <p className="prose-readable text-lg text-dyslexia-text-secondary max-w-2xl mx-auto">
              Our platform combines evidence-based learning strategies with cutting-edge AI 
              to create a truly accessible learning experience.
            </p>
          </div>

          {/* Feature cards grid */}
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div
              key={index}
              className="group relative rounded-2xl p-6 overflow-hidden transition-all duration-500 
              hover:scale-105 animate-fadeUp"
              style={{
                background: [
                  "linear-gradient(135deg,#EEF3FF,#EAFBF5)",
                  "linear-gradient(135deg,#F3E8FF,#EEF3FF)",
                  "linear-gradient(135deg,#FFF4E6,#EAFBF5)",
                  "linear-gradient(135deg,#EAFBF5,#F3E8FF)",
                  "linear-gradient(135deg,#EEF3FF,#FFF4E6)",
                  "linear-gradient(135deg,#FDEDEC,#EEF3FF)",
                ][index],
              }}
            >
              {/* Glow effect */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 
                bg-[radial-gradient(circle_at_center,rgba(107,140,163,0.25),transparent_70%)]" />
            
              {/* Floating icon */}
              <div className="mb-4 transform group-hover:-translate-y-2 transition duration-500">
                <div className="w-14 h-14 flex items-center justify-center rounded-xl bg-white shadow-md">
                  <Icon name={feature.icon} size="lg" />
                </div>
              </div>
            
              {/* Title */}
              <h3 className="text-lg font-semibold tracking-wide">
                {feature.title}
              </h3>
            
              {/* Subtle line */}
              <div className="mt-3 h-1 w-8 bg-[#6B8CA3] rounded-full group-hover:w-16 transition-all duration-500" />
            </div>
            ))}
          </div>
        </div>
      </section>

        {/* ===== BANNER + GIF SPLIT SECTION ===== */}
        <section className="px-4 sm:px-6 py-20 bg-dyslexia-bg-primary animate-[fadeRiseSoft_0.9s_ease-out_forwards]">
        <div className="mx-auto max-w-6xl grid gap-12 lg:grid-cols-2 items-center">
          
          {/* LEFT: Banner */}
          <div className="flex flex-col justify-center animate-fade-rise">
            <img
              src={assetUrl("banner.jpeg")}
              alt="Learning banner"
              className="w-full h-auto object-cover rounded-2xl shadow-md"
            />
            <p className="mt-6 text-xl font-semibold text-dyslexia-text-primary text-center leading-relaxed tracking-wide">
            Reading is hard.
            <br />
            It doesn't have to be.
            <br />
            Learn at your pace. Without pressure. Without judgment.
            </p>
          </div>

          {/* RIGHT: GIF */}
          <div className="flex justify-center lg:justify-end animate-fade-rise">
            <div className="w-full max-w-lg rounded-2xl overflow-hidden shadow-md bg-[#F4F4F4]">
              <img
                src={assetUrl("landingpagefrnds.gif")}
                alt="Friends learning"
                className="w-full h-full object-cover"
              />
            </div>
          </div>

        </div>
      </section>

      {/* ===== ABOUT US SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-dyslexia-bg-secondary via-dyslexia-bg-primary to-dyslexia-bg-secondary">
        <div className="mx-auto max-w-5xl">
          <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
            {/* Left: Content */}
            <div>
              <h2 className="text-4xl sm:text-5xl font-bold text-dyslexia-text-primary mb-6 leading-relaxed tracking-wide">
                Built for Every Learner
              </h2>
              <p className="prose-readable text-lg text-dyslexia-text-secondary mb-6">
                Dyslexia affects 1 in 5 individuals, yet most learning platforms aren't designed 
                with them in mind. We changed that.
              </p>
              <p className="prose-readable text-lg text-dyslexia-text-secondary mb-6">
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
                    <Icon name={ICON_NAMES.CHECK} size="base" className="text-dyslexia-accent-green flex-shrink-0 mt-0.5" />
                    <span className="text-dyslexia-text-secondary">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Right: Why it works */}
            <div className="space-y-6">
              <div className="rounded-2xl border border-[#6B8CA3]/30 bg-[#6B8CA3]/10 p-8 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-md">
                <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-3 leading-relaxed tracking-wide">🧠 Evidence-Based Design</h3>
                <p className="prose-readable text-dyslexia-text-secondary text-sm">
                  Our approach is grounded in decades of dyslexia research. Every feature—from font choice to spacing to feedback mechanism—is informed by what actually works.
                </p>
              </div>

              <div className="rounded-2xl border border-[#7FB77E]/30 bg-[#7FB77E]/10 p-8 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-md">
                <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-3 leading-relaxed tracking-wide">✨ Accessibility First</h3>
                <p className="prose-readable text-dyslexia-text-secondary text-sm">
                  High contrast, customizable fonts, generous spacing, and multisensory engagement aren't afterthoughts—they're baked into every interaction.
                </p>
              </div>

              <div className="rounded-2xl border border-[#A78BFA]/30 bg-[#A78BFA]/10 p-8 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-md">
                <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-3 leading-relaxed tracking-wide">💪 Built on Courage</h3>
                <p className="prose-readable text-dyslexia-text-secondary text-sm">
                  We understand the frustration and shame that often accompany dyslexia. Our platform celebrates small wins, removes judgment, and builds genuine confidence.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== HOW IT WORKS SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-dyslexia-bg-primary">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl sm:text-5xl font-bold text-dyslexia-text-primary mb-4 leading-relaxed tracking-wide">
              How It Works
            </h2>
            <p className="prose-readable text-lg text-dyslexia-text-secondary max-w-2xl mx-auto">
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
              <div key={idx} className="relative animate-fade-rise" style={{ animationDelay: `${idx * 80}ms` }}>
                {idx < 2 && (
                  <div className="hidden sm:block absolute top-16 -right-4 w-8 h-0.5 bg-gradient-to-r from-dyslexia-accent-blue to-transparent" />
                )}
                
                <div className="rounded-2xl border border-[#E8E4DC] bg-gradient-to-br from-dyslexia-bg-primary to-dyslexia-bg-secondary p-8 shadow-soft relative z-10 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-md">
                  <div className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-dyslexia-accent-blue text-white font-bold mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold text-dyslexia-text-primary mb-3 flex items-center gap-2 leading-relaxed tracking-wide">
                    <Icon name={item.icon} size="lg" className="text-dyslexia-accent-blue" />
                    {item.title}
                  </h3>
                  <p className="prose-readable text-dyslexia-text-secondary">
                    {item.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== WHY DIFFERENT SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-[#6B8CA3]/10 via-dyslexia-bg-primary to-[#A78BFA]/10">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-4xl sm:text-5xl font-bold text-dyslexia-text-primary mb-12 text-center leading-relaxed tracking-wide">
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
              <div key={idx} className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary p-8 shadow-soft transition-all duration-300 ease-out hover:shadow-md hover:-translate-y-1">
                <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-3 leading-relaxed tracking-wide">
                  {item.title}
                </h3>
                <p className="prose-readable text-dyslexia-text-secondary">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== CONTACT/CTA SECTION ===== */}
      <section className="relative px-4 py-20 sm:px-6 sm:py-28 bg-gradient-to-br from-dyslexia-accent-blue via-[#5a7a8f] to-dyslexia-accent-purple/80 text-white">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-4xl sm:text-5xl font-bold mb-6 leading-relaxed tracking-wide">
            Ready to Transform Your Learning?
          </h2>
          <p className="prose-readable text-lg text-white/90 mb-12 max-w-2xl mx-auto">
            Join thousands of dyslexic learners who are building confidence and fluency 
            through personalized, accessible learning.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link href="/auth/login">
              <Button
                variant="primary"
                className="min-w-[200px] text-lg px-8 py-3 bg-dyslexia-bg-primary text-dyslexia-accent-blue hover:bg-dyslexia-bg-secondary transition-all duration-200"
                rightIcon={ICON_NAMES.ARROW_RIGHT}
              >
                Start Learning Now
              </Button>
            </Link>
          </div>

          {/* Contact information */}
          <div className="grid gap-8 sm:grid-cols-3 pt-12 border-t border-white/20">
            {[
              { icon: ICON_NAMES.HELP, label: "Need Help?", value: "support@empowerhub.com" },
              { icon: ICON_NAMES.USER, label: "Partnership", value: "partners@empowerhub.com" },
              { icon: ICON_NAMES.LOCK, label: "Privacy", value: "privacy policy" },
            ].map((item, idx) => (
              <div key={idx} className="text-center">
                <Icon name={item.icon} size="lg" className="mx-auto mb-3 text-white/80" />
                <p className="text-sm text-white/80 mb-2">{item.label}</p>
                <p className="font-medium text-white hover:text-white/90 cursor-pointer transition-colors duration-200">
                  {item.value}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer
        className="relative text-white/80 px-4 py-12 sm:px-6"
        style={{
          backgroundImage: `url(${assetUrl("footer.jpeg")})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <div className="absolute inset-0 bg-[#1A1A1A]/85" aria-hidden />
        <div className="relative mx-auto max-w-6xl">
          <div className="grid gap-8 sm:grid-cols-4 mb-8">
            <div>
              <h3 className="font-bold text-white mb-4 leading-relaxed tracking-wide">Product</h3>
              <ul className="space-y-2 text-sm leading-relaxed tracking-wide">
                {["Learning", "Practice", "Mock Tests", "Feedback"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4 leading-relaxed tracking-wide">Company</h3>
              <ul className="space-y-2 text-sm leading-relaxed tracking-wide">
                {["About", "Blog", "Careers", "Press"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4 leading-relaxed tracking-wide">Legal</h3>
              <ul className="space-y-2 text-sm leading-relaxed tracking-wide">
                {["Privacy", "Terms", "Security", "Contact"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-white mb-4 leading-relaxed tracking-wide">Connect</h3>
              <ul className="space-y-2 text-sm leading-relaxed tracking-wide">
                {["Twitter", "LinkedIn", "Facebook", "Instagram"].map((item) => (
                  <li key={item}>
                    <a href="#" className="hover:text-white transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border-t border-white/20 pt-8 flex flex-col sm:flex-row justify-between items-center">
            <p className="text-sm mb-4 sm:mb-0 leading-relaxed tracking-wide">
              © 2026 Dyslexia EmpowerHub. All rights reserved.
            </p>
            <p className="text-sm leading-relaxed tracking-wide">
              Built with <Icon name={ICON_NAMES.ZAPS} size="sm" className="inline text-dyslexia-accent-purple" /> for dyslexic learners
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
