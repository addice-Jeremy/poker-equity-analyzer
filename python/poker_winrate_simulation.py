import random
from collections import Counter
from itertools import combinations

# Card values: 2-14 (where 11=J, 12=Q, 13=K, 14=A)
# Suits: 0-3 (clubs, diamonds, hearts, spades)

def create_deck():
    """Create a standard 52-card deck"""
    return [(rank, suit) for rank in range(2, 15) for suit in range(4)]

def evaluate_hand(cards):
    """
    Evaluate a 5-card poker hand and return a score tuple for comparison.
    Higher tuple = better hand
    """
    ranks = sorted([c[0] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = False

    # Check for straight
    if len(rank_counts) == 5:
        if ranks[0] - ranks[4] == 4:
            is_straight = True
        # Check for A-2-3-4-5 straight (wheel)
        elif ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            ranks = [5, 4, 3, 2, 1]  # Ace is low in this case

    # Straight flush
    if is_straight and is_flush:
        return (8, ranks[0])

    # Four of a kind
    if counts == [4, 1]:
        four_kind = [r for r, c in rank_counts.items() if c == 4][0]
        kicker = [r for r, c in rank_counts.items() if c == 1][0]
        return (7, four_kind, kicker)

    # Full house
    if counts == [3, 2]:
        three_kind = [r for r, c in rank_counts.items() if c == 3][0]
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        return (6, three_kind, pair)

    # Flush
    if is_flush:
        return (5, *ranks)

    # Straight
    if is_straight:
        return (4, ranks[0])

    # Three of a kind
    if counts == [3, 1, 1]:
        three_kind = [r for r, c in rank_counts.items() if c == 3][0]
        kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
        return (3, three_kind, *kickers)

    # Two pair
    if counts == [2, 2, 1]:
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
        kicker = [r for r, c in rank_counts.items() if c == 1][0]
        return (2, pairs[0], pairs[1], kicker)

    # One pair
    if counts == [2, 1, 1, 1]:
        pair = [r for r, c in rank_counts.items() if c == 2][0]
        kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
        return (1, pair, *kickers)

    # High card
    return (0, *ranks)

def get_best_hand(hole_cards, community_cards):
    """Find the best 5-card hand from 7 cards"""
    all_cards = hole_cards + community_cards
    best_hand = None

    for five_cards in combinations(all_cards, 5):
        hand_value = evaluate_hand(five_cards)
        if best_hand is None or hand_value > best_hand:
            best_hand = hand_value

    return best_hand

def simulate_hand(hero_cards, num_opponents, num_simulations=10000):
    """
    Simulate poker hands and calculate win rate

    Args:
        hero_cards: List of 2 cards (tuples) for the hero
        num_opponents: Number of opponents (5 for 6-player, 7 for 8-player)
        num_simulations: Number of Monte Carlo simulations to run

    Returns:
        dict with keys: win_rate, tie_rate, loss_rate, equity
    """
    wins = 0
    ties = 0
    losses = 0

    # Pre-create base deck for efficiency
    base_deck = create_deck()

    for _ in range(num_simulations):
        # Create deck copy and remove hero cards efficiently
        deck = [card for card in base_deck if card not in hero_cards]

        # Shuffle and deal
        random.shuffle(deck)

        # Deal opponent hands
        opponent_hands = []
        for i in range(num_opponents):
            opponent_hands.append([deck[i*2], deck[i*2+1]])

        # Deal community cards (flop, turn, river)
        community_start = num_opponents * 2
        community_cards = deck[community_start:community_start+5]

        # Evaluate all hands
        hero_best = get_best_hand(hero_cards, community_cards)
        opponent_bests = [get_best_hand(opp_hand, community_cards) for opp_hand in opponent_hands]

        # Compare
        max_opponent = max(opponent_bests)

        if hero_best > max_opponent:
            wins += 1
        elif hero_best == max_opponent:
            ties += 1
        else:
            losses += 1

    win_rate = wins / num_simulations
    tie_rate = ties / num_simulations
    loss_rate = losses / num_simulations
    equity = win_rate + (tie_rate / 2)

    return {
        'win_rate': win_rate,
        'tie_rate': tie_rate,
        'loss_rate': loss_rate,
        'equity': equity
    }

def card_to_string(card):
    """Convert card tuple to readable string"""
    rank_names = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    suit_names = {0: '♣', 1: '♦', 2: '♥', 3: '♠'}

    rank = rank_names.get(card[0], str(card[0]))
    suit = suit_names[card[1]]
    return f"{rank}{suit}"

def parse_card(card_str):
    """Parse card string like 'AH' or 'Ah' to card tuple"""
    rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    suit_map = {'C': 0, 'D': 1, 'H': 2, 'S': 3}

    rank = rank_map[card_str[0].upper()]
    suit = suit_map[card_str[1].upper()]
    return (rank, suit)

def generate_all_starting_hands():
    """
    Generate all 169 canonical starting hands in poker notation.

    Returns:
        List of hand strings: ['AA', 'AKs', 'AKo', 'AQs', 'AQo', ...]
    """
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    hands = []

    # Pocket pairs
    for rank in ranks:
        hands.append(rank + rank)

    # Suited and offsuit combinations
    for i, rank1 in enumerate(ranks):
        for rank2 in ranks[i+1:]:
            hands.append(rank1 + rank2 + 's')  # Suited
            hands.append(rank1 + rank2 + 'o')  # Offsuit

    return hands

def parse_hand_string(hand_str):
    """
    Parse hand string like 'AKs', 'AKo', or 'AA' into card tuples.

    Args:
        hand_str: String like 'AKs', 'AKo', 'AA', etc.

    Returns:
        List of 2 card tuples representing the hand
    """
    rank_map = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
                '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    rank1 = rank_map[hand_str[0]]
    rank2 = rank_map[hand_str[1]]

    # Pocket pair
    if rank1 == rank2:
        return [(rank1, 0), (rank2, 1)]

    # Suited
    if len(hand_str) == 3 and hand_str[2] == 's':
        return [(rank1, 0), (rank2, 0)]

    # Offsuit
    if len(hand_str) == 3 and hand_str[2] == 'o':
        return [(rank1, 0), (rank2, 1)]

    # Default to offsuit if no suffix
    return [(rank1, 0), (rank2, 1)]

def hand_string_to_display(hand_str):
    """Convert hand string like 'AKs' to display format like 'A♠K♠'"""
    rank1 = hand_str[0]
    rank2 = hand_str[1]

    if len(hand_str) == 2:  # Pocket pair
        return f"{rank1}{rank2}"
    elif hand_str[2] == 's':  # Suited
        return f"{rank1}{rank2}s"
    else:  # Offsuit
        return f"{rank1}{rank2}o"

# Example usage and CLI
if __name__ == "__main__":
    import sys

    # Command-line interface
    if len(sys.argv) > 1:
        hand_str = sys.argv[1]
        num_players = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        num_sims = int(sys.argv[3]) if len(sys.argv) > 3 else 50000

        hero_cards = parse_hand_string(hand_str)
        num_opponents = num_players - 1

        print(f"Simulating {hand_str} at {num_players}-player table ({num_sims:,} simulations)...")
        results = simulate_hand(hero_cards, num_opponents, num_sims)

        print(f"\nResults for {hand_str}:")
        print(f"  Equity:    {results['equity']*100:.2f}%")
        print(f"  Win rate:  {results['win_rate']*100:.2f}%")
        print(f"  Tie rate:  {results['tie_rate']*100:.2f}%")
        print(f"  Loss rate: {results['loss_rate']*100:.2f}%")

    else:
        # Default examples
        print("=== Pocket Aces (AA) ===")
        hero_cards = [(14, 0), (14, 1)]  # A♣ A♦
        print(f"Hero hand: {card_to_string(hero_cards[0])} {card_to_string(hero_cards[1])}")

        print("\nHeads-up (2 players):")
        results = simulate_hand(hero_cards, num_opponents=1, num_simulations=10000)
        print(f"Equity: {results['equity']*100:.2f}%  |  Win: {results['win_rate']*100:.2f}%  |  Tie: {results['tie_rate']*100:.2f}%")

        print("\n6-player table:")
        results = simulate_hand(hero_cards, num_opponents=5, num_simulations=10000)
        print(f"Equity: {results['equity']*100:.2f}%  |  Win: {results['win_rate']*100:.2f}%  |  Tie: {results['tie_rate']*100:.2f}%")

        # Test with AK suited
        print("\n\n=== Ace-King Suited (AKs) ===")
        hero_cards = [(14, 2), (13, 2)]  # A♥ K♥
        print(f"Hero hand: {card_to_string(hero_cards[0])} {card_to_string(hero_cards[1])}")

        print("\nHeads-up (2 players):")
        results = simulate_hand(hero_cards, num_opponents=1, num_simulations=10000)
        print(f"Equity: {results['equity']*100:.2f}%  |  Win: {results['win_rate']*100:.2f}%  |  Tie: {results['tie_rate']*100:.2f}%")

        print("\n6-player table:")
        results = simulate_hand(hero_cards, num_opponents=5, num_simulations=10000)
        print(f"Equity: {results['equity']*100:.2f}%  |  Win: {results['win_rate']*100:.2f}%  |  Tie: {results['tie_rate']*100:.2f}%")

        print("\n\nUsage: python poker_winrate_simulation.py [HAND] [PLAYERS] [SIMULATIONS]")
        print("Example: python poker_winrate_simulation.py AKs 6 50000")