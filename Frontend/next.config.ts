import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Force rebuild of styles on dev */
  reactStrictMode: true,
  swcMinify: true,
  poweredByHeader: false,
};

export default nextConfig;
