import { Suspense } from "react";
import MockClient from "./mockclient";

export const dynamic = "force-dynamic";

export default function MockPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <MockClient />
    </Suspense>
  );
}