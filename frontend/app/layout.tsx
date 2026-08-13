import type { Metadata } from "next";
import SplashScreen from "../components/SplashScreen";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mean Media AI",
  description: "SEO + GEO Intelligence for modern websites.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <SplashScreen />
        {children}
      </body>
    </html>
  );
}