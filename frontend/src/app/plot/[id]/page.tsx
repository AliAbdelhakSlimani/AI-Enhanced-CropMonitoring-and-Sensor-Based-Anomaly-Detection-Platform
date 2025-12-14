// src/app/plot/[id]/page.tsx – VERSION FINALE AVEC BOUTONS RETOUR ET DÉCONNEXION
"use client";

import { useParams, useRouter } from "next/navigation";  // ← useRouter ajouté
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import Link from "next/link";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function PlotDetail() {
  const { id } = useParams();
  const router = useRouter();  // ← Pour la déconnexion

  const { data: readings = [], isLoading } = useQuery({
    queryKey: ["readings", id],
    queryFn: () =>
      api.get(`/readings/?plot=${id}`).then((res) => res.data),
  });

  const { data: plot = {} } = useQuery({
    queryKey: ["plot", id],
    queryFn: () => api.get(`/fieldplot/${id}/`).then((res) => res.data),
  });

  // Formatage des données pour Recharts
  const chartData = readings.reduce((acc: any, reading: any) => {
    const existing = acc.find((item: any) => item.timestamp === reading.timestamp);
    if (existing) {
      existing[reading.sensor_type] = parseFloat(reading.value);
    } else {
      acc.push({
        timestamp: new Date(reading.timestamp).getTime(),
        readableTime: new Date(reading.timestamp).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" }),
        [reading.sensor_type]: parseFloat(reading.value),
      });
    }
    return acc;
  }, []);

  chartData.sort((a: any, b: any) => a.timestamp - b.timestamp);

  // Fonction de déconnexion
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");
  };

  if (isLoading) {
    return <div className="p-8 text-center text-xl">Chargement des données...</div>;
  }

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      <div className="flex justify-between items-center mb-6">
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

      <h1 className="text-4xl font-bold mb-6 text-gray-800">
        Parcelle : {plot.name || `ID ${id}`}
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Ferme</p>
          <p className="text-2xl font-bold">{plot.farm_name || "-"}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Surface</p>
          <p className="text-2xl font-bold">{plot.area_hectares || "-"} ha</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Variété</p>
          <p className="text-2xl font-bold">{plot.crop_variety || "-"}</p>
        </div>
      </div>

      <div className="bg-white p-8 rounded-xl shadow-xl">
        <h2 className="text-2xl font-bold mb-6 text-center">Évolution des capteurs (dernières 48h)</h2>
        <ResponsiveContainer width="100%" height={500}>
          <LineChart data={chartData} margin={{ top: 20, right: 40, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="readableTime" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip 
              isAnimationActive={false}
              cursor={{ stroke: '#999', strokeDasharray: '5 5' }}
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px', padding: '10px' }}
              labelStyle={{ fontWeight: 'bold', color: '#333' }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="air_humidity"
              stroke="#3b82f6"
              name="Humidité air (%)"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2 }}
              connectNulls={true}
            />
            <Line
              type="monotone"
              dataKey="soil_moisture"
              stroke="#10b981"
              name="Humidité sol (%)"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2 }}
              connectNulls={true}
            />
            <Line
              type="monotone"
              dataKey="air_temperature"
              stroke="#ef4444"
              name="Température (°C)"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2 }}
              connectNulls={true}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}