// src/app/dashboard/page.tsx – VERSION FINALE AVEC BOUTON DÉCONNEXION
"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import Link from "next/link";
import { useRouter } from "next/navigation";  // ← AJOUT POUR LA REDIRECTION

export default function Dashboard() {
  const router = useRouter();  // ← Pour rediriger après déconnexion

  // Récupère les parcelles (FieldPlot)
  const { data: plots = [], isLoading: loadingPlots } = useQuery({
    queryKey: ["plots"],
    queryFn: () => api.get("/fieldplot/").then((res) => res.data),
  });

  // Récupère les anomalies pour le statut couleur
  const { data: anomalies = [] } = useQuery({
    queryKey: ["anomalies"],
    queryFn: () => api.get("/anomalies/").then((res) => res.data),
  });

  // Calcul du statut (vert/jaune/rouge)
  const getStatus = (plotId: number) => {
    const plotAnomalies = anomalies.filter((a: any) => a.plot === plotId);
    if (plotAnomalies.length === 0) {
      return { bg: "bg-green-100", border: "border-green-500", text: "text-green-800", icon: "🟢", label: "Tout va bien" };
    }
    if (plotAnomalies.some((a: any) => a.severity === "high")) {
      return { bg: "bg-red-100", border: "border-red-500", text: "text-red-800", icon: "🔴", label: "Urgent" };
    }
    return { bg: "bg-yellow-100", border: "border-yellow-500", text: "text-yellow-800", icon: "🟡", label: "Attention" };
  };

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");  // ← Redirection immédiate vers login
  };

  if (loadingPlots) {
    return <div className="p-8 text-center text-xl">Chargement des parcelles...</div>;
  }

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">Tableau de bord</h1>
        <div className="flex gap-4">
          <Link href="/alerts">
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition text-lg font-medium">
              Voir les alertes
            </button>
          </Link>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition text-lg font-medium"
          >
            Déconnexion
          </button>
        </div>
      </div>

      {plots.length === 0 ? (
        <div className="text-center text-gray-600 text-xl mt-20">
          <p>Aucune parcelle enregistrée.</p>
          <p className="mt-4">Créez-en dans l'admin Django → <a href="http://127.0.0.1:8000/admin/" target="_blank" className="text-blue-600 underline">Admin</a></p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {plots.map((plot: any) => {
            const status = getStatus(plot.id);

            return (
              <Link href={`/plot/${plot.id}`} key={plot.id}>
                <div className={`border-4 ${status.border} ${status.bg} ${status.text} p-8 rounded-2xl shadow-xl hover:shadow-2xl transition transform hover:scale-105 cursor-pointer`}>
                  <h2 className="text-2xl font-bold mb-6">{plot.name}</h2>
                  <div className="text-center mb-6">
                    <p className="text-6xl">{status.icon}</p>
                    <p className="text-xl font-semibold mt-4">{status.label}</p>
                  </div>
                  <div className="text-lg space-y-2">
                    <p><span className="font-medium">Ferme :</span> {plot.farm_name}</p>
                    <p><span className="font-medium">Surface :</span> {plot.area_hectares} ha</p>
                    <p><span className="font-medium">Variété :</span> {plot.crop_variety}</p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}