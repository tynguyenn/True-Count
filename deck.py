import random

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        return f"Card('{self.rank}', '{self.suit}')"


class Deck:
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self.cards: list[Card] = []
        self.reset()

    def reset(self) -> None:
        """Reset and shuffle the deck(s)."""
        self.cards = [
            Card(rank, suit)
            for _ in range(self.num_decks)
            for suit in SUITS
            for rank in RANKS
        ]
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self) -> Card | None:
        """Deal a single card from the deck."""
        if self.cards:
            return self.cards.pop()
        return None

    def cards_remaining(self) -> int:
        """Return the number of cards remaining."""
        return len(self.cards)

    def decks_remaining(self) -> float:
        """Return approximate number of decks remaining."""
        return len(self.cards) / 52
