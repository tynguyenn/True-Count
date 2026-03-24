#!/usr/bin/env python3
"""
True-Count: A card counting practice app.
"""

import os
import time
from deck import Deck
from counter import Counter
from strategy import get_basic_strategy_action, calculate_hand_value, get_card_value

STARTING_BALANCE = 500
BET_OPTIONS = {
    '1': 10,
    '2': 25,
    '3': 50,
    '4': 100
}
SIM_BET = 10  # Minimum bet during simulation


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_card(card) -> str:
    """Display a card with suit symbols."""
    symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
    return f"[{card.rank}{symbols[card.suit]}]"


def is_blackjack(hand: list) -> bool:
    """Check if hand is a natural blackjack (21 with 2 cards)."""
    if len(hand) != 2:
        return False
    value, _ = calculate_hand_value(hand)
    return value == 21


def can_split(hand: list) -> bool:
    """Check if hand can be split (two cards of same rank)."""
    if len(hand) != 2:
        return False
    val1 = get_card_value(hand[0])
    val2 = get_card_value(hand[1])
    return val1 == val2


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
    print("  [5] Auto-play $10 to TC +2")
    print("  [6] Simulate to TC +2 (no balance)")
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

    cards = deck.cards.copy()
    cards.reverse()

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


def display_game_state(player_hands: list, current_hand_idx: int, dealer_hand: list,
                       bets: list, hide_dealer: bool, counter: Counter, balance: int):
    """Display the full game state with multiple hands support."""
    print()
    print("  DEALER'S HAND:")
    if hide_dealer and len(dealer_hand) >= 2:
        print(f"    {display_card(dealer_hand[0])}  [??]")
        visible_value = get_card_value(dealer_hand[0])
        print(f"    Showing: {visible_value}")
    else:
        cards_str = "  ".join(display_card(c) for c in dealer_hand)
        print(f"    {cards_str}")
        value, hand_type = calculate_hand_value(dealer_hand)
        print(f"    Value: {value} ({hand_type})")

    print()

    for i, (hand, bet) in enumerate(zip(player_hands, bets)):
        if len(player_hands) > 1:
            marker = " >>>" if i == current_hand_idx else "    "
            print(f"{marker} HAND {i + 1} (${bet}):")
        else:
            print(f"  YOUR HAND (${bet}):")

        cards_str = "  ".join(display_card(c) for c in hand)
        print(f"    {cards_str}")
        value, hand_type = calculate_hand_value(hand)
        print(f"    Value: {value} ({hand_type})")
        print()

    print(f"  Balance: ${balance}  |  RC: {counter.get_running_count():+d}  |  TC: {counter.get_true_count():+.1f}")
    print()


