"""
Basic Strategy for Blackjack based on BJA chart.
"""

from deck import Card


def get_card_value(card: Card) -> int:
    """Get blackjack value of a card."""
    if card.rank in ['J', 'Q', 'K']:
        return 10
    elif card.rank == 'A':
        return 11
    else:
        return int(card.rank)


def calculate_hand_value(hand: list[Card]) -> tuple[int, str]:
    """Calculate hand value, returns (value, 'hard'/'soft')."""
    value = 0
    aces = 0

    for card in hand:
        if card.rank == 'A':
            aces += 1
            value += 11
        elif card.rank in ['J', 'Q', 'K']:
            value += 10
        else:
            value += int(card.rank)

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    hand_type = 'soft' if aces > 0 and value <= 21 else 'hard'
    return value, hand_type


def is_pair(hand: list[Card]) -> bool:
    """Check if hand is a pair."""
    if len(hand) != 2:
        return False
    val1 = get_card_value(hand[0])
    val2 = get_card_value(hand[1])
    return val1 == val2


def get_pair_value(hand: list[Card]) -> int:
    """Get the value of the pair (for strategy lookup)."""
    return get_card_value(hand[0])


# Pair Splitting Strategy
# Key: (pair_value, dealer_upcard) -> 'Y' (split), 'N' (don't split), 'Y/N' (split if DAS)
PAIR_STRATEGY = {
    # Aces - always split
    (11, 2): 'Y', (11, 3): 'Y', (11, 4): 'Y', (11, 5): 'Y', (11, 6): 'Y',
    (11, 7): 'Y', (11, 8): 'Y', (11, 9): 'Y', (11, 10): 'Y', (11, 11): 'Y',
    # 10s - never split
    (10, 2): 'N', (10, 3): 'N', (10, 4): 'N', (10, 5): 'N', (10, 6): 'N',
    (10, 7): 'N', (10, 8): 'N', (10, 9): 'N', (10, 10): 'N', (10, 11): 'N',
    # 9s
    (9, 2): 'Y', (9, 3): 'Y', (9, 4): 'Y', (9, 5): 'Y', (9, 6): 'Y',
    (9, 7): 'N', (9, 8): 'Y', (9, 9): 'Y', (9, 10): 'N', (9, 11): 'N',
    # 8s - always split
    (8, 2): 'Y', (8, 3): 'Y', (8, 4): 'Y', (8, 5): 'Y', (8, 6): 'Y',
    (8, 7): 'Y', (8, 8): 'Y', (8, 9): 'Y', (8, 10): 'Y', (8, 11): 'Y',
    # 7s
    (7, 2): 'Y', (7, 3): 'Y', (7, 4): 'Y', (7, 5): 'Y', (7, 6): 'Y',
    (7, 7): 'Y', (7, 8): 'N', (7, 9): 'N', (7, 10): 'N', (7, 11): 'N',
    # 6s
    (6, 2): 'Y/N', (6, 3): 'Y', (6, 4): 'Y', (6, 5): 'Y', (6, 6): 'Y',
    (6, 7): 'N', (6, 8): 'N', (6, 9): 'N', (6, 10): 'N', (6, 11): 'N',
    # 5s - never split (double instead)
    (5, 2): 'N', (5, 3): 'N', (5, 4): 'N', (5, 5): 'N', (5, 6): 'N',
    (5, 7): 'N', (5, 8): 'N', (5, 9): 'N', (5, 10): 'N', (5, 11): 'N',
    # 4s
    (4, 2): 'N', (4, 3): 'N', (4, 4): 'N', (4, 5): 'Y/N', (4, 6): 'Y/N',
    (4, 7): 'N', (4, 8): 'N', (4, 9): 'N', (4, 10): 'N', (4, 11): 'N',
    # 3s
    (3, 2): 'Y/N', (3, 3): 'Y/N', (3, 4): 'Y', (3, 5): 'Y', (3, 6): 'Y',
    (3, 7): 'Y', (3, 8): 'N', (3, 9): 'N', (3, 10): 'N', (3, 11): 'N',
    # 2s
    (2, 2): 'Y/N', (2, 3): 'Y/N', (2, 4): 'Y', (2, 5): 'Y', (2, 6): 'Y',
    (2, 7): 'Y', (2, 8): 'N', (2, 9): 'N', (2, 10): 'N', (2, 11): 'N',
}

# Soft Totals Strategy
# Key: (soft_total, dealer_upcard) -> 'H', 'S', 'D', 'Ds'
SOFT_STRATEGY = {
    # A,9 (soft 20) - always stand
    (20, 2): 'S', (20, 3): 'S', (20, 4): 'S', (20, 5): 'S', (20, 6): 'S',
    (20, 7): 'S', (20, 8): 'S', (20, 9): 'S', (20, 10): 'S', (20, 11): 'S',
    # A,8 (soft 19)
    (19, 2): 'S', (19, 3): 'S', (19, 4): 'S', (19, 5): 'S', (19, 6): 'Ds',
    (19, 7): 'S', (19, 8): 'S', (19, 9): 'S', (19, 10): 'S', (19, 11): 'S',
    # A,7 (soft 18)
    (18, 2): 'Ds', (18, 3): 'Ds', (18, 4): 'Ds', (18, 5): 'Ds', (18, 6): 'Ds',
    (18, 7): 'S', (18, 8): 'S', (18, 9): 'H', (18, 10): 'H', (18, 11): 'H',
    # A,6 (soft 17)
    (17, 2): 'H', (17, 3): 'D', (17, 4): 'D', (17, 5): 'D', (17, 6): 'D',
    (17, 7): 'H', (17, 8): 'H', (17, 9): 'H', (17, 10): 'H', (17, 11): 'H',
    # A,5 (soft 16)
    (16, 2): 'H', (16, 3): 'H', (16, 4): 'D', (16, 5): 'D', (16, 6): 'D',
    (16, 7): 'H', (16, 8): 'H', (16, 9): 'H', (16, 10): 'H', (16, 11): 'H',
    # A,4 (soft 15)
    (15, 2): 'H', (15, 3): 'H', (15, 4): 'D', (15, 5): 'D', (15, 6): 'D',
    (15, 7): 'H', (15, 8): 'H', (15, 9): 'H', (15, 10): 'H', (15, 11): 'H',
    # A,3 (soft 14)
    (14, 2): 'H', (14, 3): 'H', (14, 4): 'H', (14, 5): 'D', (14, 6): 'D',
    (14, 7): 'H', (14, 8): 'H', (14, 9): 'H', (14, 10): 'H', (14, 11): 'H',
    # A,2 (soft 13)
    (13, 2): 'H', (13, 3): 'H', (13, 4): 'H', (13, 5): 'D', (13, 6): 'D',
    (13, 7): 'H', (13, 8): 'H', (13, 9): 'H', (13, 10): 'H', (13, 11): 'H',
}

