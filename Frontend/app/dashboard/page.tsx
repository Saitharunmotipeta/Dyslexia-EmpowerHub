"use client";

import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to Dyslexia EmpowerHub
        </h1>

        <p className="text-xl text-gray-700 mb-8">
          Your personalized learning companion for dyslexia support
        </p>

        <div className="flex flex-col gap-4 mt-8">
          <button
            onClick={() => {}}
            className="px-6 py-3 bg-gray-400 text-white rounded-lg"
          >
            Dynamic Module
          </button>

          <button
            onClick={() => router.push("/learning/levels")}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Learning Module
          </button>

          <button
            onClick={() => {}}
            className="px-6 py-3 bg-gray-400 text-white rounded-lg"
          >
            Chatbot
          </button>
        </div>
      </div>
    </main>
  );
}
