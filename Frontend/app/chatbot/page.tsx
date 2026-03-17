"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { chatbot, ApiError } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function ChatbotPage() {
  const router = useRouter();
  const { token, checked } = useAuth();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "bot"; text: string }>>([]);
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
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 transition-all duration-200 transform hover:scale-105 active:scale-95 font-medium text-sm shadow-soft"
        >
          <ArrowLeft size={18} className="transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Chatbot</h1>
        <p className="mt-1 text-gray-600">Ask questions and get guidance.</p>
      </div>

      <Card padding="none" className="flex flex-col overflow-hidden">
        <div className="flex max-h-[60vh] flex-1 flex-col overflow-y-auto p-4">
          {messages.length === 0 && (
            <p className="text-gray-500">Send a message to start.</p>
          )}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`mt-2 max-w-[85%] rounded-2xl px-4 py-3 ${
                msg.role === "user"
                  ? "ml-auto bg-primary-500 text-white"
                  : "bg-gray-100 text-gray-900"
              }`}
            >
              {msg.text}
            </div>
          ))}
          {loading && (
            <p className="mt-2 text-gray-500">Thinking…</p>
          )}
          <div ref={bottomRef} />
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex gap-2 border-t border-gray-200 p-4"
        >
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            maxLength={500}
            className="flex-1 rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200"
          />
          <Button type="submit" disabled={loading}>
            Send
          </Button>
        </form>

        {error && (
          <p className="px-4 pb-4 text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
      </Card>
    </div>
  );
}
