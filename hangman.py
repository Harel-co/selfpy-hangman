"""
Welcome to Python Hangman!
Created by Harel Cohen
Your goal is to guess a secret word within 6 tries or you lose.
Good luck and have fun!
## there are many comments for each section of the code so make sure to read them ;)
"""

## imports and assets
import random
in_game = True  # Global bool for when the player wins the game
wrong_tries = 1 # Global param for failed tries count
HANGMAN_PHOTOS = {'picture 1': """
x-------x
""", 'picture 2': """
x-------x
|
|
|
|
|
""", 'picture 3': """
x-------x
|       |
|       0
|
|
|
""", 'picture 4': """
x-------x
|       |
|       0
|       |
|
|
""", 'picture 5': """
x-------x
|       |
|       0
|      /|\\
|
|
""", 'picture 6': """
x-------x
|       |
|       0
|      /|\\
|      /
|
""", 'picture 7': """
x-------x
|       |
|       0
|      /|\\
|      / \\
|
"""}
HANGMAN_ASCII_ART = """Welcome to \"Hangman\" By Harel Cohen!
  _    _
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/
"""
MAX_TRIES = 7 # enter max tries count + 1

## Game helper functions - these do the main calculating for the game's requirements and levels
def invalid_input(old_letters):
    """
    Function prints an error message and returns False
    :param old_letters: list of guessed characters from previous rounds/empty list
    :type old_letters: list
    :return: False and prints a message
    """
    print('X, Invalid input.')
    print('Letters you\'ve already guessed: ' + ' -> '.join(sorted(old_letters)))
    return False


def check_input(letter_guessed, old_letters):
    """
    Function checks if the guessed character is a single english letter which is the valid input for a guess
    :param letter_guessed: the character the player guessed this round
    :type letter_guessed: str
    :param old_letters: list of guessed characters from previous rounds/empty list
    :type old_letters: list
    :return: True or False
    """
    if len(letter_guessed) > 1:
        return invalid_input(old_letters)
    elif not (letter_guessed.isalpha()):
        return invalid_input(old_letters)
    elif letter_guessed in old_letters:
        return invalid_input(old_letters)
    old_letters.append(letter_guessed)
    return True


def check_win(final):
    """
    Function checks if the player has won the game
    :param final: the str of the word with unveiled characters that were guessed correctly
    :type final: str
    :return: None - but changes global boolean in_game (True or False)
    """
    global in_game
    if '_' not in final:
        in_game = False # in_game would stop running the game - after a player wins


def show_keyword(secret_word, old_letters_guessed):
    """
    Function receives the keyword of the game and returns str that shows which
    letters were guessed correctly and where they are in the word
    :param secret_word: the keyword that players have to guess
    :type secret_word: str
    :param old_letters_guessed: list of guessed characters from previous rounds/empty list
    :type old_letters_guessed: list
    :return: str
    """
    final = ['_' for _ in range(len(secret_word))]
    counter = 1
    for i in range(len(old_letters_guessed)):
        if old_letters_guessed[i] in secret_word:
            spot = secret_word.find(old_letters_guessed[i])
            final[spot] = old_letters_guessed[i]
            while spot != secret_word.rfind(old_letters_guessed[i]):
                spot = secret_word.find(old_letters_guessed[i], spot+1)
                final[spot] = old_letters_guessed[i]
        else:
            counter += 1
    check_win(' '.join(final)) # can make the .join character a var so when the player wins it'll be 'word' and not 'w o r d'
    global wrong_tries
    wrong_tries = counter
    return ' '.join(final)


def print_hangman(num_of_tries):
    """
    Function prints the current state of the Hangman
    :param num_of_tries: amount of wrong tries already
    :type num_of_tries: int
    :return: None
    """
    print(HANGMAN_PHOTOS['picture ' + str(num_of_tries)])


def choose_word(path, index=-999):
    """
    Function gets a directory path of a file and chooses a single word that would be the keyword for the current game
    :param path: path to .txt file
    :type path: str
    :param index: the index for which word, if = -999 then chooses randomly
    :type index: int
    :return: str
    """
    file = open(path, 'r')
    hang_word = 'bamba' # default word if user fails to enter a custom word
    index = int(index)
    for line in file:
        if index == -999:
            length = len(line.split()) - 1
            index = random.randint(0, length)
        word = line.split()
        while index > len(word): # as said - if its longer than the length of the file, loop it until it reaches a number
            index -= len(word)
        hang_word = word[index]
        break
    file.close()
    return hang_word.lower()


## Function main -> this is where the game runs
def main():
    ## Starting screen
    print(HANGMAN_ASCII_ART, '\nMax Tries:', MAX_TRIES - 1)

    ## Game menu/Choose Word
    game_keyword = 'bamba' # default word if user fails to enter a custom word
    index = -999
    custom_word = False
    path = r'./Hangman-words.txt' ###### Make sure the path of Hangman-words.txt file i included is in the same folder or else it wont work
    if not 'y' == input('Would you like to use the default word list for the game (y), (or use your own.. (n)) y/n: ').lower():
        if 'y' == input('Would you like to give us your word list (.txt file) (y) or just type in a custom word (n)? y/n: ').lower():
            path = input('Enter the path to your txt file: ')
        else:
            game_keyword = input('Please enter a word for players to guess: ')
            custom_word = True
            while not game_keyword.isalpha() or (' ' in game_keyword):
                print('You have to enter a single word only using english letters!')
                game_keyword = input('Please re-enter word: ')

    if not custom_word:
        if not 'y' == input('Would you want the word to be a randomly chosen from the list (y) or to pick a specific index of a word in the list (n)? y/n: ').lower():
            index = input('Enter index: ')
        game_keyword = choose_word(path, index)

    ## before starting the game
    print_hangman(wrong_tries)
    print('_ ' * len(game_keyword))
    print()
    old_chars = []

    ## Main Game loop
    while in_game and wrong_tries < MAX_TRIES:
        guessed_char = input('Guess a letter: ').lower()
        check_input(guessed_char, old_chars)
        guessed_keyword_str = show_keyword(game_keyword, old_chars)
        print_hangman(wrong_tries)
        print(guessed_keyword_str) # because show_keyword increases wrong_tries -> changes the hangman image printed
        if wrong_tries < MAX_TRIES and in_game:
            print('\nYou\'ve got {} tries!'.format(MAX_TRIES - wrong_tries))
        elif wrong_tries >= MAX_TRIES:
            print('\nYou\'ve lost! The keyword was \"{}\"'.format(game_keyword))
        elif not in_game:
            print('\nCongrats! You have successfully guessed the word \"{}\"'.format(game_keyword))


if __name__ == "__main__":
    main()

