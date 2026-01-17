export default function HowToRead() {
  return (
    <div className="p-12 bg-gray-100">
      <h2 className="text-4xl font-bold text-gray-800 mb-10 text-center">How to Read the Chart</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 border-b-2 border-blue-500 pb-2">
            Chart Layout
          </h3>
          <ul className="space-y-3 text-gray-700">
            <li><strong>Diagonal (AA to 22):</strong> Pocket pairs</li>
            <li><strong>Upper Right Triangle:</strong> Suited hands (AKs, KQs, 87s, etc.)</li>
            <li><strong>Lower Left Triangle:</strong> Offsuit hands (AKo, KQo, 87o, etc.)</li>
            <li><strong>AA is Top-Left, 22 is Bottom-Right</strong></li>
          </ul>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 border-b-2 border-blue-500 pb-2">
            Hand Notation
          </h3>
          <ul className="space-y-3 text-gray-700">
            <li><strong>s</strong> = suited (same suit)</li>
            <li><strong>o</strong> = offsuit (different suits)</li>
            <li><strong>No suffix</strong> = pocket pair</li>
            <li><strong>Example:</strong> AKs = Ace-King suited</li>
          </ul>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md md:col-span-2">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 border-b-2 border-blue-500 pb-2">
            How to Use This Data
          </h3>
          <ol className="space-y-3 text-gray-700 list-decimal list-inside">
            <li>Select your table size using the buttons above the heatmap</li>
            <li>Find your starting hand on the chart</li>
            <li>Check the equity percentage - this is your expected win rate if all players go to showdown</li>
            <li>Watch how hand equities change with more opponents</li>
            <li>Notice premium pairs drop dramatically, while suited cards hold up better</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
