/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
  webpack: (config, { isServer }) => {
    // Exclude the old dashboard directory from the build
    config.watchOptions = {
      ignored: ['**/dashboard/**', '**/.next/**', '**/node_modules/**'],
    };
    return config;
  },
}

module.exports = nextConfig
