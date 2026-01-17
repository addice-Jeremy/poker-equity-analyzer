#!/usr/bin/env python3
"""
Generate a standalone HTML website for poker equity analysis.
Creates a single-page educational resource with interactive visualizations.
"""

import json
import sys
from pathlib import Path

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Installing plotly...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots


def load_equity_data(cache_file='equity_cache.json'):
    """Load equity data from cache file"""
    if not Path(cache_file).exists():
        print(f"❌ Cache file not found: {cache_file}")
        print(f"   Run 'python generate_equity_data.py' first")
        sys.exit(1)

    with open(cache_file, 'r') as f:
        return json.load(f)


def create_hand_grid(hands_data, metric='equity', num_players=6):
    """Create 13x13 grid for poker hand chart"""
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    grid = [[0.0 for _ in range(13)] for _ in range(13)]
    labels = [['' for _ in range(13)] for _ in range(13)]

    for i, rank1 in enumerate(ranks):
        for j, rank2 in enumerate(ranks):
            if i == j:
                hand = rank1 + rank2
            elif i < j:
                hand = rank1 + rank2 + 's'
            else:
                hand = rank2 + rank1 + 'o'

            player_key = f'players_{num_players}'
            if hand in hands_data and player_key in hands_data[hand]:
                value = hands_data[hand][player_key][metric]
                grid[i][j] = value * 100
                labels[i][j] = hand

    return grid, labels


