"use client";

import { useRouter } from "next/navigation";

export default function LearningLevels() {
  const router = useRouter();

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <h1 className="text-4xl font-bold mb-8">Select Difficulty Level</h1>

      <div className="flex flex-col gap-4">
        <button
          onClick={() => router.push("/learning/levels/1/words")}
          className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600"
        >
          Easy
        </button>

        <button
          onClick={() => router.push("/learning/levels/2/words")}
          className="px-6 py-3 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600"
        >
          Medium
        </button>

        <button
          onClick={() => router.push("/learning/levels/3/words")}
          className="px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600"
        >
          Hard
        </button>
      </div>
    </main>
  );
}
