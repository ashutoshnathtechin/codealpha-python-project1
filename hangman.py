import random

# -------------------------------------------------------------
# Predefined list of 5 words (no external file or API needed)
# -------------------------------------------------------------
WORDS = ["python", "hangman", "computer", "developer", "keyboard"]

# -------------------------------------------------------------
# Visual ASCII stages for the 6 incorrect guesses (text-based)
# -------------------------------------------------------------
HANGMAN_STAGES = [
    """
       ------
       |    |
            |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    =========
    """
]


def play_hangman():
    """Plays a single round of the Hangman game."""
    # 1. Random concept: Select one random word from the predefined list
    secret_word = random.choice(WORDS)
    
    # 2. Lists concept: Keep track of guessed letters
    guessed_letters = []
    
    # Counter for incorrect guesses (limit: 6)
    incorrect_guesses = 0
    max_incorrect_guesses = 6

    print("\n" + "=" * 45)
    print("          WELCOME TO HANGMAN!")
    print("=" * 45)
    print(f"I have chosen a secret word ({len(secret_word)} letters long).")
    print(f"You can make up to {max_incorrect_guesses} incorrect guesses.")

    # 3. While loop concept: Loop until the player wins or runs out of guesses
    while incorrect_guesses < max_incorrect_guesses:
        # Display current visual stage
        print(HANGMAN_STAGES[incorrect_guesses])

        # 4. Strings & Lists concept: Build the word display with revealed letters or underscores
        display_word = []
        for letter in secret_word:
            if letter in guessed_letters:
                display_word.append(letter)
            else:
                display_word.append("_")

        # 5. Strings concept: Format and display game state
        print(f"Word: {' '.join(display_word)}")
        print(f"Incorrect guesses left: {max_incorrect_guesses - incorrect_guesses}")
        
        if guessed_letters:
            print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        else:
            print("Guessed letters: (None yet)")

        # Check win condition: If no underscores remain, player wins
        if "_" not in display_word:
            print("\n" + "*" * 45)
            print("CONGRATULATIONS! You won!")
            print(f"The secret word was: '{secret_word.upper()}'.")
            print("*" * 45)
            return

        # Prompt player for input
        guess = input("\nEnter a letter to guess: ").strip().lower()

        # 6. If-Else concept: Input validation
        if len(guess) != 1 or not guess.isalpha():
            print(">> Invalid input! Please enter exactly one alphabetical letter.")
            continue

        if guess in guessed_letters:
            print(f">> You already guessed '{guess}'. Please try another letter.")
            continue

        # Record valid guess in the list
        guessed_letters.append(guess)

        # 7. If-Else concept: Check whether guess is in the secret word
        if guess in secret_word:
            print(f">> Good guess! '{guess}' is in the secret word.")
        else:
            incorrect_guesses += 1
            print(f">> Incorrect! '{guess}' is not in the secret word.")

    # If the while loop completes without winning, player has used all 6 guesses
    print(HANGMAN_STAGES[incorrect_guesses])
    print("\n" + "!" * 45)
    print("GAME OVER! You ran out of guesses.")
    print(f"The secret word was: '{secret_word.upper()}'. Better luck next time!")
    print("!" * 45)


def main():
    """Main game driver loop allowing replay."""
    while True:
        play_hangman()
        replay = input("\nWould you like to play again? (y/n): ").strip().lower()
        if replay not in ("y", "yes"):
            print("\nThanks for playing! Goodbye!\n")
            break


if __name__ == "__main__":
    main()
