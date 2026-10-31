# Text-Based Hangman Game (Python)

A simple, robust, console-based Hangman game written in Python.

## Features & Scope Compliance

- **Predefined Words**: Uses a fixed list of 5 predefined words without needing external files or APIs.
- **Guess Limit**: Limits incorrect guesses strictly to 6.
- **Pure Console I/O**: Clean text input/output with ASCII gallows stages; no external graphics libraries or audio.
- **Input Validation**: Automatically rejects multi-character inputs, digits, special symbols, and already-guessed letters without penalizing the player.
- **Replay Support**: Offers an interactive prompt to play another round when the game concludes.

## Key Concepts Used

1. **`random`**: Selects a secret word randomly from the predefined list using `random.choice()`.
2. **`while loop`**: Drives the core game turn cycle as well as the replay loop.
3. **`if-else`**: Handles validation, duplicate checks, hit/miss detection, and win/loss conditions.
4. **`strings`**: Handles user input normalization (`.strip()`, `.lower()`, `.isalpha()`) and word formatting (`' '.join()`, f-strings).
5. **`lists`**: Manages the word bank, the visual ASCII stages, the guessed letters history, and the masked word display.

## How to Run

Run the script from your terminal:

```bash
python hangman.py
```
