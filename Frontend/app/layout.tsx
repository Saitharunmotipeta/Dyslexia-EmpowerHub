import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import { Nav } from "@/components/layout/Nav";
import { DyslexiaModeToggle } from "@/components/DyslexiaModeToggle";
import { assetUrl } from "@/constants/assets";

export const metadata: Metadata = {
  title: "Dyslexia EmpowerHub",
  description: "Dyslexia-friendly learning platform",
  icons: {
    icon: assetUrl("favicon.ico"),
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{if(localStorage.getItem('dyslexiaMode')==='true')document.body.classList.add('dyslexia-mode');}catch(e){}})();`,
          }}
        />
        <AuthProvider>
          <div className="flex min-h-screen flex-col">
            <Nav />
            <main className="flex-1">{children}</main>
          </div>
          <DyslexiaModeToggle />
        </AuthProvider>
      </body>
    </html>
  );
}
