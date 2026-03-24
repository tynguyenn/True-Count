# True-Count

A terminal-based blackjack card counting trainer. Practice Hi-Lo counting, learn basic strategy, and simulate your way to a hot deck.

## Features

- **Full Blackjack Gameplay** - Hit, stand, double down, and split
- **Hi-Lo Card Counting** - Running count and true count displayed in real-time
- **Basic Strategy Engine** - Bot plays perfect basic strategy (based on BJA chart)
- **Betting System** - $10 / $25 / $50 / $100 bet options with $500 starting balance
- **Auto-Play Mode** - Bot plays $10 hands until true count reaches +2
- **Simulation Mode** - Fast-forward through hands without affecting balance
- **Multi-Deck Support** - Configure 1-8 decks (default: 6)

## Installation

```bash
# Clone the repository
cd True-Count

# Run the game
python3 main.py
```

No dependencies required - just Python 3.10+.

## How to Play

### Main Menu

```
[1] Start Game              - Play blackjack manually
[2] Shuffle Deck            - Reset and shuffle the deck
[3] Show Deck               - Peek at card order (for practice)
[4] Settings                - Configure number of decks
[5] Auto-play $10 to TC +2  - Bot plays until count is hot
[6] Simulate to TC +2       - Fast-forward without balance
[q] Quit
```

### During Gameplay

```
[h] Hit
[s] Stand
[d] Double Down (first two cards, if you have the balance)
[p] Split (pairs only, if you have the balance)
```

### Betting Screen

```
[1] $10    [2] $25    [3] $50    [4] $100
[a] Auto-play $10 to TC +2
[s] Simulate to TC +2 (no balance)
[q] Back to menu
```

## Hi-Lo Card Counting

The Hi-Lo system assigns values to cards:

| Cards | Value |
|-------|-------|
| 2-6   | +1    |
| 7-9   | 0     |
| 10-A  | -1    |

- **Running Count (RC)** - Sum of all card values seen
- **True Count (TC)** - Running count ÷ decks remaining

When TC is +2 or higher, the player has an edge. Bet big!

## Basic Strategy

The bot uses the standard basic strategy chart from Blackjack Apprenticeship:

- **Hard Totals** - When to hit, stand, or double
- **Soft Totals** - Hands with Ace counted as 11
- **Pair Splitting** - When to split pairs

## Project Structure

```
True-Count/
├── main.py        # Game loop and UI
├── deck.py        # Card and Deck classes
├── counter.py     # Hi-Lo counting logic
├── strategy.py    # Basic strategy tables
└── images/        # Reference charts
```

## Tips for Practice

1. Start with **Simulate to TC +2** to get to a favorable count quickly
2. When TC hits +2+, take over and bet big ($50-$100)
3. Use **Show Deck** to verify your count is accurate
4. Practice keeping the running count mentally before looking at the display

## License

MIT
