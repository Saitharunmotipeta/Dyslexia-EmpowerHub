import Link from "next/link";
import { ROUTES } from "@/constants/routes";

export default function LandingPage() {
  return (
    <main style={{ padding: "40px" }}>
      <h1>AI Learning Platform</h1>
      <p>Pronunciation training powered by AI.</p>

      <div style={{ marginTop: "20px" }}>
        <Link href={ROUTES.LOGIN}>Login</Link>
        <br />
        <Link href={ROUTES.REGISTER}>Sign Up</Link>
      </div>
    </main>
  );
}
