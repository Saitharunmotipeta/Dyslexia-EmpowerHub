"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { chatbot, ApiError } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { assetUrl } from "@/constants/assets";

export default function ChatbotPage() {
  const router = useRouter();
  const { token, checked } = useAuth();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    Array<{ role: "user" | "bot"; text: string }>
  >([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) router.push("/auth/login");
  }, [token, checked, router]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = message.trim();
    if (!text || loading) return;

    setMessage("");
    setMessages((m) => [...m, { role: "user", text }]);
    setLoading(true);
    setError(null);

    try {
      const res = await chatbot.chat({ message: text });
      setMessages((m) => [...m, { role: "bot", text: res.reply }]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Send failed");
    } finally {
      setLoading(false);
    }
  };

  if (!checked || !token) return null;

  return (
    <div
      className="relative min-h-screen flex items-center justify-center px-4 py-10 sm:px-6"
      style={{
        backgroundImage: `url(${assetUrl("chatbot.jpeg")})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* 🔥 OVERLAY */}
      <div className="absolute inset-0 bg-[#FDF6EC]/90 backdrop-blur-sm" />

      {/* CONTENT */}
      <div className="relative w-full max-w-5xl">

        {/* HEADER */}
        <div className="mb-8">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#A78BFA]/15 text-dyslexia-accent-purple hover:bg-[#A78BFA]/25 transition-all duration-200 hover:scale-105 active:scale-95 text-sm"
          >
            <ArrowLeft size={18} />
            Back to Dashboard
          </Link>

          <h1 className="mt-2 text-3xl font-bold text-dyslexia-text-primary">
            Chatbot
          </h1>

          <p className="mt-1 text-dyslexia-text-secondary">
            Ask questions and get guidance.
          </p>
        </div>

        {/* CHAT CARD */}
        <div className="flex justify-center">
          <div className="w-full max-w-2xl">

            <Card className="flex flex-col overflow-hidden rounded-2xl shadow-md">

              {/* CHAT AREA */}
              <div className="flex max-h-[60vh] flex-1 flex-col overflow-y-auto p-4">

                {messages.length === 0 && (
                  <p className="text-dyslexia-text-secondary">
                    Send a message to start.
                  </p>
                )}

                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`mt-2 max-w-[85%] rounded-2xl px-4 py-3 ${
                      msg.role === "user"
                        ? "ml-auto bg-dyslexia-accent-blue text-white"
                        : "bg-dyslexia-bg-secondary text-dyslexia-text-primary"
                    }`}
                  >
                    {msg.text}
                  </div>
                ))}

                {loading && (
                  <p className="mt-2 text-dyslexia-text-secondary">
                    Thinking...
                  </p>
                )}

                <div ref={bottomRef} />
              </div>

              {/* INPUT */}
              <form
                onSubmit={handleSubmit}
                className="flex gap-2 border-t border-[#E8E4DC] p-4"
              >
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your message..."
                  maxLength={500}
                  className="flex-1 rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-secondary px-4 py-3 focus:border-dyslexia-accent-blue focus:outline-none focus:ring-2 focus:ring-dyslexia-accent-blue/20"
                />

                <Button type="submit" disabled={loading}>
                  Send
                </Button>
              </form>

              {error && (
                <p className="px-4 pb-4 text-sm text-dyslexia-accent-purple">
                  {error}
                </p>
              )}

            </Card>

          </div>
        </div>

      </div>
    </div>
  );
}