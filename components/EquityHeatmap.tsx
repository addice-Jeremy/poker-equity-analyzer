"use client";

import { useState } from "react";

interface EquityHeatmapProps {
  data: any;
}

export default function EquityHeatmap({ data }: EquityHeatmapProps) {
  const [playerCount, setPlayerCount] = useState(6);

  const ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"];

  const getHandName = (row: number, col: number): string => {
    if (row === col) {
      return `${ranks[row]}${ranks[col]}`;
    } else if (row < col) {
      return `${ranks[row]}${ranks[col]}s`;
    } else {
      return `${ranks[col]}${ranks[row]}o`;
    }
  };

  const getEquity = (hand: string): number => {
    const handData = data.hands[hand];
    if (!handData) return 0;
    const playerData = handData[`players_${playerCount}`];
    return playerData ? playerData.equity * 100 : 0;
  };

  const getColor = (equity: number): string => {
    // Dynamic thresholds based on player count
    let premiumThreshold: number;
    let strongThreshold: number;
    let playableThreshold: number;

    if (playerCount === 2) {
      premiumThreshold = 50;
      strongThreshold = 40;
      playableThreshold = 30;
    } else if (playerCount === 3) {
      premiumThreshold = 40;
      strongThreshold = 30;
      playableThreshold = 22;
    } else if (playerCount === 4) {
      premiumThreshold = 35;
      strongThreshold = 27;
      playableThreshold = 20;
    } else if (playerCount === 5) {
      premiumThreshold = 30;
      strongThreshold = 23;
      playableThreshold = 17;
    } else {
      // 6-max
      premiumThreshold = 27;
      strongThreshold = 20;
      playableThreshold = 15;
    }

    // Apply gradient within each category
    if (equity >= premiumThreshold + 10) return "bg-emerald-600";
    if (equity >= premiumThreshold + 5) return "bg-emerald-500";
    if (equity >= premiumThreshold) return "bg-green-500";
    if (equity >= strongThreshold + 5) return "bg-green-400";
    if (equity >= strongThreshold) return "bg-lime-400";
    if (equity >= playableThreshold + 5) return "bg-yellow-400";
    if (equity >= playableThreshold) return "bg-yellow-500";
    if (equity >= playableThreshold - 5) return "bg-orange-400";
    if (equity >= playableThreshold - 10) return "bg-orange-500";
    if (equity >= playableThreshold - 15) return "bg-red-400";
    return "bg-red-500";
  };

  const getTextColor = (equity: number): string => {
    return equity >= 15 ? "text-white" : "text-gray-800";
  };

  // Dynamic legend thresholds based on player count
  const getLegendCategories = () => {
    if (playerCount === 2) {
      return [
        { color: "bg-green-500", label: "Premium (50%+)" },
        { color: "bg-yellow-400", label: "Strong (40-50%)" },
        { color: "bg-orange-400", label: "Playable (30-40%)" },
        { color: "bg-red-400", label: "Weak (<30%)" },
      ];
    } else if (playerCount === 3) {
      return [
        { color: "bg-green-500", label: "Premium (40%+)" },
        { color: "bg-yellow-400", label: "Strong (30-40%)" },
        { color: "bg-orange-400", label: "Playable (22-30%)" },
        { color: "bg-red-400", label: "Weak (<22%)" },
      ];
    } else if (playerCount === 4) {
      return [
        { color: "bg-green-500", label: "Premium (35%+)" },
        { color: "bg-yellow-400", label: "Strong (27-35%)" },
        { color: "bg-orange-400", label: "Playable (20-27%)" },
        { color: "bg-red-400", label: "Weak (<20%)" },
      ];
    } else if (playerCount === 5) {
      return [
        { color: "bg-green-500", label: "Premium (30%+)" },
        { color: "bg-yellow-400", label: "Strong (23-30%)" },
        { color: "bg-orange-400", label: "Playable (17-23%)" },
        { color: "bg-red-400", label: "Weak (<17%)" },
      ];
    } else {
      // 6-max
      return [
        { color: "bg-green-500", label: "Premium (27%+)" },
        { color: "bg-yellow-400", label: "Strong (20-27%)" },
        { color: "bg-orange-400", label: "Playable (15-20%)" },
        { color: "bg-red-400", label: "Weak (<15%)" },
      ];
    }
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Interactive Equity Heatmap</h2>
        <p className="text-gray-600 mb-4">Select table size to see how equity changes</p>

        {/* Player count selector */}
        <div className="flex justify-center gap-2 flex-wrap">
          {[2, 3, 4, 5, 6].map((count) => (
            <button
              key={count}
              onClick={() => setPlayerCount(count)}
              className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                playerCount === count
                  ? "bg-blue-600 text-white shadow-lg"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              {count === 2 ? "Heads-Up" : count === 6 ? "6-Max" : `${count}-Handed`}
            </button>
          ))}
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="bg-white rounded-xl p-4 shadow-lg overflow-x-auto">
        <table className="w-full border-collapse">
          <tbody>
            {ranks.map((rowRank, rowIdx) => (
              <tr key={rowRank}>
                {ranks.map((colRank, colIdx) => {
                  const hand = getHandName(rowIdx, colIdx);
                  const equity = getEquity(hand);
                  return (
                    <td
                      key={colRank}
                      className={`border border-gray-300 p-2 text-center ${getColor(
                        equity
                      )} ${getTextColor(equity)}`}
                      title={`${hand}: ${equity.toFixed(1)}% equity`}
                    >
                      <div className="font-bold text-sm">{hand}</div>
                      <div className="text-xs">{equity.toFixed(1)}%</div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="mt-4 flex justify-center gap-4 flex-wrap">
        {getLegendCategories().map((category, idx) => (
          <div key={idx} className="flex items-center gap-2">
            <div className={`w-4 h-4 ${category.color} rounded`}></div>
            <span className="text-sm text-gray-700">{category.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
