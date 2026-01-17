#!/usr/bin/env python3
"""
Interactive visualization dashboard for poker equity data.
Creates heatmaps, charts, and tables using plotly.
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
        print(f"   Run 'python generate_equity_data.py' first to generate data")
        sys.exit(1)

    with open(cache_file, 'r') as f:
        return json.load(f)


def create_hand_grid(hands_data, metric='equity', num_players=6):
    """
    Create 13x13 grid for poker hand chart.

    Args:
        hands_data: Dict of hand data
        metric: 'equity' or 'win_rate'
        num_players: Table size (2-6 players)

    Returns:
        grid: 13x13 matrix of values
        labels: 13x13 matrix of hand labels
    """
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    # Initialize grids
    grid = [[0.0 for _ in range(13)] for _ in range(13)]
    labels = [['' for _ in range(13)] for _ in range(13)]

    for i, rank1 in enumerate(ranks):
        for j, rank2 in enumerate(ranks):
            if i == j:
                # Pocket pairs (diagonal)
                hand = rank1 + rank2
            elif i < j:
                # Suited hands (upper triangle)
                hand = rank1 + rank2 + 's'
            else:
                # Offsuit hands (lower triangle)
                hand = rank2 + rank1 + 'o'

            # Get metric value
            player_key = f'players_{num_players}'
            if hand in hands_data and player_key in hands_data[hand]:
                value = hands_data[hand][player_key][metric]
                grid[i][j] = value * 100  # Convert to percentage
                labels[i][j] = hand

    return grid, labels


def create_equity_heatmap_with_dropdown(data):
    """Create interactive equity heatmap with dropdown for table size selection"""
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
            textfont={"size": 10},
            colorscale='RdYlGn',
            colorbar=dict(title="Equity %"),
            hovertemplate='<b>%{text}</b><br>Equity: %{z:.2f}%<extra></extra>',
            visible=(num_players == 6)  # Show 6-max by default
        )
        traces.append(trace)

    # Create figure with all traces
    fig = go.Figure(data=traces)

    # Create dropdown buttons
    buttons = []
    for i, num_players in enumerate(range(2, 7)):
        label = "Heads-Up (2 players)" if num_players == 2 else f"{num_players} Players"
        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {"visible": [j == i for j in range(5)]},
                    {"title": f'Poker Starting Hand Equity - {label}<br><sub>Diagonal: Pairs | Upper Right: Suited | Lower Left: Offsuit</sub>'}
                ]
            )
        )

    # Add dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                active=4,  # 6-max is index 4 (0=2p, 1=3p, 2=4p, 3=5p, 4=6p)
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        title=f'Poker Starting Hand Equity - 6 Players<br><sub>Diagonal: Pairs | Upper Right: Suited | Lower Left: Offsuit</sub>',
        xaxis_title="Second Card",
        yaxis_title="First Card",
        width=900,
        height=850,
        xaxis=dict(side='top'),
        yaxis=dict(autorange='reversed'),  # Reverse Y-axis so AA is top-left
        font=dict(size=12)
    )

    return fig


def create_winrate_heatmap_with_dropdown(data):
    """Create interactive win rate heatmap with dropdown for table size selection"""
    hands_data = data['hands']
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    # Create traces for each table size
    traces = []
    for num_players in range(2, 7):
        grid, labels = create_hand_grid(hands_data, 'win_rate', num_players)

        trace = go.Heatmap(
            z=grid,
            x=ranks,
            y=ranks,
            text=labels,
            texttemplate='%{text}<br>%{z:.1f}%',
            textfont={"size": 10},
            colorscale='Blues',
            colorbar=dict(title="Win Rate %"),
            hovertemplate='<b>%{text}</b><br>Win Rate: %{z:.2f}%<extra></extra>',
            visible=(num_players == 6)  # Show 6-max by default
        )
        traces.append(trace)

    # Create figure with all traces
    fig = go.Figure(data=traces)

    # Create dropdown buttons
    buttons = []
    for i, num_players in enumerate(range(2, 7)):
        label = "Heads-Up (2 players)" if num_players == 2 else f"{num_players} Players"
        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {"visible": [j == i for j in range(5)]},
                    {"title": f'Poker Starting Hand Win Rate - {label}<br><sub>Diagonal: Pairs | Upper Right: Suited | Lower Left: Offsuit</sub>'}
                ]
            )
        )

    # Add dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                active=4,  # 6-max is index 4
                buttons=buttons,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        title=f'Poker Starting Hand Win Rate - 6 Players<br><sub>Diagonal: Pairs | Upper Right: Suited | Lower Left: Offsuit</sub>',
        xaxis_title="Second Card",
        yaxis_title="First Card",
        width=900,
        height=850,
        xaxis=dict(side='top'),
        yaxis=dict(autorange='reversed'),  # Reverse Y-axis so AA is top-left
        font=dict(size=12)
    )

    return fig


def create_rankings_table(data, num_players=6, top_n=50):
    """Create hand rankings table"""
    hands_data = data['hands']
    player_key = f'players_{num_players}'

    # Get all hands with equity
    hand_equities = [
        (hand, values[player_key]['equity'], values[player_key]['win_rate'])
        for hand, values in hands_data.items()
        if player_key in values
    ]

    # Sort by equity
    hand_equities.sort(key=lambda x: x[1], reverse=True)

    # Take top N
    top_hands = hand_equities[:top_n]

    # Prepare table data
    ranks = list(range(1, len(top_hands) + 1))
    hands = [h[0] for h in top_hands]
    equities = [f"{h[1]*100:.2f}%" for h in top_hands]
    win_rates = [f"{h[2]*100:.2f}%" for h in top_hands]

    # Color code rows
    colors = []
    for rank in ranks:
        if rank <= 10:
            colors.append('lightgreen')  # Premium
        elif rank <= 25:
            colors.append('lightyellow')  # Strong
        else:
            colors.append('lightcoral')  # Marginal

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Rank</b>', '<b>Hand</b>', '<b>Equity</b>', '<b>Win Rate</b>'],
            fill_color='paleturquoise',
            align='center',
            font=dict(size=14)
        ),
        cells=dict(
            values=[ranks, hands, equities, win_rates],
            fill_color=[colors, colors, colors, colors],
            align=['center', 'center', 'center', 'center'],
            font=dict(size=12),
            height=30
        )
    )])

    fig.update_layout(
        title=f'Top {top_n} Starting Hands by Equity - {num_players} Players',
        width=600,
        height=800
    )

    return fig


def create_equity_vs_players_chart(data, selected_hands=None):
    """
    Create line chart showing how equity changes with table size.

    Args:
        data: Equity data
        selected_hands: List of hand strings to plot. If None, uses defaults.
    """
    hands_data = data['hands']

    # Default hand categories if none specified
    if selected_hands is None:
        selected_hands = [
            'AA', 'KK', 'QQ',  # Premium pairs
            '88', '77', '66',  # Mid pairs
            'AKs', 'AQs', 'KQs',  # Premium suited
            'AKo', 'AQo',  # Premium offsuit
            '87s', '76s',  # Suited connectors
        ]

    fig = go.Figure()

    # Plot each hand
    for hand in selected_hands:
        if hand not in hands_data:
            continue

        players = list(range(2, 7))
        equities = []

        for num_players in players:
            player_key = f'players_{num_players}'
            equity = hands_data[hand][player_key]['equity'] * 100
            equities.append(equity)

        # Determine line style
        if len(hand) == 2:  # Pocket pair
            line_style = dict(width=3)
        elif hand.endswith('s'):  # Suited
            line_style = dict(width=2, dash='dot')
        else:  # Offsuit
            line_style = dict(width=2, dash='dash')

        fig.add_trace(go.Scatter(
            x=players,
            y=equities,
            mode='lines+markers',
            name=hand,
            line=line_style,
            marker=dict(size=8),
            hovertemplate='%{y:.2f}%<extra></extra>'
        ))

    fig.update_layout(
        title='Starting Hand Equity vs. Table Size<br><sub>Solid: Pairs | Dotted: Suited | Dashed: Offsuit</sub>',
        xaxis_title='Number of Players',
        yaxis_title='Equity %',
        xaxis=dict(
            tickmode='linear',
            tick0=2,
            dtick=1
        ),
        yaxis=dict(range=[0, 100]),
        width=900,
        height=600,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    return fig


def create_dashboard(data):
    """Create complete interactive dashboard with all visualizations"""

    # Create individual figures for each table size
    print("Creating visualizations...")

    all_figs = []

    # Equity heatmaps for each table size
    for num_players in range(2, 7):
        fig = create_equity_heatmap(data, num_players)
        all_figs.append(fig)

    # Win rate heatmaps for each table size
    for num_players in range(2, 7):
        fig = create_winrate_heatmap(data, num_players)
        all_figs.append(fig)

    # Rankings tables for key table sizes
    for num_players in [2, 6]:
        fig = create_rankings_table(data, num_players, top_n=50)
        all_figs.append(fig)

    # Equity vs players chart
    fig = create_equity_vs_players_chart(data)
    all_figs.append(fig)

    return all_figs


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Visualize poker equity data"
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
        default='poker_equity_dashboard.html',
        help='Output HTML file (default: poker_equity_dashboard.html)'
    )
    parser.add_argument(
        '--players', '-p',
        type=int,
        choices=[2, 3, 4, 5, 6],
        default=6,
        help='Number of players for quick view (default: 6)'
    )
    parser.add_argument(
        '--chart', '-t',
        type=str,
        choices=['equity', 'winrate', 'rankings', 'trend', 'all'],
        default='all',
        help='Chart type to display (default: all)'
    )

    args = parser.parse_args()

    # Load data
    print(f"Loading data from {args.cache}...")
    data = load_equity_data(args.cache)

    print(f"Data loaded: {data['metadata']['num_hands']} hands")
    print(f"Generated: {data['metadata']['generated_at']}")
    print(f"Simulations: {data['metadata']['num_simulations']:,} per hand\n")

    # Create visualizations based on chart type
    if args.chart == 'equity':
        print("Creating equity heatmap with dropdown...")
        fig = create_equity_heatmap_with_dropdown(data)
        fig.show()
    elif args.chart == 'winrate':
        print("Creating win rate heatmap with dropdown...")
        fig = create_winrate_heatmap_with_dropdown(data)
        fig.show()
    elif args.chart == 'rankings':
        fig = create_rankings_table(data, args.players)
        fig.show()
    elif args.chart == 'trend':
        fig = create_equity_vs_players_chart(data)
        fig.show()
    elif args.chart == 'all':
        print("Creating comprehensive dashboard...")
        print("This will open multiple visualizations in your browser.")

        # Show key visualizations with dropdowns
        print("\n1. Equity Heatmap (with dropdown for 2-6 players)")
        fig_equity = create_equity_heatmap_with_dropdown(data)
        fig_equity.show()

        print("\n2. Win Rate Heatmap (with dropdown for 2-6 players)")
        fig_winrate = create_winrate_heatmap_with_dropdown(data)
        fig_winrate.show()

        print("\n3. Top 50 Hand Rankings (6 players)")
        fig_rankings = create_rankings_table(data, 6, top_n=50)
        fig_rankings.show()

        print("\n4. Equity vs Table Size")
        fig_trend = create_equity_vs_players_chart(data)
        fig_trend.show()

        print(f"\n✓ All visualizations displayed!")
        print("   Use the dropdown menu at the top to switch between table sizes!")

    print("\n" + "="*60)
    print("USAGE TIPS:")
    print("="*60)
    print("• Use the DROPDOWN MENU at the top to switch between table sizes")
    print("• Hover over cells for detailed information")
    print("• AA is in the TOP-LEFT, 22 is in the BOTTOM-RIGHT")
    print("• Diagonal = Pairs | Upper Right = Suited | Lower Left = Offsuit")
    print("• Use plotly controls to zoom, pan, and save as image")
    print("• Green = high equity, Red = low equity in heatmaps")
    print("\nQuick commands:")
    print("  python visualize_equity.py --chart equity")
    print("  python visualize_equity.py --chart winrate")
    print("  python visualize_equity.py --chart trend")
    print("  python visualize_equity.py --chart rankings --players 6")


if __name__ == "__main__":
    main()
