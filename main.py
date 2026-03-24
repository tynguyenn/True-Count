#!/usr/bin/env python3
"""
True-Count: A card counting practice app.
"""

from deck import Deck
from counter import Counter


def display_card(card) -> str:
    """Display a card with a simple ASCII representation."""
    symbols = {'Hearts': 'H', 'Diamonds': 'D', 'Clubs': 'C', 'Spades': 'S'}
    return f"[{card.rank}{symbols[card.suit]}]"


def main():
    print("=" * 40)
    print("  TRUE-COUNT: Card Counting Trainer")
    print("=" * 40)
    print()

    # Get number of decks
    while True:
        try:
            num_decks = int(input("Number of decks (1-8): "))
            if 1 <= num_decks <= 8:
                break
            print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Please enter a valid number.")

    deck = Deck(num_decks)
    counter = Counter(num_decks)

    print(f"\nStarting with {num_decks} deck(s) ({deck.cards_remaining()} cards)")
    print("\nCommands:")
    print("  [Enter] - Deal next card")
    print("  'r'     - Reset deck")
    print("  's'     - Show current count")
    print("  'q'     - Quit")
    print("-" * 40)

    while True:
        command = input("\n> ").strip().lower()

        if command == 'q':
            print("\nThanks for practicing!")
            break

        elif command == 'r':
            deck.reset()
            counter.reset()
            print(f"\nDeck reset. {deck.cards_remaining()} cards remaining.")

        elif command == 's':
            print(f"\n  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print(f"  Cards Seen:    {counter.cards_seen}")
            print(f"  Cards Left:    {deck.cards_remaining()}")

        elif command == '' or command == 'd':
            card = deck.deal()
            if card is None:
                print("\nNo cards remaining! Press 'r' to reset.")
                continue

            value = counter.count_card(card)
            value_str = f"+{value}" if value > 0 else str(value)

            print(f"\n  Card: {display_card(card):8} Value: {value_str}")
            print(f"  Running Count: {counter.get_running_count():+d}  |  True Count: {counter.get_true_count():+.1f}")

        else:
            print("Unknown command. Press Enter to deal, 's' for stats, 'r' to reset, 'q' to quit.")


if __name__ == "__main__":
    main()
