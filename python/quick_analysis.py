#!/usr/bin/env python3
"""
Quick command-line poker equity analyzer.
Load cached data and perform quick lookups and comparisons.
"""

import json
import sys
from pathlib import Path


def load_data(cache_file='equity_cache.json'):
    """Load equity data from cache"""
    if not Path(cache_file).exists():
        print(f"❌ No cache file found. Run: python generate_equity_data.py")
        sys.exit(1)

    with open(cache_file, 'r') as f:
        return json.load(f)


def compare_hands(data, hand1, hand2, num_players=6):
    """Compare two hands at a specific table size"""
    hands_data = data['hands']
    player_key = f'players_{num_players}'

    if hand1 not in hands_data:
        print(f"❌ Hand '{hand1}' not found")
        return

    if hand2 not in hands_data:
        print(f"❌ Hand '{hand2}' not found")
        return

    h1_data = hands_data[hand1][player_key]
    h2_data = hands_data[hand2][player_key]

    print(f"\n{'='*60}")
    print(f"HAND COMPARISON - {num_players} Players")
    print(f"{'='*60}\n")

    print(f"{'Metric':<15} {hand1:>8} {hand2:>8} {'Difference':>12}")
    print(f"{'-'*60}")
    print(f"{'Equity':<15} {h1_data['equity']*100:>7.2f}% {h2_data['equity']*100:>7.2f}% {(h1_data['equity']-h2_data['equity'])*100:>+11.2f}%")
    print(f"{'Win Rate':<15} {h1_data['win_rate']*100:>7.2f}% {h2_data['win_rate']*100:>7.2f}% {(h1_data['win_rate']-h2_data['win_rate'])*100:>+11.2f}%")
    print(f"{'Tie Rate':<15} {h1_data['tie_rate']*100:>7.2f}% {h2_data['tie_rate']*100:>7.2f}% {(h1_data['tie_rate']-h2_data['tie_rate'])*100:>+11.2f}%")
    print()


def show_hand_detail(data, hand, show_all_sizes=True):
    """Show detailed statistics for a single hand"""
    hands_data = data['hands']

    if hand not in hands_data:
        print(f"❌ Hand '{hand}' not found")
        return

    hand_data = hands_data[hand]

    print(f"\n{'='*60}")
    print(f"DETAILED ANALYSIS: {hand}")
    print(f"{'='*60}\n")

    if show_all_sizes:
        print(f"{'Players':<10} {'Equity':>10} {'Win Rate':>10} {'Tie Rate':>10}")
        print(f"{'-'*60}")
        for num_players in range(2, 7):
            player_key = f'players_{num_players}'
            stats = hand_data[player_key]
            print(f"{num_players:<10} {stats['equity']*100:>9.2f}% {stats['win_rate']*100:>9.2f}% {stats['tie_rate']*100:>9.2f}%")
    else:
        player_key = 'players_6'
        stats = hand_data[player_key]
        print(f"6-Max Table:")
        print(f"  Equity:    {stats['equity']*100:>6.2f}%")
        print(f"  Win Rate:  {stats['win_rate']*100:>6.2f}%")
        print(f"  Tie Rate:  {stats['tie_rate']*100:>6.2f}%")
        print(f"  Loss Rate: {stats['loss_rate']*100:>6.2f}%")

    print()


def top_hands(data, num_players=6, n=20):
    """Show top N hands by equity"""
    hands_data = data['hands']
    player_key = f'players_{num_players}'

    # Get all hands with equity
    hand_equities = [
        (hand, values[player_key]['equity'])
        for hand, values in hands_data.items()
        if player_key in values
    ]

    # Sort by equity
    hand_equities.sort(key=lambda x: x[1], reverse=True)

    print(f"\n{'='*60}")
    print(f"TOP {n} STARTING HANDS - {num_players} Players")
    print(f"{'='*60}\n")

    print(f"{'Rank':<6} {'Hand':<8} {'Equity':>10}")
    print(f"{'-'*60}")

    for i, (hand, equity) in enumerate(hand_equities[:n], 1):
        print(f"{i:<6} {hand:<8} {equity*100:>9.2f}%")

    print()


