from deck import Card

# Hi-Lo counting system values
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,  # Low cards: +1
    '7': 0, '8': 0, '9': 0,                   # Neutral: 0
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1  # High cards: -1
}


class Counter:
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_seen = 0

    def reset(self) -> None:
        """Reset the count."""
        self.running_count = 0
        self.cards_seen = 0

    def count_card(self, card: Card) -> int:
        """Count a card and return its Hi-Lo value."""
        value = HI_LO_VALUES[card.rank]
        self.running_count += value
        self.cards_seen += 1
        return value

    def get_running_count(self) -> int:
        """Get the current running count."""
        return self.running_count

    def get_true_count(self) -> float:
        """Calculate the true count (running count / decks remaining)."""
        decks_remaining = self.num_decks - (self.cards_seen / 52)
        if decks_remaining <= 0:
            return 0
        return self.running_count / decks_remaining

    def get_card_value(self, card: Card) -> int:
        """Get the Hi-Lo value for a card without counting it."""
        return HI_LO_VALUES[card.rank]
