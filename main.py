#!/usr/bin/env python3
"""
True-Count: A card counting practice app.
"""

import os
from deck import Deck
from counter import Counter


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_card(card) -> str:
    """Display a card with a simple ASCII representation."""
    symbols = {'Hearts': 'H', 'Diamonds': 'D', 'Clubs': 'C', 'Spades': 'S'}
    return f"[{card.rank}{symbols[card.suit]}]"


def get_card_value(card) -> int:
    """Get blackjack value of a card."""
    if card.rank in ['J', 'Q', 'K']:
        return 10
    elif card.rank == 'A':
        return 11  # Will handle soft/hard later
    else:
        return int(card.rank)


def calculate_hand_value(hand: list) -> tuple[int, str]:
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

    # Convert aces from 11 to 1 if busting
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    hand_type = 'soft' if aces > 0 and value <= 21 else 'hard'
    return value, hand_type


def show_menu():
    """Display the main menu."""
    clear_screen()
    print("=" * 40)
    print("  TRUE-COUNT: Card Counting Trainer")
    print("=" * 40)
    print()
    print("  [1] Start Game")
    print("  [2] Shuffle Deck")
    print("  [3] Show Deck (Peek at cards)")
    print("  [4] Settings")
    print("  [q] Quit")
    print()
    print("-" * 40)


def show_deck(deck: Deck):
    """Show all cards in the current deck order."""
    clear_screen()
    print("=" * 40)
    print("  DECK CONTENTS (Top to Bottom)")
    print("=" * 40)
    print()

    # Show cards in rows of 8
    cards = deck.cards.copy()
    cards.reverse()  # Show top card first

    for i, card in enumerate(cards):
        print(f"{display_card(card):10}", end="")
        if (i + 1) % 8 == 0:
            print()

    if len(cards) % 8 != 0:
        print()

    print()
    print(f"Total: {len(cards)} cards")
    print("-" * 40)
    input("\nPress Enter to return to menu...")


def settings_menu(num_decks: int) -> int:
    """Settings menu to configure the game."""
    while True:
        clear_screen()
        print("=" * 40)
        print("  SETTINGS")
        print("=" * 40)
        print()
        print(f"  [1] Number of decks: {num_decks}")
        print("  [b] Back to main menu")
        print()
        print("-" * 40)

        choice = input("\n> ").strip().lower()

        if choice == 'b':
            return num_decks
        elif choice == '1':
            try:
                new_decks = int(input("Enter number of decks (1-8): "))
                if 1 <= new_decks <= 8:
                    num_decks = new_decks
                    print(f"Set to {num_decks} deck(s).")
                else:
                    print("Please enter a number between 1 and 8.")
            except ValueError:
                print("Invalid input.")
            input("Press Enter to continue...")


def display_hands(player_hand: list, dealer_hand: list, hide_dealer: bool = True):
    """Display both hands."""
    print()
    print("  DEALER'S HAND:")
    if hide_dealer and len(dealer_hand) >= 2:
        # Show first card, hide second
        print(f"    {display_card(dealer_hand[0])}  [??]")
        visible_value = get_card_value(dealer_hand[0])
        print(f"    Showing: {visible_value}")
    else:
        # Show all cards
        cards_str = "  ".join(display_card(c) for c in dealer_hand)
        print(f"    {cards_str}")
        value, hand_type = calculate_hand_value(dealer_hand)
        print(f"    Value: {value} ({hand_type})")

    print()
    print("  YOUR HAND:")
    cards_str = "  ".join(display_card(c) for c in player_hand)
    print(f"    {cards_str}")
    value, hand_type = calculate_hand_value(player_hand)
    print(f"    Value: {value} ({hand_type})")
    print()


