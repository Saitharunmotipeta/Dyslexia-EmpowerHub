import { Suspense } from "react";
import MockResultClient from "./mockresultclient";

export const dynamic = "force-dynamic";

export default function MockPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <MockResultClient />
    </Suspense>
  );
}