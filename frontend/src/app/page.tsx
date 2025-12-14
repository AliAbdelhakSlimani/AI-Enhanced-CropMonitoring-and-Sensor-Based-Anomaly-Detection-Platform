// src/app/page.tsx  ← PAGE RACINE (remplace tout)
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      router.push("/dashboard");  // connecté → dashboard
    } else {
      router.push("/login");      // pas connecté → login
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <p className="text-xl">Redirection en cours...</p>
    </div>
  );
}