def suited_vs_offsuit(data, num_players=6):
    """Compare suited vs offsuit for all premium hands"""
    hands_data = data['hands']
    player_key = f'players_{num_players}'

    print(f"\n{'='*60}")
    print(f"SUITED vs OFFSUIT COMPARISON - {num_players} Players")
    print(f"{'='*60}\n")

    print(f"{'Hands':<10} {'Suited':>10} {'Offsuit':>10} {'Advantage':>12}")
    print(f"{'-'*60}")

    # Define hand pairs to compare
    hand_pairs = [
        ('A', 'K'), ('A', 'Q'), ('A', 'J'), ('A', 'T'),
        ('K', 'Q'), ('K', 'J'), ('K', 'T'),
        ('Q', 'J'), ('Q', 'T'),
        ('J', 'T')
    ]

    for rank1, rank2 in hand_pairs:
        suited = f"{rank1}{rank2}s"
        offsuit = f"{rank1}{rank2}o"

        if suited in hands_data and offsuit in hands_data:
            s_equity = hands_data[suited][player_key]['equity'] * 100
            o_equity = hands_data[offsuit][player_key]['equity'] * 100
            diff = s_equity - o_equity

            print(f"{rank1}{rank2:<8} {s_equity:>9.2f}% {o_equity:>9.2f}% {diff:>+11.2f}%")

    print()


def pairs_analysis(data):
    """Show how pocket pairs scale across table sizes"""
    hands_data = data['hands']
    pairs = ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22']

    print(f"\n{'='*60}")
    print(f"POCKET PAIRS - Equity by Table Size")
    print(f"{'='*60}\n")

    print(f"{'Pair':<6} {'HU':>8} {'3-way':>8} {'4-way':>8} {'5-way':>8} {'6-max':>8} {'Drop':>8}")
    print(f"{'-'*60}")

    for pair in pairs:
        if pair in hands_data:
            equities = []
            for num_players in range(2, 7):
                player_key = f'players_{num_players}'
                equity = hands_data[pair][player_key]['equity'] * 100
                equities.append(equity)

            drop = equities[0] - equities[-1]
            print(f"{pair:<6} {equities[0]:>7.2f}% {equities[1]:>7.2f}% {equities[2]:>7.2f}% {equities[3]:>7.2f}% {equities[4]:>7.2f}% {drop:>+7.2f}%")

    print()


def main():
    if len(sys.argv) < 2:
        print("""
Poker Equity Quick Analysis Tool

Usage:
  python quick_analysis.py compare HAND1 HAND2 [PLAYERS]
  python quick_analysis.py detail HAND [--all]
  python quick_analysis.py top [N] [PLAYERS]
  python quick_analysis.py suited [PLAYERS]
  python quick_analysis.py pairs

Examples:
  python quick_analysis.py compare AA KK 6
  python quick_analysis.py detail AKs --all
  python quick_analysis.py top 20 6
  python quick_analysis.py suited 6
  python quick_analysis.py pairs
        """)
        sys.exit(0)

    # Load data
    data = load_data()

    command = sys.argv[1].lower()

    if command == 'compare':
        if len(sys.argv) < 4:
            print("Usage: python quick_analysis.py compare HAND1 HAND2 [PLAYERS]")
            sys.exit(1)
        hand1 = sys.argv[2]
        hand2 = sys.argv[3]
        num_players = int(sys.argv[4]) if len(sys.argv) > 4 else 6
        compare_hands(data, hand1, hand2, num_players)

    elif command == 'detail':
        if len(sys.argv) < 3:
            print("Usage: python quick_analysis.py detail HAND [--all]")
            sys.exit(1)
        hand = sys.argv[2]
        show_all = '--all' in sys.argv
        show_hand_detail(data, hand, show_all)

    elif command == 'top':
        n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 20
        num_players = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        top_hands(data, num_players, n)

    elif command == 'suited':
        num_players = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        suited_vs_offsuit(data, num_players)

    elif command == 'pairs':
        pairs_analysis(data)

    else:
        print(f"❌ Unknown command: {command}")
        print("Try: python quick_analysis.py (with no args for help)")


if __name__ == "__main__":
    main()