def run_game(deck: Deck, counter: Counter):
    """Run the blackjack game."""

    while True:
        # Check if enough cards to play
        if deck.cards_remaining() < 10:
            clear_screen()
            print("=" * 40)
            print("  NOT ENOUGH CARDS")
            print("=" * 40)
            print("\n  Please shuffle the deck from the menu.")
            input("\n  Press Enter to return...")
            return

        clear_screen()
        print("=" * 40)
        print("  NEW HAND")
        print("=" * 40)
        print()
        print(f"  Cards Remaining: {deck.cards_remaining()}")
        print(f"  Running Count:   {counter.get_running_count():+d}")
        print(f"  True Count:      {counter.get_true_count():+.1f}")
        print()
        print("-" * 40)
        print("  [Enter] Deal hand")
        print("  [q]     Back to menu")
        print("-" * 40)

        choice = input("\n> ").strip().lower()
        if choice == 'q':
            return

        # Deal initial cards: Player, Dealer, Player, Dealer(hidden)
        player_hand = []
        dealer_hand = []

        # Player first card
        card = deck.deal()
        player_hand.append(card)
        counter.count_card(card)

        # Dealer first card (face up)
        card = deck.deal()
        dealer_hand.append(card)
        counter.count_card(card)

        # Player second card
        card = deck.deal()
        player_hand.append(card)
        counter.count_card(card)

        # Dealer second card (face down - don't count yet)
        dealer_hole_card = deck.deal()
        dealer_hand.append(dealer_hole_card)
        # Note: hole card not counted until revealed

        # Player's turn
        while True:
            clear_screen()
            print("=" * 40)
            print("  YOUR TURN")
            print("=" * 40)

            display_hands(player_hand, dealer_hand, hide_dealer=True)

            print(f"  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print()

            player_value, _ = calculate_hand_value(player_hand)

            if player_value > 21:
                print("  BUST! You went over 21.")
                input("\n  Press Enter to continue...")
                break

            if player_value == 21:
                print("  21! Standing automatically.")
                input("\n  Press Enter to continue...")
                break

            print("-" * 40)
            print("  [h] Hit")
            print("  [s] Stand")
            print("-" * 40)

            action = input("\n> ").strip().lower()

            if action == 'h':
                card = deck.deal()
                player_hand.append(card)
                counter.count_card(card)

            elif action == 's':
                break

        # Reveal dealer's hole card and count it
        counter.count_card(dealer_hole_card)

        # Show result
        clear_screen()
        print("=" * 40)
        print("  HAND COMPLETE")
        print("=" * 40)

        display_hands(player_hand, dealer_hand, hide_dealer=False)

        player_value, _ = calculate_hand_value(player_hand)
        dealer_value, _ = calculate_hand_value(dealer_hand)

        print("-" * 40)

        if player_value > 21:
            print("  Result: DEALER WINS (Player bust)")
        elif dealer_value > 21:
            print("  Result: YOU WIN (Dealer bust)")
        elif player_value > dealer_value:
            print("  Result: YOU WIN")
        elif dealer_value > player_value:
            print("  Result: DEALER WINS")
        else:
            print("  Result: PUSH (Tie)")

        print()
        print(f"  Running Count: {counter.get_running_count():+d}")
        print(f"  True Count:    {counter.get_true_count():+.1f}")
        print("-" * 40)
        print("  [Enter] Next hand")
        print("  [q]     Back to menu")

        choice = input("\n> ").strip().lower()
        if choice == 'q':
            return


def main():
    num_decks = 6  # Default for blackjack
    deck = Deck(num_decks)
    counter = Counter(num_decks)

    while True:
        show_menu()
        print(f"  Current: {num_decks} deck(s), {deck.cards_remaining()} cards")
        print()

        choice = input("> ").strip().lower()

        if choice == 'q':
            clear_screen()
            print("Thanks for practicing!")
            break

        elif choice == '1':
            run_game(deck, counter)

        elif choice == '2':
            deck.reset()
            counter.reset()
            print("\n  Deck shuffled!")
            input("  Press Enter to continue...")

        elif choice == '3':
            show_deck(deck)

        elif choice == '4':
            new_decks = settings_menu(num_decks)
            if new_decks != num_decks:
                num_decks = new_decks
                deck = Deck(num_decks)
                counter = Counter(num_decks)


if __name__ == "__main__":
    main()
