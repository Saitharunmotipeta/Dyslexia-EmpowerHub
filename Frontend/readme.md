# Dyslexia EmpowerHub — Frontend

Next.js 14 (App Router) frontend for the Dyslexia EmpowerHub backend.

## Setup

1. Copy env example and set your backend URL:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local: NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
   ```

2. Install and run:
   ```bash
   npm install
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000).

## Structure

- **`app/`** — App Router pages; mirrors backend route groups: `auth`, `learning`, `practice`, `mock`, `dynamic`, `feedback`, `chatbot`.
- **`lib/api.ts`** — All API calls; uses `NEXT_PUBLIC_API_BASE_URL` and attaches JWT from `localStorage`.
- **`context/AuthContext.tsx`** — Token storage, login/register, profile.
- **`hooks/useDebounce.ts`** — 300ms debounce (e.g. pace slider).
- **`components/ui/`** — Reusable UI (Button, Card, Input, ProgressBar, PlaceholderMedia, DifficultyBadge).

## Backend

No backend files are modified. The frontend calls the existing FastAPI routes as documented in the backend analysis.