def play_hand(deck: Deck, counter: Counter, hand: list, bet: int, balance: int,
              dealer_hand: list, all_hands: list, hand_idx: int, all_bets: list,
              is_split_hand: bool = False, auto_play: bool = False) -> tuple[list, int, int, list, list]:
    """
    Play a single hand. Returns (final_hand, final_bet, balance, new_hands, new_bets).
    If auto_play is True, uses basic strategy automatically.
    """
    new_hands = []
    new_bets = []
    dealer_upcard = dealer_hand[0]

    while True:
        if not auto_play:
            clear_screen()
            print("=" * 40)
            if len(all_hands) > 1:
                print(f"  PLAYING HAND {hand_idx + 1}      Bet: ${bet}")
            else:
                print(f"  YOUR TURN              Bet: ${bet}")
            print("=" * 40)

            display_game_state(all_hands, hand_idx, dealer_hand, all_bets, True, counter, balance)

        hand_value, _ = calculate_hand_value(hand)

        if hand_value > 21:
            if not auto_play:
                print("  BUST! You went over 21.")
                input("\n  Press Enter to continue...")
            break

        if hand_value == 21:
            if not auto_play:
                print("  21! Standing automatically.")
                input("\n  Press Enter to continue...")
            break

        # Determine available actions
        can_double = len(hand) == 2 and balance >= bet
        can_split_hand = can_split(hand) and balance >= bet and not is_split_hand

        if auto_play:
            # Get basic strategy decision
            action = get_basic_strategy_action(hand, dealer_upcard, can_double, can_split_hand)

            if action == 'P':
                action = 'p'
            elif action == 'D':
                action = 'd'
            elif action == 'H':
                action = 'h'
            else:  # 'S'
                action = 's'
        else:
            print("-" * 40)
            print("  [h] Hit")
            print("  [s] Stand")
            if can_double:
                print("  [d] Double Down")
            if can_split_hand:
                print("  [p] Split")
            print("-" * 40)

            action = input("\n> ").strip().lower()

        if action == 'h':
            card = deck.deal()
            hand.append(card)
            counter.count_card(card)

        elif action == 's':
            break

        elif action == 'd' and can_double:
            balance -= bet
            bet *= 2
            all_bets[hand_idx] = bet

            card = deck.deal()
            hand.append(card)
            counter.count_card(card)

            if not auto_play:
                clear_screen()
                print("=" * 40)
                print(f"  DOUBLE DOWN!           Bet: ${bet}")
                print("=" * 40)

                display_game_state(all_hands, hand_idx, dealer_hand, all_bets, True, counter, balance)

                hand_value, _ = calculate_hand_value(hand)
                if hand_value > 21:
                    print("  BUST!")
                else:
                    print("  Standing after double.")
                input("\n  Press Enter to continue...")
            break

        elif action == 'p' and can_split_hand:
            balance -= bet

            card1 = hand[0]
            card2 = hand[1]

            hand.clear()
            hand.append(card1)
            new_card = deck.deal()
            hand.append(new_card)
            counter.count_card(new_card)

            split_hand = [card2]
            new_card = deck.deal()
            split_hand.append(new_card)
            counter.count_card(new_card)

            new_hands.append(split_hand)
            new_bets.append(bet)

            if not auto_play:
                clear_screen()
                print("=" * 40)
                print("  SPLIT!")
                print("=" * 40)
                print(f"\n  Hand split into two. Playing first hand...")
                input("\n  Press Enter to continue...")

    return hand, bet, balance, new_hands, new_bets


def play_single_hand_sim(deck: Deck, counter: Counter) -> None:
    """Play a single hand in simulation mode (no balance tracking, just counting)."""

    # Deal initial cards
    player_hands = [[]]
    bets = [SIM_BET]
    dealer_hand = []

    card = deck.deal()
    player_hands[0].append(card)
    counter.count_card(card)

    card = deck.deal()
    dealer_hand.append(card)
    counter.count_card(card)

    card = deck.deal()
    player_hands[0].append(card)
    counter.count_card(card)

    dealer_hole_card = deck.deal()
    dealer_hand.append(dealer_hole_card)

    # Check for blackjacks
    player_bj = is_blackjack(player_hands[0])
    dealer_bj = is_blackjack(dealer_hand)

    if player_bj or dealer_bj:
        counter.count_card(dealer_hole_card)
        return

    # Play each hand with basic strategy
    hand_idx = 0
    dummy_balance = 10000  # Unlimited for sim

    while hand_idx < len(player_hands):
        hand, new_bet, dummy_balance, new_hands, new_bets = play_hand(
            deck, counter, player_hands[hand_idx], bets[hand_idx], dummy_balance,
            dealer_hand, player_hands, hand_idx, bets,
            is_split_hand=(len(player_hands) > 1),
            auto_play=True
        )
        player_hands[hand_idx] = hand
        bets[hand_idx] = new_bet

        if new_hands:
            for i, (nh, nb) in enumerate(zip(new_hands, new_bets)):
                player_hands.insert(hand_idx + 1 + i, nh)
                bets.insert(hand_idx + 1 + i, nb)

        hand_idx += 1

    # Reveal dealer's hole card
    counter.count_card(dealer_hole_card)

    # Dealer's turn
    all_busted = all(calculate_hand_value(h)[0] > 21 for h in player_hands)

    if not all_busted:
        while True:
            dealer_value, _ = calculate_hand_value(dealer_hand)
            if dealer_value >= 17:
                break
            card = deck.deal()
            dealer_hand.append(card)
            counter.count_card(card)


