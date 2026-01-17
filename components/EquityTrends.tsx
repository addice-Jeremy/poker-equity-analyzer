"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface EquityTrendsProps {
  data: any;
}

export default function EquityTrends({ data }: EquityTrendsProps) {
  // Calculate category averages - sample hands shown
  // Category names for data (clean names for hover)
  const handCategories = {
    "Premium Pairs": ["AA", "KK", "QQ"],
    "High Cards": ["AKs", "AQs", "AJs", "KQs"],
    "Mid Pairs": ["JJ", "TT", "99", "88"],
    "Suited Connectors": ["JTs", "T9s", "98s", "87s"],
  };

  // Legend labels with example hands
  const legendLabels: Record<string, string> = {
    "Premium Pairs": "Premium Pairs (AA, KK, QQ)",
    "High Cards": "High Cards (AK, AQ, AJ, KQ)",
    "Mid Pairs": "Mid Pairs (JJ, TT, 99, 88)",
    "Suited Connectors": "Suited Connectors (JTs, T9s, 98s, 87s)",
  };

  const chartData = [2, 3, 4, 5, 6].map((players) => {
    const point: any = { players };

    Object.entries(handCategories).forEach(([category, hands]) => {
      let sum = 0;
      let count = 0;
      hands.forEach((hand) => {
        const handData = data.hands[hand];
        if (handData && handData[`players_${players}`]) {
          sum += handData[`players_${players}`].equity * 100;
          count++;
        }
      });
      point[category] = count > 0 ? (sum / count).toFixed(1) : 0;
    });

    return point;
  });

  // Calculate average equity for each category (using 6-max as reference for ordering)
  const categoryAverages = Object.entries(handCategories).map(([category, hands]) => {
    let sum = 0;
    let count = 0;
    hands.forEach((hand) => {
      const handData = data.hands[hand];
      if (handData && handData["players_6"]) {
        sum += handData["players_6"].equity * 100;
        count++;
      }
    });
    return {
      category,
      avgEquity: count > 0 ? sum / count : 0,
    };
  });

  // Sort categories by equity (highest to lowest) and assign colors
  const sortedCategories = categoryAverages
    .sort((a, b) => b.avgEquity - a.avgEquity)
    .map((item) => item.category);

  const colorMap: Record<string, string> = {
    [sortedCategories[0]]: "#10b981", // green for highest
    [sortedCategories[1]]: "#3b82f6", // blue
    [sortedCategories[2]]: "#f59e0b", // orange
    [sortedCategories[3]]: "#8b5cf6", // purple for lowest
  };

  return (
    <div className="p-12 bg-gray-50">
      <h2 className="text-4xl font-bold text-gray-800 mb-4 text-center">Equity Trends by Table Size</h2>
      <p className="text-gray-600 text-center mb-8 max-w-3xl mx-auto">
        How different hand categories scale as more players enter the pot
      </p>

      <div className="bg-white rounded-xl p-6 shadow-lg">
        <ResponsiveContainer width="100%" height={500}>
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 80 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="players"
              label={{ value: "Number of Players", position: "insideBottom", offset: -10 }}
            />
            <YAxis
              label={{ value: "Equity %", angle: -90, position: "insideLeft" }}
            />
            <Tooltip
              formatter={(value: any, name: any) => [`${value}%`, name]}
              itemSorter={(item: any) => {
                // Sort by the actual equity value in descending order
                return -parseFloat(item.value);
              }}
            />
            <Legend
              wrapperStyle={{ paddingTop: "20px" }}
              layout="vertical"
              verticalAlign="bottom"
              align="center"
              iconSize={12}
              content={(props) => {
                const { payload } = props;
                if (!payload) return null;

                // Sort payload by our sorted categories order
                const sortedPayload = sortedCategories
                  .map(cat => payload.find((p: any) => p.value === cat))
                  .filter(Boolean);

                return (
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", paddingTop: "20px", gap: "8px" }}>
                    {sortedPayload.map((entry: any, index: number) => (
                      <div key={`item-${index}`} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <svg width="12" height="12">
                          <line x1="0" y1="6" x2="12" y2="6" stroke={entry.color} strokeWidth="2" />
                        </svg>
                        <span style={{ fontSize: "14px", color: "#374151" }}>{legendLabels[entry.value]}</span>
                      </div>
                    ))}
                  </div>
                );
              }}
            />
            {sortedCategories.map((category) => (
              <Line
                key={category}
                type="monotone"
                dataKey={category}
                stroke={colorMap[category]}
                strokeWidth={2}
                dot={{ r: 4 }}
                legendType="line"
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
