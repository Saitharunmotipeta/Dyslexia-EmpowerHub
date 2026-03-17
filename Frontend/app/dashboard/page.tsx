"use client";

import { useRouter } from "next/navigation";
import { BookOpen, Zap, MessageCircle } from "lucide-react";
import { Icon } from "@/components/ui/Icon";

export default function Dashboard() {
  const router = useRouter();

  const modules = [
    {
      id: "learning",
      title: "Learning Levels",
      description: "Master reading and pronunciation with interactive lessons tailored to your pace. Build confidence step by step.",
      iconName: "BookOpen" as const,
      color: "from-blue-500 to-blue-600",
      lightColor: "bg-blue-50",
      buttonColor: "bg-blue-600 hover:bg-blue-700",
      action: () => router.push("/learning"),
    },
    {
      id: "dynamic",
      title: "Dynamic Module",
      description: "Practice spelling and pronunciation with dynamic, real-time feedback. Learn at your own rhythm with personalized challenges.",
      iconName: "Zap" as const,
      color: "from-amber-500 to-orange-600",
      lightColor: "bg-amber-50",
      buttonColor: "bg-amber-600 hover:bg-amber-700",
      action: () => router.push("/dynamic"),
    },
    {
      id: "chatbot",
      title: "Smart Assistant",
      description: "Chat with our AI assistant for instant support, tips, and guidance. Ask questions anytime you need help.",
      iconName: "MessageCircle" as const,
      color: "from-purple-500 to-purple-600",
      lightColor: "bg-purple-50",
      buttonColor: "bg-purple-600 hover:bg-purple-700",
      action: () => router.push("/chatbot"),
    },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50 p-6 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-12 md:mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 leading-tight">
            Welcome to Dyslexia EmpowerHub
          </h1>
          <p className="text-lg md:text-xl text-gray-700 max-w-2xl mx-auto leading-relaxed">
            Your personalized learning companion for dyslexia support. Choose a module below to get started.
          </p>
        </div>

        {/* Modules Grid */}
        <div className="grid md:grid-cols-3 gap-6 md:gap-8">
          {modules.map((module) => (
            <div
              key={module.id}
              className={`${module.lightColor} rounded-2xl p-8 shadow-soft-lg hover:shadow-soft-lg transition-all duration-300 hover:scale-105 flex flex-col`}
            >
              {/* Icon Section */}
              <div className={`bg-gradient-to-br ${module.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6`}>
                <Icon name={module.iconName} size="lg" className="text-white" />
              </div>

              {/* Content Section */}
              <div className="flex-grow">
                <h2 className="text-2xl font-bold text-gray-900 mb-3">
                  {module.title}
                </h2>
                <p className="text-gray-700 leading-relaxed text-base mb-6">
                  {module.description}
                </p>
              </div>

              {/* Button Section */}
              <button
                onClick={module.action}
                className={`${module.buttonColor} text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 focus:outline-2 focus:outline-offset-2 w-full`}
              >
                Get Started
              </button>
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="mt-16 text-center">
          <p className="text-gray-600 text-sm md:text-base">
            Each module is designed with dyslexia in mind. 
            Take your time and go at your own pace.
          </p>
        </div>
      </div>
    </main>
  );
}
