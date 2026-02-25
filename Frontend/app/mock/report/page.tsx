import { Suspense } from "react";
import MockReportClient from "./mockreportclient";

export const dynamic = "force-dynamic";

export default function MockPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <MockReportClient />
    </Suspense>
  );
}