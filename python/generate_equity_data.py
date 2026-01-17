#!/usr/bin/env python3
"""
Generate equity data for all 169 poker starting hands.
Simulates from heads-up (2 players) to 6-max (6 players).
Results are cached to equity_cache.json for fast subsequent runs.
"""

import json
import os
import sys
from datetime import datetime
from multiprocessing import Pool, cpu_count
from poker_winrate_simulation import (
    generate_all_starting_hands,
    parse_hand_string,
    simulate_hand
)

try:
    from tqdm import tqdm
except ImportError:
    print("Installing tqdm for progress bars...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm


def simulate_hand_for_all_table_sizes(hand_str, num_simulations=50000):
    """
    Simulate a single hand across all table sizes (2-6 players).

    Args:
        hand_str: Hand string like 'AA', 'AKs', etc.
        num_simulations: Number of Monte Carlo simulations per table size

    Returns:
        dict: Results for all table sizes
    """
    hand_cards = parse_hand_string(hand_str)
    results = {}

    for num_players in range(2, 7):  # 2 to 6 players
        num_opponents = num_players - 1
        sim_results = simulate_hand(hand_cards, num_opponents, num_simulations)

        results[f"players_{num_players}"] = {
            "equity": round(sim_results['equity'], 4),
            "win_rate": round(sim_results['win_rate'], 4),
            "tie_rate": round(sim_results['tie_rate'], 4),
            "loss_rate": round(sim_results['loss_rate'], 4)
        }

    return hand_str, results


def simulate_single_hand_wrapper(args):
    """Wrapper for multiprocessing to unpack arguments"""
    hand_str, num_simulations = args
    return simulate_hand_for_all_table_sizes(hand_str, num_simulations)


def load_cache(cache_file='equity_cache.json'):
    """Load existing cache if available"""
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None


def save_cache(data, cache_file='equity_cache.json'):
    """Save data to cache file"""
    with open(cache_file, 'w') as f:
        json.dump(data, f, indent=2)


def generate_equity_data(num_simulations=50000, force=False, cache_file='equity_cache.json', use_parallel=True):
    """
    Generate equity data for all 169 starting hands.

    Args:
        num_simulations: Number of simulations per hand per table size
        force: If True, regenerate all data even if cache exists
        cache_file: Path to cache file
        use_parallel: If True, use multiprocessing for faster generation
    """
    # Check cache
    if not force:
        cached_data = load_cache(cache_file)
        if cached_data and cached_data.get('metadata', {}).get('num_simulations') == num_simulations:
            print(f"✓ Using cached data from {cache_file}")
            print(f"  Generated: {cached_data['metadata']['generated_at']}")
            print(f"  Simulations per hand: {cached_data['metadata']['num_simulations']:,}")
            print(f"  Total hands: {len(cached_data['hands'])}")
            return cached_data
        elif cached_data:
            print(f"⚠ Cache exists but with different simulation count")
            print(f"  Cached: {cached_data['metadata']['num_simulations']:,} sims")
            print(f"  Requested: {num_simulations:,} sims")
            print(f"  Regenerating data...")

    # Generate all starting hands
    all_hands = generate_all_starting_hands()
    print(f"\n🃏 Generating equity data for {len(all_hands)} hands")
    print(f"   Table sizes: 2-6 players")
    print(f"   Simulations per hand per table size: {num_simulations:,}")
    print(f"   Total simulations: {len(all_hands) * 5 * num_simulations:,}")

    if use_parallel:
        num_processes = max(1, cpu_count() - 1)  # Leave one CPU free
        print(f"   Using {num_processes} parallel processes\n")

        # Prepare arguments for parallel processing
        args = [(hand, num_simulations) for hand in all_hands]

        # Run simulations in parallel with progress bar
        equity_data = {}
        with Pool(num_processes) as pool:
            results = list(tqdm(
                pool.imap(simulate_single_hand_wrapper, args),
                total=len(all_hands),
                desc="Simulating hands",
                unit="hand"
            ))

        # Convert results to dict
        for hand_str, hand_results in results:
            equity_data[hand_str] = hand_results
    else:
        print("   Running sequentially (use_parallel=False)\n")
        equity_data = {}
        for hand_str in tqdm(all_hands, desc="Simulating hands", unit="hand"):
            _, hand_results = simulate_hand_for_all_table_sizes(hand_str, num_simulations)
            equity_data[hand_str] = hand_results

    # Prepare final data structure with metadata
    final_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "num_simulations": num_simulations,
            "num_hands": len(all_hands),
            "table_sizes": [2, 3, 4, 5, 6],
            "version": "1.0"
        },
        "hands": equity_data
    }

    # Save to cache
    save_cache(final_data, cache_file)
    print(f"\n✓ Data generated and saved to {cache_file}")

    return final_data


def print_summary_stats(data):
    """Print summary statistics from the equity data"""
    hands_data = data['hands']

    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)

    # Top 10 hands for heads-up
    print("\nTop 10 Hands (Heads-up Equity):")
    hu_equities = [(hand, values['players_2']['equity']) for hand, values in hands_data.items()]
    hu_equities.sort(key=lambda x: x[1], reverse=True)

    for i, (hand, equity) in enumerate(hu_equities[:10], 1):
        print(f"  {i:2d}. {hand:4s}  {equity*100:5.2f}%")

    # Top 10 hands for 6-max
    print("\nTop 10 Hands (6-Player Equity):")
    six_max_equities = [(hand, values['players_6']['equity']) for hand, values in hands_data.items()]
    six_max_equities.sort(key=lambda x: x[1], reverse=True)

    for i, (hand, equity) in enumerate(six_max_equities[:10], 1):
        print(f"  {i:2d}. {hand:4s}  {equity*100:5.2f}%")

    # Compare AA equity across table sizes
    print("\nPocket Aces (AA) Equity by Table Size:")
    aa_data = hands_data['AA']
    for players in range(2, 7):
        equity = aa_data[f'players_{players}']['equity']
        print(f"  {players} players: {equity*100:5.2f}%")

    # Suited vs Offsuit premium hands
    print("\nSuited vs Offsuit (AK, AQ, KQ):")
    for rank1, rank2 in [('A', 'K'), ('A', 'Q'), ('K', 'Q')]:
        suited = hands_data[f'{rank1}{rank2}s']['players_6']['equity']
        offsuit = hands_data[f'{rank1}{rank2}o']['players_6']['equity']
        diff = (suited - offsuit) * 100
        print(f"  {rank1}{rank2}s: {suited*100:5.2f}%  |  {rank1}{rank2}o: {offsuit*100:5.2f}%  |  Δ: {diff:+.2f}%")

    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate poker equity data for all 169 starting hands"
    )
    parser.add_argument(
        '--sims', '-s',
        type=int,
        default=50000,
        help='Number of simulations per hand per table size (default: 50000)'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force regeneration even if cache exists'
    )
    parser.add_argument(
        '--cache', '-c',
        type=str,
        default='equity_cache.json',
        help='Cache file path (default: equity_cache.json)'
    )
    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel processing (slower but uses less memory)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print summary statistics after generation'
    )

    args = parser.parse_args()

    # Generate or load data
    data = generate_equity_data(
        num_simulations=args.sims,
        force=args.force,
        cache_file=args.cache,
        use_parallel=not args.no_parallel
    )

    # Print summary if requested
    if args.summary or args.force:
        print_summary_stats(data)

    print(f"\n✓ Ready! Use visualize_equity.py to view interactive charts")
