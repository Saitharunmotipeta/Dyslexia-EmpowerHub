"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createUserAccount } from "@/features/auth/service";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import styles from "./register.module.css";

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
      router.push("/auth/login");
    } catch {
      alert("Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <h1 className={styles.title}>Create Account</h1>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputGroup}>
          <label htmlFor="username" className={styles.label}>Username</label>
          <Input
            id="username"
            placeholder="Enter your username"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className={styles.inputGroup}>
          <label htmlFor="email" className={styles.label}>Email</label>
          <Input
            id="email"
            type="email"
            placeholder="Enter your email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className={styles.inputGroup}>
          <label htmlFor="password" className={styles.label}>Password</label>
          <Input
            id="password"
            type="password"
            placeholder="Enter your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <Button type="submit" loading={loading} className={styles.button}>
          Sign Up
        </Button>
      </form>
    </main>
  );
}
