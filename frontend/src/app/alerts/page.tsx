// src/app/alerts/page.tsx – VERSION FINALE AVEC BOUTONS RETOUR ET DÉCONNEXION
"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import Link from "next/link";
import { useRouter } from "next/navigation";  // ← Pour la déconnexion

export default function AlertsPage() {
  const router = useRouter();  // ← Pour rediriger après déconnexion

  const { data: recommendations = [], isLoading } = useQuery({
    queryKey: ["recommendations"],
    queryFn: () => api.get("/recommandations/").then((res) => res.data),
    refetchInterval: 15000, // rafraîchit toutes les 15 secondes
  });

  // Couleur selon la confiance
  const getPriorityColor = (confidence: string) => {
    if (confidence === "high") return "border-red-500 bg-red-50";
    if (confidence === "medium") return "border-yellow-500 bg-yellow-50";
    return "border-gray-400 bg-gray-50";
  };

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");
  };

  if (isLoading) {
    return <div className="p-8 text-center text-xl">Chargement des alertes...</div>;
  }

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      <div className="flex justify-between items-center mb-8">
        <div className="flex gap-4">
          <Link href="/dashboard">
            <button className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition text-lg font-medium">
              ← Retour au dashboard
            </button>
          </Link>
        </div>

        <button
          onClick={handleLogout}
          className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition text-lg font-medium"
        >
          Déconnexion
        </button>
      </div>

      <h1 className="text-4xl font-bold mb-8 text-gray-800">Alertes & Recommandations</h1>

      {recommendations.length === 0 ? (
        <div className="text-center text-gray-600 text-xl mt-20 bg-white p-12 rounded-xl shadow">
          <p className="text-6xl mb-4">✅</p>
          <p>Aucune alerte active pour le moment.</p>
          <p className="mt-4">Tout va bien dans vos parcelles !</p>
        </div>
      ) : (
        <div className="space-y-8">
          {recommendations.map((rec: any) => (
            <div
              key={rec.id}
              className={`border-4 rounded-2xl p-8 shadow-xl ${getPriorityColor(rec.confidence)}`}
            >
              <div className="flex justify-between items-start mb-6">
                <h2 className="text-3xl font-bold text-gray-800">{rec.title}</h2>
                <div className="text-right">
                  <span className="block text-sm text-gray-600">Confiance</span>
                  <span className="text-2xl font-bold" style={{ color: "black" }}>
                    {rec.confidence === "high" ? "🔴 Élevée" : rec.confidence === "medium" ? "🟠 Moyenne" : "⚪ Faible"}
                  </span>
                </div>
              </div>

              <div className="mb-6">
                <p className="text-lg text-gray-700 leading-relaxed">{rec.explanation_text}</p>
              </div>

              <div className="bg-blue-50 p-6 rounded-xl border-2 border-blue-200">
                <p className="font-bold text-blue-900 text-xl mb-2">Recommandation de l'agent :</p>
                <p className="text-blue-800 text-lg leading-relaxed">{rec.recommended_action}</p>
              </div>

              <p className="text-sm text-gray-500 mt-6 text-right">
                Détectée le {new Date(rec.timestamp).toLocaleString("fr-FR")}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}