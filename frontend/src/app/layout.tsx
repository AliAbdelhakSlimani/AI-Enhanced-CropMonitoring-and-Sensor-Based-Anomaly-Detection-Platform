// src/app/layout.tsx – AJOUTE LE PROVIDER
import "./globals.css";
import Providers from "./providers";  // ← NOUVEL IMPORT
import Link from "next/link";
import { ReactNode } from "react";

export const metadata = {
  title: "Crop Anomaly Platform",
  description: "Monitoring agricole intelligent",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  const isLoggedIn = typeof window !== "undefined" && !!localStorage.getItem("access_token");

  return (
    <html lang="fr">
      <body className="min-h-screen bg-gray-50">
        <Providers>  {/* ← ENVELOPPE TOUTE L'APP ICI */}
          {isLoggedIn ? (
            <div className="flex">
              {/* Sidebar */}
              <div className="w-64 bg-blue-900 text-white min-h-screen p-6">
                <h1 className="text-2xl font-bold mb-10">CropGuard</h1>
                <nav className="space-y-4">
                  <Link href="/dashboard" className="block py-3 px-4 rounded hover:bg-blue-800 transition">
                    Tableau de bord
                  </Link>
                  <Link href="/plots" className="block py-3 px-4 rounded hover:bg-blue-800 transition">
                    Parcelles
                  </Link>
                  <Link href="/alerts" className="block py-3 px-4 rounded hover:bg-blue-800 transition">
                    Alertes
                  </Link>
                  <button
                    onClick={() => {
                      localStorage.clear();
                      window.location.href = "/login";
                    }}
                    className="w-full text-left py-3 px-4 rounded hover:bg-red-800 transition mt-10"
                  >
                    Déconnexion
                  </button>
                </nav>
              </div>

              <div className="flex-1 p-8">{children}</div>
            </div>
          ) : (
            children
          )}
        </Providers>
      </body>
    </html>
  );
}