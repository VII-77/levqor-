/** @type {import("next").NextConfig} */
const nextConfig = {
  redirects: async () => ([
    { source: "/home", destination: "/", permanent: true },
    { source: "/status", destination: "/insights", permanent: false },
  ]),
};
export default nextConfig;
