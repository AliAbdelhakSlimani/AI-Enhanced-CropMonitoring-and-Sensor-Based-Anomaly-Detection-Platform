// src/app/plots/page.tsx
"use client";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import Link from "next/link";

export default function PlotsPage() {
  const { data: plots = [] } = useQuery({
    queryKey: ["plots"],
    queryFn: () => api.get("/readings/").then(res => res.data),
  });

  const { data: anomalies = [] } = useQuery({
    queryKey: ["anomalies"],
    queryFn: () => api.get("/anomalies/").then(res => res.data),
  });

  const getStatus = (plotId: number) => {
    const recent = anomalies.filter((a: any) => a.plot === plotId);
    if (recent.length === 0) return { color: "bg-green-500", text: "Normal" };
    if (recent.some((a: any) => a.severity === "high")) return { color: "bg-red-500", text: "Urgent" };
    return { color: "bg-yellow-500", text: "Attention" };
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Mes Parcelles</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {plots.map((plot: any) => {
          const status = getStatus(plot.id);
          return (
            <Link href={`/plot/${plot.id}`} key={plot.id}>
              <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-xl font-semibold">{plot.name}</h2>
                  <span className={`px-3 py-1 rounded-full text-white text-sm ${status.color}`}>
                    {status.text}
                  </span>
                </div>
                <p className="text-gray-600">Ferme: {plot.farm.name}</p>
                <p className="text-gray-600">Surface: {plot.area_hectares} ha</p>
                <p className="text-sm text-gray-500 mt-4">Cliquez pour voir les données</p>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}