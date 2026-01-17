"use client";

import { useState } from "react";

interface KeyInsightsProps {
  data: any;
}

export default function KeyInsights({ data }: KeyInsightsProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Calculate all insights
  const aaData = data.hands["AA"];
  const aa_hu = aaData["players_2"].equity * 100;
  const aa_6max = aaData["players_6"].equity * 100;
  const aa_drop = aa_hu - aa_6max;

  const aksData = data.hands["AKs"]["players_6"];
  const akoData = data.hands["AKo"]["players_6"];
  const aks_equity = aksData.equity * 100;
  const ako_equity = akoData.equity * 100;
  const suited_bonus = aks_equity - ako_equity;

  const kkData = data.hands["KK"];
  const kk_hu = kkData["players_2"].equity * 100;
  const kk_6max = kkData["players_6"].equity * 100;

  const jjData = data.hands["JJ"]["players_6"];
  const ttData = data.hands["TT"]["players_6"];
  const jj_equity = jjData.equity * 100;
  const tt_equity = ttData.equity * 100;

  const aksData_hu = data.hands["AKs"]["players_2"];
  const aksData_6max = data.hands["AKs"]["players_6"];
  const aks_hu_equity = aksData_hu.equity * 100;
  const aks_6max_equity = aksData_6max.equity * 100;

  const a2sData = data.hands["A2s"]["players_6"];
  const a2oData = data.hands["A2o"]["players_6"];
  const a2s_equity = a2sData.equity * 100;
  const a2o_equity = a2oData.equity * 100;

  const _22Data_hu = data.hands["22"]["players_2"];
  const _22Data_6max = data.hands["22"]["players_6"];
  const _22_hu = _22Data_hu.equity * 100;
  const _22_6max = _22Data_6max.equity * 100;

  const qqData = data.hands["QQ"]["players_6"];
  const qq_equity = qqData.equity * 100;

  const ajo_Data = data.hands["AJo"]["players_6"];
  const kqsData = data.hands["KQs"]["players_6"];
  const ajo_equity = ajo_Data.equity * 100;
  const kqs_equity = kqsData.equity * 100;

  const _77Data = data.hands["77"]["players_6"];
  const akData = data.hands["AKo"]["players_6"];
  const _77_equity = _77Data.equity * 100;
  const ak_equity = akData.equity * 100;

  const jtsData = data.hands["JTs"]["players_6"];
  const aqoData = data.hands["AQo"]["players_6"];
  const jts_equity = jtsData.equity * 100;
  const aqo_equity = aqoData.equity * 100;

  const insights = [
    {
      title: "Premium Pairs Lose Value Multi-Way",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{aa_hu.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">Heads-up</div>
          </div>
          <div className="text-2xl text-gray-400">→</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-500">{aa_6max.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">6-max</div>
          </div>
        </div>
      ),
      text: `AA equity drops ${aa_drop.toFixed(1)}% with more opponents`,
      strategy: "Raise pre-flop to thin the field",
    },
    {
      title: "Suited Cards Add Value",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{aks_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">AKs</div>
          </div>
          <div className="text-xl text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{ako_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">AKo</div>
          </div>
        </div>
      ),
      text: `Suited gives +${suited_bonus.toFixed(1)}% equity at 6-max`,
      strategy: "Suited matters, but high card ranks matter more",
    },
    {
      title: "Position is Power",
      visual: (
        <div className="text-center my-6">
          <div className="text-5xl font-bold text-blue-600">~5%</div>
        </div>
      ),
      text: "Equity advantage from late position",
      strategy: "Play 40% from button, 15% from early",
    },
    {
      title: "Small Pairs Need Deep Stacks",
      visual: (
        <div className="text-center my-6">
          <div className="text-5xl font-bold text-purple-600">15:1</div>
        </div>
      ),
      text: "Minimum implied odds to profitably set mine",
      strategy: "Fold 22-66 to raises without deep stacks",
    },
    {
      title: "KK Still Dominates Most Hands",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{kk_6max.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">6-max</div>
          </div>
          <div className="text-2xl text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{kk_hu.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">Heads-up</div>
          </div>
        </div>
      ),
      text: `KK has ${kk_6max.toFixed(1)}% equity even at 6-max`,
      strategy: "Kings are still premium - play them aggressively",
    },
    {
      title: "AK Suffers More Than Pairs",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{aks_hu_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">Heads-up</div>
          </div>
          <div className="text-2xl text-gray-400">→</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{aks_6max_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">6-max</div>
          </div>
        </div>
      ),
      text: `AKs drops ${(aks_hu_equity - aks_6max_equity).toFixed(1)}% from HU to 6-max`,
      strategy: "Unpaired hands lose value faster than pocket pairs",
    },
    {
      title: "Mid Pairs Competitive with Big Cards",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-lime-600">{_77_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">77</div>
          </div>
          <div className="text-xl text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{ak_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">AKo</div>
          </div>
        </div>
      ),
      text: `77 has ${_77_equity.toFixed(1)}% equity vs AKo's ${ak_equity.toFixed(1)}% at 6-max`,
      strategy: "Pocket pairs hold value better than unpaired hands multiway",
    },
    {
      title: "Suited Connectors vs Offsuit Broadway",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{jts_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">JTs</div>
          </div>
          <div className="text-xl text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{aqo_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">AQo</div>
          </div>
        </div>
      ),
      text: "JTs and AQo have nearly identical equity at 6-max",
      strategy: "Connected cards have more playability than high cards",
    },
    {
      title: "Drawing Hands Improve Multiway",
      visual: (
        <div className="flex items-center justify-center gap-4 my-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{jts_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">JTs 6-max</div>
          </div>
          <div className="text-xl text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-500">{aqo_equity.toFixed(1)}%</div>
            <div className="text-sm text-gray-500">AQo 6-max</div>
          </div>
        </div>
      ),
      text: "Suited connectors compete with offsuit broadway multiway",
      strategy: "Drawing hands have better implied odds with more players",
    },
  ];

  const nextInsight = () => {
    setCurrentIndex((prev) => (prev + 1) % insights.length);
  };

  const prevInsight = () => {
    setCurrentIndex((prev) => (prev - 1 + insights.length) % insights.length);
  };

  const currentInsight = insights[currentIndex];

  return (
    <div className="p-12 bg-white">
      <h2 className="text-4xl font-bold text-gray-800 mb-10 text-center">Key Insights</h2>

      <div className="max-w-4xl mx-auto relative">
        {/* Carousel */}
        <div className="flex items-center gap-4">
          {/* Left Arrow */}
          <button
            onClick={prevInsight}
            className="flex-shrink-0 w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
            aria-label="Previous insight"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>

          {/* Insight Card */}
          <div className="flex-1 border-2 border-gray-200 rounded-xl p-8 min-h-[280px]">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
              {currentInsight.title}
            </h3>
            {currentInsight.visual}
            <p className="text-base text-gray-600 text-center mb-3">
              {currentInsight.text}
            </p>
            <p className="text-base text-blue-600 font-semibold text-center">
              {currentInsight.strategy}
            </p>
          </div>

          {/* Right Arrow */}
          <button
            onClick={nextInsight}
            className="flex-shrink-0 w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors"
            aria-label="Next insight"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* Dots Indicator */}
        <div className="flex justify-center gap-2 mt-6">
          {insights.map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentIndex(idx)}
              className={`w-2 h-2 rounded-full transition-all ${
                idx === currentIndex ? "bg-blue-600 w-8" : "bg-gray-300"
              }`}
              aria-label={`Go to insight ${idx + 1}`}
            />
          ))}
        </div>

        {/* Counter */}
        <p className="text-center text-gray-500 text-sm mt-4">
          {currentIndex + 1} / {insights.length}
        </p>
      </div>
    </div>
  );
}
