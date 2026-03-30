/** Turn API trend/pattern blobs into readable lines for the UI. */
export function summarizeInsightBlock(data: unknown): string {
  if (data == null) return "";
  if (typeof data === "string") return data;
  if (typeof data === "number" || typeof data === "boolean") return String(data);

  if (typeof data === "object") {
    const o = data as Record<string, unknown>;
    if (typeof o.summary === "string") return o.summary;
    if (typeof o.message === "string") return o.message;
    if (typeof o.headline === "string") return o.headline;
    if (typeof o.title === "string") return o.title;
    if (typeof o.explanation === "string") return o.explanation;

    const nested = o.pattern ?? o.trend;
    if (nested && typeof nested === "object") {
      const p = nested as Record<string, unknown>;
      if (typeof p.label === "string") return p.label;
      if (typeof p.description === "string") return p.description;
      if (typeof p.code === "string") return p.code.replace(/_/g, " ");
    }

    if (Array.isArray(o.feedback)) {
      return o.feedback.map(String).join(" · ");
    }
  }

  try {
    return JSON.stringify(data, null, 2);
  } catch {
    return String(data);
  }
}
