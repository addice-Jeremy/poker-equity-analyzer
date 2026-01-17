import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Poker Equity Calculator",
  description: "Interactive poker equity calculator with Monte Carlo simulation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
