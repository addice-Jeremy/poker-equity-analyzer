"use client";

import { useState, useEffect } from "react";
import EquityHeatmap from "@/components/EquityHeatmap";
import KeyInsights from "@/components/KeyInsights";
import EquityTrends from "@/components/EquityTrends";
import HowToRead from "@/components/HowToRead";
import StrategyGuide from "@/components/StrategyGuide";
import PokerOdds from "@/components/PokerOdds";

export default function Home() {
  const [equityData, setEquityData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load equity data from API
    fetch("/api/equity")
      .then((res) => res.json())
      .then((data) => {
        setEquityData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load equity data:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="text-white text-2xl">Loading equity data...</div>
      </div>
    );
  }

  if (!equityData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="text-white text-2xl">Failed to load equity data</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-800 to-blue-600 rounded-t-2xl p-12 text-center text-white">
          <h1 className="text-5xl font-bold mb-4">Poker Starting Hand Equity Analysis</h1>
          <p className="text-xl opacity-90">
            Master pre-flop strategy with data-driven insights from 84+ million simulated hands
          </p>
        </div>

        {/* Main Content Container */}
        <div className="bg-white rounded-b-2xl shadow-2xl overflow-hidden">
          {/* Heatmap Section */}
          <div className="p-8 bg-gray-50">
            <EquityHeatmap data={equityData} />
          </div>

          {/* How to Read */}
          <HowToRead />

          {/* Key Insights with Carousel */}
          <KeyInsights data={equityData} />

          {/* Equity Trends */}
          <EquityTrends data={equityData} />

          {/* Strategy Guide */}
          <StrategyGuide />

          {/* Poker Odds */}
          <PokerOdds />

          {/* About Section */}
          <div className="p-8 bg-gray-50 text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">About This Data</h2>
            <p className="text-gray-600 max-w-3xl mx-auto">
              Based on Monte Carlo simulation with{" "}
              <strong>{equityData.metadata.num_simulations.toLocaleString()} simulations</strong> per
              hand per table size. All 169 starting hands simulated across 2-6 player tables with
              ±0.3% accuracy (95% confidence).
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