def run_simulation(deck: Deck, counter: Counter, target_tc: float = 2.0):
    """Run simulation until true count reaches target."""
    clear_screen()
    print("=" * 40)
    print("  SIMULATION MODE")
    print("=" * 40)
    print()
    print(f"  Target True Count: +{target_tc}")
    print(f"  Bot plays basic strategy until TC >= +{target_tc}")
    print()
    print("  Press Enter to start simulation...")
    print("  Press 'q' to cancel")
    print()

    choice = input("> ").strip().lower()
    if choice == 'q':
        return False

    hands_played = 0
    start_cards = deck.cards_remaining()

    while deck.cards_remaining() > 15:
        # Check if we've reached target
        tc = counter.get_true_count()
        if tc >= target_tc:
            clear_screen()
            print("=" * 40)
            print("  TARGET REACHED!")
            print("=" * 40)
            print()
            print(f"  Hands Played: {hands_played}")
            print(f"  Cards Dealt:  {start_cards - deck.cards_remaining()}")
            print(f"  Cards Left:   {deck.cards_remaining()}")
            print()
            print(f"  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print()
            print("  The count is hot! Time to play.")
            print()
            input("  Press Enter to start playing...")
            return True

        # Play a hand
        play_single_hand_sim(deck, counter)
        hands_played += 1

        # Show progress every 10 hands
        if hands_played % 10 == 0:
            clear_screen()
            print("=" * 40)
            print("  SIMULATING...")
            print("=" * 40)
            print()
            print(f"  Hands Played: {hands_played}")
            print(f"  Cards Left:   {deck.cards_remaining()}")
            print(f"  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print()
            print("  Waiting for TC >= +2.0...")

    # Ran out of cards
    clear_screen()
    print("=" * 40)
    print("  SIMULATION COMPLETE")
    print("=" * 40)
    print()
    print(f"  Hands Played: {hands_played}")
    print(f"  Cards Left:   {deck.cards_remaining()}")
    print()
    print(f"  Final Running Count: {counter.get_running_count():+d}")
    print(f"  Final True Count:    {counter.get_true_count():+.1f}")
    print()
    print("  Deck exhausted before reaching TC +2.")
    print("  This happens! Shuffle and try again.")
    print()
    input("  Press Enter to return to menu...")
    return False


def run_auto_play(deck: Deck, counter: Counter, balance: int, target_tc: float = 2.0) -> tuple[bool, int]:
    """
    Auto-play with $10 bets using basic strategy until TC reaches target.
    Returns (reached_target, new_balance).
    """
    clear_screen()
    print("=" * 40)
    print("  AUTO-PLAY MODE")
    print("=" * 40)
    print()
    print(f"  Balance: ${balance}")
    print(f"  Bet: $10 per hand (basic strategy)")
    print(f"  Target True Count: +{target_tc}")
    print()
    print("  Press Enter to start...")
    print("  Press 'q' to cancel")
    print()

    choice = input("> ").strip().lower()
    if choice == 'q':
        return False, balance

    hands_played = 0
    auto_bet = 10

    while deck.cards_remaining() > 15 and balance >= auto_bet:
        # Check if we've reached target
        tc = counter.get_true_count()
        if tc >= target_tc:
            clear_screen()
            print("=" * 40)
            print("  TARGET REACHED!")
            print("=" * 40)
            print()
            print(f"  Hands Played: {hands_played}")
            print(f"  Balance: ${balance}")
            print(f"  Cards Left: {deck.cards_remaining()}")
            print()
            print(f"  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print()
            print("  The count is hot! Time to bet big.")
            print()
            input("  Press Enter to continue...")
            return True, balance

        # Play a hand with real balance
        balance -= auto_bet

        player_hands = [[]]
        bets = [auto_bet]
        dealer_hand = []

        card = deck.deal()
        player_hands[0].append(card)
        counter.count_card(card)

        card = deck.deal()
        dealer_hand.append(card)
        counter.count_card(card)

        card = deck.deal()
        player_hands[0].append(card)
        counter.count_card(card)

        dealer_hole_card = deck.deal()
        dealer_hand.append(dealer_hole_card)

        # Check for blackjacks
        player_bj = is_blackjack(player_hands[0])
        dealer_bj = is_blackjack(dealer_hand)

        if player_bj or dealer_bj:
            counter.count_card(dealer_hole_card)
            if player_bj and dealer_bj:
                balance += auto_bet  # Push
            elif player_bj:
                balance += auto_bet + int(auto_bet * 1.5)  # BJ pays 3:2
            # Dealer BJ = loss (already deducted)
            hands_played += 1
        else:
            # Play hands with basic strategy
            hand_idx = 0
            dummy_balance = 10000  # For splits/doubles tracking

            while hand_idx < len(player_hands):
                hand, new_bet, dummy_balance, new_hands, new_bets = play_hand(
                    deck, counter, player_hands[hand_idx], bets[hand_idx], dummy_balance,
                    dealer_hand, player_hands, hand_idx, bets,
                    is_split_hand=(len(player_hands) > 1),
                    auto_play=True
                )

                # Track extra money spent on doubles/splits
                extra_spent = new_bet - bets[hand_idx]
                if extra_spent > 0:
                    balance -= extra_spent

                player_hands[hand_idx] = hand
                bets[hand_idx] = new_bet

                if new_hands:
                    for i, (nh, nb) in enumerate(zip(new_hands, new_bets)):
                        player_hands.insert(hand_idx + 1 + i, nh)
                        bets.insert(hand_idx + 1 + i, nb)
                        balance -= nb  # Pay for split hand

                hand_idx += 1

            # Reveal dealer hole card
            counter.count_card(dealer_hole_card)

            # Dealer's turn
            all_busted = all(calculate_hand_value(h)[0] > 21 for h in player_hands)

            if not all_busted:
                while True:
                    dealer_value, _ = calculate_hand_value(dealer_hand)
                    if dealer_value >= 17:
                        break
                    card = deck.deal()
                    dealer_hand.append(card)
                    counter.count_card(card)

            # Calculate results
            dealer_value, _ = calculate_hand_value(dealer_hand)

            for hand, hand_bet in zip(player_hands, bets):
                player_value, _ = calculate_hand_value(hand)

                if player_value > 21:
                    winnings = 0
                elif dealer_value > 21:
                    winnings = hand_bet * 2
                elif player_value > dealer_value:
                    winnings = hand_bet * 2
                elif dealer_value > player_value:
                    winnings = 0
                else:
                    winnings = hand_bet

                balance += winnings

            hands_played += 1

        # Show progress every 5 hands
        if hands_played % 5 == 0:
            clear_screen()
            print("=" * 40)
            print("  AUTO-PLAYING...")
            print("=" * 40)
            print()
            print(f"  Hands Played: {hands_played}")
            print(f"  Balance: ${balance}")
            print(f"  Cards Left: {deck.cards_remaining()}")
            print()
            print(f"  Running Count: {counter.get_running_count():+d}")
            print(f"  True Count:    {counter.get_true_count():+.1f}")
            print()
            print("  Waiting for TC >= +2.0...")

    # Ran out of cards or money
    clear_screen()
    print("=" * 40)
    print("  AUTO-PLAY STOPPED")
    print("=" * 40)
    print()
    print(f"  Hands Played: {hands_played}")
    print(f"  Balance: ${balance}")
    print(f"  Cards Left: {deck.cards_remaining()}")
    print()
    print(f"  Running Count: {counter.get_running_count():+d}")
    print(f"  True Count:    {counter.get_true_count():+.1f}")
    print()

    if balance < auto_bet:
        print("  Out of money!")
    else:
        print("  Deck needs shuffle.")
    print()
    input("  Press Enter to continue...")
    return False, balance


def run_game_with_balance(deck: Deck, counter: Counter, starting_balance: int):
    """Run the blackjack game with a specific starting balance."""
    run_game(deck, counter, starting_balance)


def run_game(deck: Deck, counter: Counter, starting_balance: int = None):
    """Run the blackjack game."""
    balance = starting_balance if starting_balance is not None else STARTING_BALANCE

    while True:
        if deck.cards_remaining() < 15:
            clear_screen()
            print("=" * 40)
            print("  NOT ENOUGH CARDS")
            print("=" * 40)
            print("\n  Please shuffle the deck from the menu.")
            input("\n  Press Enter to return...")
            return

        if balance <= 0:
            clear_screen()
            print("=" * 40)
            print("  GAME OVER")
            print("=" * 40)
            print("\n  You're out of money!")
            print(f"  Final Balance: ${balance}")
            input("\n  Press Enter to return...")
            return

        # Betting screen
        clear_screen()
        print("=" * 40)
        print("  PLACE YOUR BET")
        print("=" * 40)
        print()
        print(f"  Balance: ${balance}")
        print(f"  Cards Remaining: {deck.cards_remaining()}")
        print()
        print(f"  Running Count: {counter.get_running_count():+d}")
        print(f"  True Count:    {counter.get_true_count():+.1f}")
        print()
        print("-" * 40)
        print("  [1] $10")
        print("  [2] $25")
        print("  [3] $50")
        print("  [4] $100")
        print("  [a] Auto-play $10 to TC +2")
        print("  [s] Simulate to TC +2 (no balance)")
        print("  [q] Back to menu")
        print("-" * 40)

        choice = input("\n> ").strip().lower()
        if choice == 'q':
            return

        if choice == 's':
            if not run_simulation(deck, counter):
                return  # Deck exhausted, go back to menu
            continue  # TC reached, show betting screen again

        if choice == 'a':
            result, balance = run_auto_play(deck, counter, balance)
            if not result:
                if balance <= 0:
                    clear_screen()
                    print("=" * 40)
                    print("  GAME OVER")
                    print("=" * 40)
                    print("\n  You're out of money!")
                    input("\n  Press Enter to return...")
                    return
                if deck.cards_remaining() < 15:
                    return  # Deck exhausted, go back to menu
            continue  # TC reached or continue playing

        if choice not in BET_OPTIONS:
            continue

        bet = BET_OPTIONS[choice]
        if bet > balance:
            print(f"\n  Not enough money! You have ${balance}")
            input("  Press Enter to continue...")
            continue

        balance -= bet

        # Deal initial cards
        player_hands = [[]]
        bets = [bet]
        dealer_hand = []

        card = deck.deal()
        player_hands[0].append(card)
        counter.count_card(card)

        card = deck.deal()
        dealer_hand.append(card)
        counter.count_card(card)

        card = deck.deal()
        player_hands[0].append(card)
        counter.count_card(card)

        dealer_hole_card = deck.deal()
        dealer_hand.append(dealer_hole_card)

        # Check for blackjacks
        player_bj = is_blackjack(player_hands[0])
        dealer_bj = is_blackjack(dealer_hand)

        if player_bj or dealer_bj:
            counter.count_card(dealer_hole_card)

            clear_screen()
            print("=" * 40)
            print("  BLACKJACK!")
            print("=" * 40)

            display_game_state(player_hands, 0, dealer_hand, bets, False, counter, balance)

            if player_bj and dealer_bj:
                print("  Both have Blackjack - PUSH!")
                balance += bet
            elif player_bj:
                print("  BLACKJACK! You win 3:2!")
                balance += bet + int(bet * 1.5)
            else:
                print("  Dealer has Blackjack!")

            print(f"\n  Balance: ${balance}")
            input("\n  Press Enter to continue...")
            continue

        # Play each hand
        hand_idx = 0
        while hand_idx < len(player_hands):
            hand, new_bet, balance, new_hands, new_bets = play_hand(
                deck, counter, player_hands[hand_idx], bets[hand_idx], balance,
                dealer_hand, player_hands, hand_idx, bets,
                is_split_hand=(len(player_hands) > 1),
                auto_play=False
            )
            player_hands[hand_idx] = hand
            bets[hand_idx] = new_bet

            if new_hands:
                for i, (nh, nb) in enumerate(zip(new_hands, new_bets)):
                    player_hands.insert(hand_idx + 1 + i, nh)
                    bets.insert(hand_idx + 1 + i, nb)

            hand_idx += 1

        # Reveal dealer's hole card
        counter.count_card(dealer_hole_card)

        # Dealer's turn
        all_busted = all(calculate_hand_value(h)[0] > 21 for h in player_hands)

        if not all_busted:
            while True:
                clear_screen()
                print("=" * 40)
                print("  DEALER'S TURN")
                print("=" * 40)

                display_game_state(player_hands, -1, dealer_hand, bets, False, counter, balance)

                dealer_value, _ = calculate_hand_value(dealer_hand)

                if dealer_value >= 17:
                    if dealer_value > 21:
                        print("  Dealer BUSTS!")
                    else:
                        print(f"  Dealer stands on {dealer_value}.")
                    time.sleep(1)
                    break

                print(f"  Dealer hits...")
                time.sleep(1)

                card = deck.deal()
                dealer_hand.append(card)
                counter.count_card(card)

        # Determine results
        clear_screen()
        print("=" * 40)
        print("  RESULTS")
        print("=" * 40)

        display_game_state(player_hands, -1, dealer_hand, bets, False, counter, balance)

        dealer_value, _ = calculate_hand_value(dealer_hand)
        total_winnings = 0

        print("-" * 40)
        for i, (hand, hand_bet) in enumerate(zip(player_hands, bets)):
            player_value, _ = calculate_hand_value(hand)

            hand_label = f"Hand {i + 1}" if len(player_hands) > 1 else "Result"

            if player_value > 21:
                result = "LOSE (Bust)"
                winnings = 0
            elif dealer_value > 21:
                result = "WIN (Dealer bust)"
                winnings = hand_bet * 2
            elif player_value > dealer_value:
                result = "WIN"
                winnings = hand_bet * 2
            elif dealer_value > player_value:
                result = "LOSE"
                winnings = 0
            else:
                result = "PUSH"
                winnings = hand_bet

            balance += winnings
            net = winnings - hand_bet
            print(f"  {hand_label}: {result} (${'+' if net >= 0 else ''}{net})")
            total_winnings += net

        print("-" * 40)
        print(f"  Net: ${'+' if total_winnings >= 0 else ''}{total_winnings}  |  Balance: ${balance}")

        print("-" * 40)
        print("  [Enter] Next hand")
        print("  [q]     Back to menu")

        choice = input("\n> ").strip().lower()
        if choice == 'q':
            return


def main():
    num_decks = 6
    deck = Deck(num_decks)
    counter = Counter(num_decks)

    while True:
        show_menu()
        print(f"  Current: {num_decks} deck(s), {deck.cards_remaining()} cards")
        print(f"  RC: {counter.get_running_count():+d}  |  TC: {counter.get_true_count():+.1f}")
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

        elif choice == '5':
            # Auto-play with $10 bets, then start game if target reached
            result, balance = run_auto_play(deck, counter, STARTING_BALANCE)
            if result:
                run_game_with_balance(deck, counter, balance)

        elif choice == '6':
            # Run simulation (no balance), then start game if target reached
            if run_simulation(deck, counter):
                run_game(deck, counter)


if __name__ == "__main__":
    main()
