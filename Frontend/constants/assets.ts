/**
 * Base URL for static image assets (external).
 */

export const ASSETS_BASE_URL =
  "https://raw.githubusercontent.com/Saitharunmotipeta/dyslexia-static-assets/main/images/words";

export function assetUrl(filename: string): string {
  return `${ASSETS_BASE_URL}/${filename}`;
}
