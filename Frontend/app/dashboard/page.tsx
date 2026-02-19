'use client';

export default function Dashboard() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to Dyslexia EmpowerHub
        </h1>
        <p className="text-xl text-gray-700 mb-8">
          Your personalized learning companion for dyslexia support
        </p>
        <div className="space-y-4">
          <p className="text-lg text-gray-600">
            Get started by exploring our features and resources
          </p>
        </div>
      </div>
    </main>
  );
}
