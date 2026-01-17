export default function PokerOdds() {
  return (
    <div className="p-12 bg-gray-50">
      <h2 className="text-4xl font-bold text-gray-800 mb-4 text-center">How to Calculate Poker Odds</h2>
      <p className="text-gray-600 text-center mb-10 max-w-3xl mx-auto">
        Every action you make, hand you play, or bet you face has odds, probability, and statistics attached to it.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto mb-10">
        <div className="bg-white rounded-xl p-6 shadow-md border-t-4 border-blue-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Pot Odds</h3>
          <p className="text-sm text-gray-600 mb-4">
            <strong>What it is:</strong> The ratio of the current pot size to the cost of a contemplated call.
          </p>
          <div className="bg-gray-100 rounded-lg p-4 font-mono text-sm">
            <p><strong>Example:</strong></p>
            <p>Pot = $100, Bet = $50</p>
            <p>Call $50 to win $150</p>
            <p>Pot odds = 150:50 = <strong>3:1</strong></p>
            <p>Need 25% equity to call</p>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md border-t-4 border-blue-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Equity</h3>
          <p className="text-sm text-gray-600 mb-4">
            <strong>What it is:</strong> Your percentage chance to win the pot at showdown.
          </p>
          <div className="bg-gray-100 rounded-lg p-4 font-mono text-sm">
            <p><strong>Rule of 4 and 2:</strong></p>
            <p>Flop → Turn+River:</p>
            <p>Outs × 4 = Equity %</p>
            <p className="mt-2">Turn → River:</p>
            <p>Outs × 2 = Equity %</p>
            <p className="mt-2">9 outs (flush) × 4 = <strong>36%</strong></p>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md border-t-4 border-blue-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Pot Odds vs Equity</h3>
          <p className="text-sm text-gray-600 mb-4">
            <strong>Decision rule:</strong> Compare your equity to the pot odds.
          </p>
          <div className="bg-gray-100 rounded-lg p-4 font-mono text-sm">
            <p>Pot odds = 3:1 (25%)</p>
            <p>Your equity = 36%</p>
            <p className="mt-2 text-green-700 font-bold">36% &gt; 25%</p>
            <p className="mt-2"><strong>→ CALL is profitable</strong></p>
            <p className="mt-2 text-sm">You need 25% to break even, you have 36%</p>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-md border-t-4 border-blue-500">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Implied Odds</h3>
          <p className="text-sm text-gray-600 mb-4">
            <strong>What it is:</strong> Pot odds + potential future bets you can win.
          </p>
          <div className="bg-gray-100 rounded-lg p-4 font-mono text-sm">
            <p><strong>Example:</strong></p>
            <p>Current pot odds: 25%</p>
            <p>Your equity: 20%</p>
            <p className="mt-2">BUT opponent has $200 left</p>
            <p className="mt-2 text-green-700">If you hit, you can win more</p>
            <p className="mt-2"><strong>→ CALL can be profitable</strong></p>
          </div>
        </div>
      </div>

      {/* Real Example */}
      <div className="bg-white rounded-xl p-8 shadow-lg max-w-4xl mx-auto">
        <h3 className="text-2xl font-bold text-gray-800 mb-6">Real Example: Drawing to a Flush on the Flop</h3>

        <div className="space-y-6">
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p className="font-semibold mb-2">Step 1: Calculate Equity</p>
            <p className="text-gray-700">You have 9 flush outs (13 cards of your suit - 4 you can see = 9 remaining)</p>
            <p className="font-mono text-blue-700">9 outs × 4 = <strong>36% equity</strong></p>
          </div>

          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p className="font-semibold mb-2">Step 2: Calculate Pot Odds</p>
            <p className="text-gray-700">Pot is $100, opponent bets $50</p>
            <p className="font-mono text-blue-700">You call $50 to win $150 = 3:1 = <strong>25% pot odds</strong></p>
          </div>

          <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
            <p className="font-semibold mb-2">Step 3: Compare and Decide</p>
            <p className="text-gray-700">Your equity (36%) &gt; Pot odds (25%)</p>
            <p className="font-bold text-green-700 text-lg mt-2">✓ CALL - This is profitable long-term</p>
          </div>
        </div>

        {/* Turn Example */}
        <div className="mt-8 bg-gray-50 rounded-xl p-6">
          <h4 className="text-xl font-bold text-gray-800 mb-4">Scenario: Same Draw on the Turn</h4>
          <p className="text-gray-700 mb-2"><strong>Your hand:</strong> A♠ K♠ | <strong>Board:</strong> 9♠ 6♠ 2♥ 7♣</p>
          <p className="text-gray-700 mb-4"><strong>Pot:</strong> $600 | <strong>Opponent bets:</strong> $600 (pot-sized)</p>

          <div className="space-y-4">
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <p className="font-semibold mb-2">Step 1: Calculate Equity</p>
              <p className="font-mono text-blue-700">9 flush outs × 2 = <strong>18% equity</strong> (approximately)</p>
            </div>

            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <p className="font-semibold mb-2">Step 2: Calculate Pot Odds</p>
              <p className="font-mono text-blue-700">Call $600 to win $1200 → 1200:600 = 2:1 = <strong>33% required</strong></p>
            </div>

            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <p className="font-semibold mb-2">Step 3: Compare</p>
              <p className="text-gray-700">Your equity (18%) &lt; Required equity (33%)</p>
              <p className="font-bold text-red-700 text-lg mt-2">✗ FOLD - not enough equity</p>
            </div>
          </div>
        </div>

        {/* Quick Reference */}
        <div className="mt-8">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">Quick Reference: Outs to Equity</h4>
          <table className="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
            <thead>
              <tr className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
                <th className="p-3 text-left">Outs</th>
                <th className="p-3 text-left">Turn</th>
                <th className="p-3 text-left">River</th>
                <th className="p-3 text-left">Example</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-200 hover:bg-gray-100">
                <td className="p-3 font-semibold">15</td>
                <td className="p-3">60%</td>
                <td className="p-3">30%</td>
                <td className="p-3">Flush draw + straight draw</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-100">
                <td className="p-3 font-semibold">12</td>
                <td className="p-3">48%</td>
                <td className="p-3">24%</td>
                <td className="p-3">Flush draw + overcard pair draw</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-100">
                <td className="p-3 font-semibold">9</td>
                <td className="p-3">36%</td>
                <td className="p-3">18%</td>
                <td className="p-3">Flush draw</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-100">
                <td className="p-3 font-semibold">8</td>
                <td className="p-3">32%</td>
                <td className="p-3">16%</td>
                <td className="p-3">Open-ended straight draw</td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-100">
                <td className="p-3 font-semibold">4</td>
                <td className="p-3">16%</td>
                <td className="p-3">8%</td>
                <td className="p-3">Gutshot straight draw</td>
              </tr>
              <tr className="hover:bg-gray-100">
                <td className="p-3 font-semibold">2</td>
                <td className="p-3">8%</td>
                <td className="p-3">4%</td>
                <td className="p-3">Pocket pair to set</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