# Hard Totals Strategy
# Key: (hard_total, dealer_upcard) -> 'H', 'S', 'D'
HARD_STRATEGY = {
    # 17+ - always stand
    (17, 2): 'S', (17, 3): 'S', (17, 4): 'S', (17, 5): 'S', (17, 6): 'S',
    (17, 7): 'S', (17, 8): 'S', (17, 9): 'S', (17, 10): 'S', (17, 11): 'S',
    # 16
    (16, 2): 'S', (16, 3): 'S', (16, 4): 'S', (16, 5): 'S', (16, 6): 'S',
    (16, 7): 'H', (16, 8): 'H', (16, 9): 'H', (16, 10): 'H', (16, 11): 'H',
    # 15
    (15, 2): 'S', (15, 3): 'S', (15, 4): 'S', (15, 5): 'S', (15, 6): 'S',
    (15, 7): 'H', (15, 8): 'H', (15, 9): 'H', (15, 10): 'H', (15, 11): 'H',
    # 14
    (14, 2): 'S', (14, 3): 'S', (14, 4): 'S', (14, 5): 'S', (14, 6): 'S',
    (14, 7): 'H', (14, 8): 'H', (14, 9): 'H', (14, 10): 'H', (14, 11): 'H',
    # 13
    (13, 2): 'S', (13, 3): 'S', (13, 4): 'S', (13, 5): 'S', (13, 6): 'S',
    (13, 7): 'H', (13, 8): 'H', (13, 9): 'H', (13, 10): 'H', (13, 11): 'H',
    # 12
    (12, 2): 'H', (12, 3): 'H', (12, 4): 'S', (12, 5): 'S', (12, 6): 'S',
    (12, 7): 'H', (12, 8): 'H', (12, 9): 'H', (12, 10): 'H', (12, 11): 'H',
    # 11 - always double
    (11, 2): 'D', (11, 3): 'D', (11, 4): 'D', (11, 5): 'D', (11, 6): 'D',
    (11, 7): 'D', (11, 8): 'D', (11, 9): 'D', (11, 10): 'D', (11, 11): 'D',
    # 10
    (10, 2): 'D', (10, 3): 'D', (10, 4): 'D', (10, 5): 'D', (10, 6): 'D',
    (10, 7): 'D', (10, 8): 'D', (10, 9): 'D', (10, 10): 'H', (10, 11): 'H',
    # 9
    (9, 2): 'H', (9, 3): 'D', (9, 4): 'D', (9, 5): 'D', (9, 6): 'D',
    (9, 7): 'H', (9, 8): 'H', (9, 9): 'H', (9, 10): 'H', (9, 11): 'H',
    # 8 and below - always hit
    (8, 2): 'H', (8, 3): 'H', (8, 4): 'H', (8, 5): 'H', (8, 6): 'H',
    (8, 7): 'H', (8, 8): 'H', (8, 9): 'H', (8, 10): 'H', (8, 11): 'H',
}


def get_basic_strategy_action(hand: list[Card], dealer_upcard: Card,
                               can_double: bool = True, can_split: bool = True) -> str:
    """
    Get the basic strategy action for a hand.

    Returns: 'H' (hit), 'S' (stand), 'D' (double), 'P' (split)
    """
    dealer_val = get_card_value(dealer_upcard)
    hand_value, hand_type = calculate_hand_value(hand)

    # Check for pair splitting first
    if can_split and is_pair(hand):
        pair_val = get_pair_value(hand)
        decision = PAIR_STRATEGY.get((pair_val, dealer_val), 'N')

        # Y/N means split if Double After Split allowed - we'll assume DAS is allowed
        if decision == 'Y' or decision == 'Y/N':
            return 'P'

    # Check soft totals
    if hand_type == 'soft' and hand_value <= 20:
        decision = SOFT_STRATEGY.get((hand_value, dealer_val), 'S')

        if decision == 'D':
            return 'D' if can_double else 'H'
        elif decision == 'Ds':
            return 'D' if can_double else 'S'
        else:
            return decision

    # Hard totals
    # Cap at 17 for lookup (17+ all stand)
    lookup_val = min(hand_value, 17)
    # Floor at 8 for lookup (8 and below all hit)
    lookup_val = max(lookup_val, 8)

    decision = HARD_STRATEGY.get((lookup_val, dealer_val), 'H')

    if decision == 'D':
        return 'D' if can_double else 'H'

    return decision