def create_equity_heatmap_for_website(data):
    """Create equity heatmap optimized for website display"""
    hands_data = data['hands']
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    # Create traces for each table size
    traces = []
    for num_players in range(2, 7):
        grid, labels = create_hand_grid(hands_data, 'equity', num_players)

        trace = go.Heatmap(
            z=grid,
            x=ranks,
            y=ranks,
            text=labels,
            texttemplate='%{text}<br>%{z:.1f}%',
            textfont={"size": 11, "family": "monospace"},
            colorscale='RdYlGn',
            colorbar=dict(
                title=dict(text="Equity %", side="right"),
                tickmode="linear",
                tick0=0,
                dtick=10
            ),
            hovertemplate='<b>%{text}</b><br>Equity: %{z:.2f}%<extra></extra>',
            visible=(num_players == 6)
        )
        traces.append(trace)

    fig = go.Figure(data=traces)

    # Create dropdown buttons
    buttons = []
    player_labels = {
        2: "Heads-Up (2 Players)",
        3: "3-Handed",
        4: "4-Handed",
        5: "5-Handed",
        6: "6-Max"
    }

    for i, num_players in enumerate(range(2, 7)):
        buttons.append(
            dict(
                label=player_labels[num_players],
                method="update",
                args=[
                    {"visible": [j == i for j in range(5)]},
                    {"title.text": f"Poker Starting Hand Equity - {player_labels[num_players]}"}
                ]
            )
        )

    # Layout optimized for web
    fig.update_layout(
        updatemenus=[
            dict(
                active=4,
                buttons=buttons,
                direction="down",
                showactive=True,
                x=1.0,
                xanchor="right",
                y=1.02,
                yanchor="bottom",
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="#ccc",
                borderwidth=1
            )
        ],
        title={
            'text': "Poker Starting Hand Equity - 6-Max",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Second Card",
        yaxis_title="First Card",
        width=None,  # Responsive width
        height=700,
        xaxis=dict(side='top', tickfont=dict(size=12)),
        yaxis=dict(autorange='reversed', tickfont=dict(size=12)),
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=60, r=60, t=100, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return fig


def create_equity_trends_chart(data):
    """Create chart showing how equity changes with table size for key hands"""
    hands_data = data['hands']

    # Select representative hands
    hands_to_plot = {
        'Premium Pairs': ['AA', 'KK', 'QQ'],
        'Mid Pairs': ['88', '77', '66'],
        'High Cards': ['AKs', 'AQs', 'AKo'],
        'Suited Connectors': ['JTs', '98s', '87s']
    }

    fig = go.Figure()

    colors = {
        'Premium Pairs': '#e74c3c',
        'Mid Pairs': '#f39c12',
        'High Cards': '#3498db',
        'Suited Connectors': '#27ae60'
    }

    for category, hands in hands_to_plot.items():
        for hand in hands:
            if hand not in hands_data:
                continue

            players = list(range(2, 7))
            equities = []

            for num_players in players:
                player_key = f'players_{num_players}'
                equity = hands_data[hand][player_key]['equity'] * 100
                equities.append(equity)

            fig.add_trace(go.Scatter(
                x=players,
                y=equities,
                mode='lines+markers',
                name=hand,
                line=dict(color=colors[category], width=2),
                marker=dict(size=8),
                legendgroup=category,
                legendgrouptitle=dict(text=category),
                hovertemplate=f'<b>{hand}</b><br>Equity: %{{y:.1f}}%<extra></extra>'
            ))

    fig.update_layout(
        title='How Hand Equity Changes with Table Size',
        xaxis_title='Number of Players',
        yaxis_title='Equity %',
        xaxis=dict(tickmode='linear', tick0=2, dtick=1),
        yaxis=dict(range=[0, 100]),
        height=500,
        hovermode='x unified',
        legend=dict(groupclick="togglegroup"),
        font=dict(family='Arial, sans-serif')
    )

    return fig


def generate_insights_html(data):
    """Generate HTML for key insights section"""
    hands_data = data['hands']

    # Get key statistics
    aa_hu = hands_data['AA']['players_2']['equity'] * 100
    aa_6max = hands_data['AA']['players_6']['equity'] * 100
    aa_drop = aa_hu - aa_6max

    aks_equity = hands_data['AKs']['players_6']['equity'] * 100
    ako_equity = hands_data['AKo']['players_6']['equity'] * 100
    suited_bonus = aks_equity - ako_equity

    # Generate trends chart
    trends_fig = create_equity_trends_chart(data)
    trends_html = trends_fig.to_html(
        include_plotlyjs=False,
        div_id='trends-chart',
        config={'displayModeBar': True, 'displaylogo': False}
    )

    html = f"""
    <div class="how-to-read">
        <h2>How to Read the Chart</h2>

        <div class="reading-guide">
            <div class="guide-section">
                <h3>Chart Layout</h3>
                <ul>
                    <li><strong>Diagonal (AA to 22):</strong> Pocket pairs</li>
                    <li><strong>Upper Right Triangle:</strong> Suited hands (AKs, KQs, 87s, etc.)</li>
                    <li><strong>Lower Left Triangle:</strong> Offsuit hands (AKo, KQo, 87o, etc.)</li>
                    <li><strong>AA is Top-Left, 22 is Bottom-Right</strong></li>
                </ul>
            </div>

            <div class="guide-section">
                <h3>Color Guide</h3>
                <ul>
                    <li><span class="color-demo green">🟢 Green (40%+):</span> Premium hands - raise from any position</li>
                    <li><span class="color-demo yellow">🟡 Yellow (25-40%):</span> Strong hands - raise from middle/late position</li>
                    <li><span class="color-demo orange">🟠 Orange (15-25%):</span> Playable hands - late position or with good odds</li>
                    <li><span class="color-demo red">🔴 Red (&lt;15%):</span> Weak hands - fold in most situations</li>
                </ul>
            </div>

            <div class="guide-section">
                <h3>Using the Dropdown</h3>
                <ol>
                    <li>Click the dropdown menu in the <strong>top-right corner</strong></li>
                    <li>Select different table sizes (Heads-Up through 6-Max)</li>
                    <li>Watch how hand equities change with more opponents</li>
                    <li>Notice premium pairs drop dramatically, while suited cards hold up better</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="practical-strategy">
        <h2>Practical Strategy Guide</h2>

        <div class="strategy-grid">
            <div class="strategy-card">
                <h3>Early Position (Tight Range)</h3>
                <p class="range-desc">Top ~15% of hands</p>
                <p><strong>Raise:</strong> AA-TT, AKs, AKo, AQs</p>
                <p><strong>Why:</strong> You'll face multiple opponents and act first post-flop.
                Need strong hands that play well multi-way.</p>
            </div>

            <div class="strategy-card">
                <h3>Middle Position (Standard Range)</h3>
                <p class="range-desc">Top ~25% of hands</p>
                <p><strong>Raise:</strong> AA-77, AK-AJ, KQs, KJs, QJs</p>
                <p><strong>Why:</strong> Fewer players behind you. Can still face resistance
                but position advantage on some opponents.</p>
            </div>

            <div class="strategy-card">
                <h3>Button (Wide Range)</h3>
                <p class="range-desc">Top ~40% of hands</p>
                <p><strong>Raise:</strong> All pairs, suited aces, suited connectors, broadway cards</p>
                <p><strong>Why:</strong> Best position post-flop. Can play weaker hands profitably.
                Position compensates for lower equity.</p>
            </div>

            <div class="strategy-card">
                <h3>Big Blind Defense</h3>
                <p class="range-desc">~30-40% vs button raise</p>
                <p><strong>Call:</strong> Hands with >30% equity vs button's range + good playability</p>
                <p><strong>Why:</strong> Already invested money (the blind). Need decent equity
                to defend, but don't need premium hands.</p>
            </div>
        </div>
    </div>

    <div class="poker-odds-section">
        <h2>How to Calculate Poker Odds</h2>
        <p class="section-intro">Every action you make, hand you play, or bet you face has odds, probability, and statistics attached to it.
        Here are the main poker numbers you need to master:</p>

        <div class="odds-grid">
            <div class="odds-card">
                <h3>Pot Odds</h3>
                <p><strong>What it is:</strong> The ratio of the current pot size to the cost of a contemplated call.</p>
                <div class="example-box">
                    <p><strong>Example:</strong></p>
                    <p>Pot = $100, Bet = $50<br>
                    You need to call $50 to win $150<br>
                    Pot odds = 150:50 = <strong>3:1</strong><br>
                    Need 25% equity to call profitably</p>
                </div>
            </div>

            <div class="odds-card">
                <h3>Equity</h3>
                <p><strong>What it is:</strong> Your expected share of the pot based on how often you win.</p>
                <div class="example-box">
                    <p><strong>Calculating Outs:</strong></p>
                    <p>Drawing to a flush? You have 13 suited cards<br>
                    2 in hand + 2 on board = 4 known<br>
                    Outs = 13 - 4 = <strong>9 outs</strong><br><br>
                    <strong>On the turn:</strong> 9 × 4 = 36% (~40%)<br>
                    <strong>On the river:</strong> 9 × 2 = 18% (~20%)</p>
                </div>
            </div>

            <div class="odds-card">
                <h3>Pot Odds vs Equity</h3>
                <p><strong>What it is:</strong> Comparing your equity to the pot odds to make profitable decisions.</p>
                <div class="example-box">
                    <p><strong>Common Scenarios:</strong></p>
                    <p><strong>1/2 pot bet:</strong> 3:1 odds → Need 25% equity<br>
                    <strong>3/4 pot bet:</strong> 7:3 odds → Need 30% equity<br>
                    <strong>Pot sized bet:</strong> 2:1 odds → Need 33% equity<br>
                    <strong>2x pot bet:</strong> 3:2 odds → Need 40% equity</p>
                </div>
            </div>

            <div class="odds-card">
                <h3>Implied Odds</h3>
                <p><strong>What it is:</strong> Potential future winnings if you hit your draw.</p>
                <div class="example-box">
                    <p><strong>Example:</strong></p>
                    <p>Flush draw on flop (9 outs = ~35% to hit)<br>
                    Opponent bets pot ($100), you call $100<br>
                    If you hit, you expect to win $300+ more<br>
                    <strong>Implied odds justify the call</strong></p>
                </div>
            </div>
        </div>

        <div class="decision-framework">
            <h3>Applying Odds in Real Situations</h3>

            <div class="situation-example">
                <h4>Scenario: Drawing to a Flush on the Flop</h4>
                <p><strong>Your hand:</strong> A♠ K♠ | <strong>Board:</strong> 9♠ 6♠ 2♥</p>
                <p><strong>Pot:</strong> $200 | <strong>Opponent bets:</strong> $200 (pot-sized)</p>

                <div class="calculation-steps">
                    <div class="step">
                        <strong>Step 1: Calculate Equity</strong>
                        <p>9 flush outs × 4 = 36% equity (approximately)</p>
                    </div>

                    <div class="step">
                        <strong>Step 2: Calculate Pot Odds</strong>
                        <p>Call $200 to win $400 → 400:200 = 2:1 = 33% required</p>
                    </div>

                    <div class="step">
                        <strong>Step 3: Compare</strong>
                        <p>Your equity (36%) > Required equity (33%)</p>
                        <p class="decision-good">✓ CALL is profitable</p>
                    </div>

                    <div class="step">
                        <strong>Step 4: Consider Implied Odds</strong>
                        <p>If opponent has two pair, they may pay you off big on turn/river</p>
                        <p>But watch out - they could also improve to a full house!</p>
                    </div>
                </div>
            </div>

            <div class="situation-example">
                <h4>Scenario: Same Draw on the Turn</h4>
                <p><strong>Your hand:</strong> A♠ K♠ | <strong>Board:</strong> 9♠ 6♠ 2♥ 7♣</p>
                <p><strong>Pot:</strong> $600 | <strong>Opponent bets:</strong> $600 (pot-sized)</p>

                <div class="calculation-steps">
                    <div class="step">
                        <strong>Step 1: Calculate Equity</strong>
                        <p>9 flush outs × 2 = 18% equity (approximately)</p>
                    </div>

                    <div class="step">
                        <strong>Step 2: Calculate Pot Odds</strong>
                        <p>Call $600 to win $1200 → 1200:600 = 2:1 = 33% required</p>
                    </div>

                    <div class="step">
                        <strong>Step 3: Compare</strong>
                        <p>Your equity (18%) < Required equity (33%)</p>
                        <p class="decision-bad">✗ FOLD - not enough equity</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="quick-reference">
            <h3>Quick Reference: Outs to Equity</h3>
            <table class="outs-table">
                <thead>
                    <tr>
                        <th>Outs</th>
                        <th>Turn</th>
                        <th>River</th>
                        <th>Example</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>15</td>
                        <td>60%</td>
                        <td>30%</td>
                        <td>Flush draw + straight draw</td>
                    </tr>
                    <tr>
                        <td>12</td>
                        <td>48%</td>
                        <td>24%</td>
                        <td>Flush draw + overcard pair draw</td>
                    </tr>
                    <tr>
                        <td>9</td>
                        <td>36%</td>
                        <td>18%</td>
                        <td>Flush draw</td>
                    </tr>
                    <tr>
                        <td>8</td>
                        <td>32%</td>
                        <td>16%</td>
                        <td>Open-ended straight draw</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>16%</td>
                        <td>8%</td>
                        <td>Gutshot straight draw</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>8%</td>
                        <td>4%</td>
                        <td>Pocket pair to set</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="insights-section">
        <h2>Key Insights</h2>

        <div class="insights-container">
            <div class="insight-box">
                <h3>Premium Pairs Lose Value</h3>
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-number good">{aa_hu:.1f}%</div>
                        <div class="stat-desc">Heads-up</div>
                    </div>
                    <div class="stat-arrow">→</div>
                    <div class="stat-item">
                        <div class="stat-number bad">{aa_6max:.1f}%</div>
                        <div class="stat-desc">6-max</div>
                    </div>
                </div>
                <p class="insight-text">AA equity drops {aa_drop:.1f}% with more opponents</p>
                <p class="insight-tip">Raise pre-flop to thin the field</p>
            </div>

            <div class="insight-box">
                <h3>Suited Advantage</h3>
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-number good">{aks_equity:.1f}%</div>
                        <div class="stat-desc">AKs</div>
                    </div>
                    <div class="stat-vs">vs</div>
                    <div class="stat-item">
                        <div class="stat-number">{ako_equity:.1f}%</div>
                        <div class="stat-desc">AKo</div>
                    </div>
                </div>
                <p class="insight-text">Suited gives +{suited_bonus:.1f}% equity at 6-max</p>
                <p class="insight-tip">High cards matter more than suited</p>
            </div>

            <div class="insight-box">
                <h3>Position Value</h3>
                <div class="stat-single">
                    <div class="stat-number-large">~5%</div>
                </div>
                <p class="insight-text">Equity advantage from position</p>
                <p class="insight-tip">Play 40% from button, 15% early</p>
            </div>

            <div class="insight-box">
                <h3>Small Pairs Strategy</h3>
                <div class="stat-single">
                    <div class="stat-number-large">15:1</div>
                </div>
                <p class="insight-text">Minimum implied odds needed</p>
                <p class="insight-tip">Fold without deep stacks</p>
            </div>
        </div>
    </div>

    <div class="trends-section">
        <h2>Equity Trends by Table Size</h2>
        <p class="section-intro">How different hand categories scale as more players enter the pot.</p>
        {trends_html}
    </div>

    <div class="methodology">
        <h2>About This Data</h2>
        <p>Based on Monte Carlo simulation with <strong>{data['metadata']['num_simulations']:,} simulations</strong> per hand per table size. All 169 starting hands simulated across 2-6 player tables with ±0.5% accuracy.</p>
    </div>
    """

    return html


def generate_website(data, output_file='poker_equity_website.html'):
    """Generate complete standalone website"""

    # Create the interactive heatmap
    fig = create_equity_heatmap_for_website(data)

    # Get the HTML div for the plot
    plot_html = fig.to_html(
        include_plotlyjs='cdn',
        div_id='equity-heatmap',
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'poker_equity_chart',
                'height': 700,
                'width': 1000
            }
        }
    )

    # Generate insights HTML
    insights_html = generate_insights_html(data)

    # Complete HTML with styling
    complete_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poker Starting Hand Equity Analysis</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header p {{
            font-size: 1.3em;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }}

        .chart-section {{
            padding: 40px;
            background: #f8f9fa;
        }}

        .chart-intro {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .chart-intro h2 {{
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}

        .chart-intro p {{
            font-size: 1.1em;
            color: #666;
        }}

        #equity-heatmap {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .insights-section {{
            padding: 60px 40px;
            background: white;
        }}

        .insights-section h2 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 40px;
            text-align: center;
        }}

        .insights-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
            justify-content: center;
        }}

        .insight-box {{
            flex: 1 1 250px;
            max-width: 280px;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            box-sizing: border-box;
        }}

        .insight-box h3 {{
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }}

        .stat-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: nowrap;
        }}

        .stat-item {{
            text-align: center;
            flex-shrink: 0;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: 700;
            color: #3498db;
            line-height: 1;
            margin-bottom: 5px;
        }}

        .stat-number.good {{
            color: #27ae60;
        }}

        .stat-number.bad {{
            color: #e74c3c;
        }}

        .stat-desc {{
            font-size: 0.85em;
            color: #7f8c8d;
        }}

        .stat-arrow {{
            font-size: 1.5em;
            color: #95a5a6;
            flex-shrink: 0;
        }}

        .stat-vs {{
            font-size: 1em;
            color: #95a5a6;
            font-weight: 600;
            flex-shrink: 0;
        }}

        .stat-single {{
            text-align: center;
            margin: 20px 0;
        }}

        .stat-number-large {{
            font-size: 3em;
            font-weight: 700;
            color: #3498db;
            line-height: 1;
        }}

        .insight-text {{
            font-size: 0.95em;
            color: #666;
            text-align: center;
            margin: 15px 0 10px 0;
            line-height: 1.4;
        }}

        .insight-tip {{
            font-size: 0.9em;
            color: #3498db;
            font-weight: 600;
            text-align: center;
            margin-top: 10px;
        }}

        .how-to-read {{
            padding: 60px 40px;
            background: #ecf0f1;
        }}

        .how-to-read h2 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 40px;
            text-align: center;
        }}

        .reading-guide {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        .guide-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .guide-section h3 {{
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}

        .guide-section ul, .guide-section ol {{
            padding-left: 20px;
        }}

        .guide-section li {{
            margin: 10px 0;
            font-size: 1.05em;
        }}

        .color-demo {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}

        .color-demo.green {{
            background: #d4edda;
            color: #155724;
        }}

        .color-demo.yellow {{
            background: #fff3cd;
            color: #856404;
        }}

        .color-demo.orange {{
            background: #ffe0b2;
            color: #e65100;
        }}

        .color-demo.red {{
            background: #f8d7da;
            color: #721c24;
        }}

        .practical-strategy {{
            padding: 60px 40px;
            background: white;
        }}

        .practical-strategy h2 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 40px;
            text-align: center;
        }}

        .strategy-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }}

        .strategy-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .strategy-card h3 {{
            font-size: 1.4em;
            margin-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }}

        .range-desc {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 15px;
            font-style: italic;
        }}

        .methodology {{
            padding: 40px;
            background: #f8f9fa;
            text-align: center;
        }}

        .methodology h2 {{
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 20px;
        }}

        .methodology p {{
            font-size: 1.05em;
            line-height: 1.8;
            color: #666;
            max-width: 800px;
            margin: 0 auto;
        }}

        .formula-box {{
            background: #34495e;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}

        .formula-content {{
            color: #ecf0f1;
            font-family: 'Courier New', monospace;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
        }}

        .trends-section {{
            padding: 60px 40px;
            background: white;
        }}

        .trends-section h2 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }}

        .section-intro {{
            text-align: center;
            font-size: 1.1em;
            color: #666;
            max-width: 800px;
            margin: 0 auto 30px;
        }}

        #trends-chart {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        code {{
            background: #ecf0f1;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}

        .poker-odds-section {{
            padding: 60px 40px;
            background: #f8f9fa;
        }}

        .poker-odds-section h2 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 40px;
            text-align: center;
        }}

        .poker-odds-section h3 {{
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 15px;
        }}

        .poker-odds-section h4 {{
            font-size: 1.3em;
            color: #34495e;
            margin: 25px 0 15px 0;
        }}

        .odds-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}

        .odds-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-top: 4px solid #3498db;
        }}

        .example-box {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            font-size: 1.05em;
            line-height: 1.8;
        }}

        .decision-framework {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            margin: 40px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .situation-example {{
            margin-bottom: 30px;
        }}

        .calculation-steps {{
            margin-top: 20px;
        }}

        .step {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }}

        .step strong {{
            color: #2c3e50;
            font-size: 1.1em;
            display: block;
            margin-bottom: 10px;
        }}

        .decision-good {{
            background: #d4edda;
            border-left-color: #27ae60;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}

        .decision-bad {{
            background: #f8d7da;
            border-left-color: #e74c3c;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #e74c3c;
        }}

        .outs-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
            background: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}

        .outs-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-size: 1.1em;
        }}

        .outs-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}

        .outs-table tr:last-child td {{
            border-bottom: none;
        }}

        .outs-table tr:hover {{
            background: #f8f9fa;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}

            .header p {{
                font-size: 1em;
            }}

            .insights-container {{
                flex-direction: column;
            }}

            .insight-box {{
                max-width: 100%;
            }}

            .reading-guide, .strategy-grid, .odds-grid {{
                grid-template-columns: 1fr;
            }}

            #equity-heatmap {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Poker Starting Hand Equity Analysis</h1>
            <p>Master pre-flop strategy with data-driven insights from 42+ million simulated hands</p>
        </div>

        <div class="chart-section">
            <div class="chart-intro">
                <h2>Interactive Equity Heatmap</h2>
                <p>Use the dropdown in the top-right to switch between table sizes.
                Hover over any cell for detailed statistics.</p>
            </div>
            {plot_html}
        </div>

        {insights_html}
    </div>
</body>
</html>
    """

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(complete_html)

    print(f"✓ Website generated: {output_file}")
    return output_file


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate poker equity analysis website"
    )
    parser.add_argument(
        '--cache', '-c',
        type=str,
        default='equity_cache.json',
        help='Cache file path (default: equity_cache.json)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='poker_equity_website.html',
        help='Output HTML file (default: poker_equity_website.html)'
    )

    args = parser.parse_args()

    print("Loading equity data...")
    data = load_equity_data(args.cache)

    print(f"Generating website with {data['metadata']['num_hands']} hands...")
    output_file = generate_website(data, args.output)

    print(f"\n✨ Success! Open the file in your browser:")
    print(f"   file://{Path(output_file).absolute()}")
    print(f"\nOr run: open {output_file}")


if __name__ == "__main__":
    main()
