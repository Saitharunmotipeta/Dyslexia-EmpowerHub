import { Suspense } from "react";
import MockStartClient from "./mockstartclient";

export const dynamic = "force-dynamic";

export default function MockPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <MockStartClient />
    </Suspense>
  );
}