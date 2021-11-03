import random
from words import words
import string

def get_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.lower()

def hangman():
    word = get_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_lowercase)
    used_letters = set()
    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print("You have", lives, "lives left. Letters used: ", " ".join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in word]
        print("Current Word: ", " ".join(word_list))

        user_letter = input("Guess a letter: ").lower()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1
                print("Letter is incorrect.")
        elif user_letter in used_letters:
            print("Letter has been guessed. Please try again.")
        else:
            print("Invalid character. Try again.")

    if lives == 0:
        print("The noose got you. The word was", word)
    else:
        print("You got it! The word was", word)

hangman()
