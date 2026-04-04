/**
 * Browser-visible API base (Next.js inlines NEXT_PUBLIC_* at build time).
 * Restart `npm run dev` after changing Frontend .env.local.
 */
export function getPublicApiBaseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  const base = raw && raw.length > 0 ? raw : "http://localhost:8000";
  return base.replace(/\/+$/, "");
}
