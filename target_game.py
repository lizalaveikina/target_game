import os
import sys
from random import choice
from string import ascii_uppercase
from typing import List

if os.name == 'nt':
    def clear_screen():
        """
        Screen cleaning
        """
        os.system('cls')
else:
    def clear_screen():
        """
        Screen cleaning
        """
        os.system('clear')


def is_good_word(word: str, letters: List[str]) -> bool:
    """
    checks whether a word is formed from the letters in the game
    >>> is_good_word('game', list('gamemover'))
    True
    """
    word = list(word)
    for char in letters:
        try:
            word.remove(char.lower())
        except ValueError:
            pass
    return not bool(len(word))


def get_letters(grid: List[List[str]]) -> List[str]:
    """
    Convert grid to list
    >>> get_letters([['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']])
    ['I', 'G', 'E', 'P', 'I', 'S', 'W', 'M', 'G']
    """
    letters = []
    for row in grid:
        letters.extend(row)
    return letters


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    grid = []
    for line in range(3):
        grid.append(list())
        for char_count in range(3):
            grid[line].append(choice(ascii_uppercase))
    return grid


def get_words(f: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    """
    words_set = set()
    with open(f, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()
            center_char = letters[len(letters) // 2].lower()
            if len(line) >= 4 and not line.startswith('#') and center_char in line:
                if is_good_word(line, letters):
                    words_set.add(line.lower())
    return list(words_set)


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.
    """
    word_lines = sys.stdin.readlines()
    user_words = []
    for line in word_lines:
        for word in line.split():
            if word:
                user_words.append(word.lower())
    return user_words


def get_all_good_user_words(user_words: List[str], letters: List[str]) -> List[str]:
    """
    The function returns a list of all words that are longer than three characters, do not contain #,
    they contain a letter from the middle of the playing field
    >>> get_all_good_user_words(['qazc', 'qcvb','dfgh','fghj'], list('qazxcvbnn'))
    ['qazc', 'qcvb']
    """
    all_good_user_words = list()
    center_char = letters[len(letters) // 2].lower()
    for word in user_words:
        if len(word) >= 4 and not word.startswith('#') and center_char in word:
            if is_good_word(word, letters):
                all_good_user_words.append(word.lower())
    return all_good_user_words


def get_good_user_words(user_words: List[str], letters: List[str], words_from_dict: List[str]) -> List[str]:
    """
        (list, list, list) -> list

        Checks user words with the rules and returns list of those words
        that are in dictionary.
        """

    all_good_user_words = set(get_all_good_user_words(user_words, letters))
    print(all_good_user_words)
    good_user_words = list(all_good_user_words.intersection(words_from_dict))
    return good_user_words


def get_pure_user_words(user_words: List[str], letters: List[str], words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list
    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    all_good_user_words = set(get_all_good_user_words(user_words, letters))
    pure_user_words = list(all_good_user_words.difference(words_from_dict))
    print(len(all_good_user_words) - len(pure_user_words))
    return pure_user_words


def results_to_file(words_from_dict, pure_user_words, good_user_words):
    """
    Save the game results to file
    """
    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(f'Number of correct words:\n\t{len(good_user_words)}\n')
        file.write(f'Words that the player entered correctly and that \
                        are present in the dictionary:\n\t{", ".join(good_user_words)}\n')
        file.write(f'All possible words:\n\t{", ".join(words_from_dict)}\n')
        file.write(f'Words '
                   f'that the player missed:\n\t{", ".join(set(words_from_dict) - set(good_user_words))}\n')
        file.write(f'Words entered by the player that \
                        are not in the dictionary:\n\t{", ".join(pure_user_words)}\n')


def results():
    """
    Main game function
    """
    clear_screen()
    print('=============Start the GAME=============')
    grid = generate_grid()
    print(*grid, sep='\n')
    print('=' * 40)
    print('Enter a word or press Enter and ctrl+d to finish')
    user_words = get_user_words()
    print('=' * 40)
    print('List of all words that can be built from the letters of the playing field:')
    letters = get_letters(grid)
    words_from_dict = get_words('en.txt', letters)
    print(*words_from_dict, sep=', ')
    print('=' * 40)
    print('Pure user words:')
    pure_user_words = get_pure_user_words(user_words, letters, words_from_dict)
    print(*pure_user_words, sep=', ')
    print('=' * 40)
    print('Good user words:')
    good_user_words = get_good_user_words(user_words, letters, words_from_dict)
    print(*good_user_words, sep=', ')
    results_to_file(words_from_dict, pure_user_words, good_user_words)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
