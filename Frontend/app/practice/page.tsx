import { Suspense } from "react";
import PracticeClient from "./practiceclient";

export const dynamic = "force-dynamic";

export default function PracticePage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <PracticeClient />
    </Suspense>
  );
}