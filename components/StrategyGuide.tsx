export default function StrategyGuide() {
  return (
    <div className="p-12 bg-white">
      <h2 className="text-4xl font-bold text-gray-800 mb-4 text-center">Practical Strategy Guide</h2>

      <p className="text-gray-600 text-center mb-10 max-w-3xl mx-auto">
        Your position at the table drastically affects which hands you can profitably play.
        Acting last gives you more information and control, allowing you to play weaker hands.
        Here's how to adjust your starting hand range based on position:
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold mb-2 border-b-2 border-white/30 pb-2">
            Early Position (Tight Range)
          </h3>
          <p className="text-sm opacity-90 mb-4 italic">Top ~15% of hands</p>
          <p className="mb-2"><strong>Raise:</strong> AA-TT, AKs, AKo, AQs</p>
          <p className="text-sm opacity-90">
            <strong>Why:</strong> You'll face multiple opponents and act first post-flop. Need strong hands that play well multi-way.
          </p>
        </div>

        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold mb-2 border-b-2 border-white/30 pb-2">
            Middle Position (Standard Range)
          </h3>
          <p className="text-sm opacity-90 mb-4 italic">Top ~25% of hands</p>
          <p className="mb-2"><strong>Raise:</strong> AA-77, AK-AJ, KQs, KJs, QJs</p>
          <p className="text-sm opacity-90">
            <strong>Why:</strong> Fewer players behind you. Can still face resistance but position advantage on some opponents.
          </p>
        </div>

        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold mb-2 border-b-2 border-white/30 pb-2">
            Button (Wide Range)
          </h3>
          <p className="text-sm opacity-90 mb-4 italic">Top ~40% of hands</p>
          <p className="mb-2"><strong>Raise:</strong> All pairs, suited aces, suited connectors, broadway cards</p>
          <p className="text-sm opacity-90">
            <strong>Why:</strong> Best position post-flop. Can play weaker hands profitably. Position compensates for lower equity.
          </p>
        </div>

        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold mb-2 border-b-2 border-white/30 pb-2">
            Big Blind Defense
          </h3>
          <p className="text-sm opacity-90 mb-4 italic">~30-40% vs button raise</p>
          <p className="mb-2"><strong>Call:</strong> Hands with &gt;30% equity vs button's range + good playability</p>
          <p className="text-sm opacity-90">
            <strong>Why:</strong> Already invested money (the blind). Need decent equity to defend, but don't need premium hands.
          </p>
        </div>
      </div>
    </div>
  );
}
