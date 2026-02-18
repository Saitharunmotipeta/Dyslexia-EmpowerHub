"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createUserAccount } from "@/features/auth/service";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createUserAccount({ username, email, password });
      router.push("/");
    } catch {
      alert("Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: "40px", maxWidth: "400px" }}>
      <h1>Create Account</h1>

      <form onSubmit={handleSubmit}>
        <Input
          placeholder="Username"
          required
          onChange={(e) => setUsername(e.target.value)}
        />

        <Input
          type="email"
          placeholder="Email"
          required
          onChange={(e) => setEmail(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Password"
          required
          onChange={(e) => setPassword(e.target.value)}
        />

        <Button type="submit" loading={loading}>
          Sign Up
        </Button>
      </form>
    </main>
  );
}
