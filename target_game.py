import os
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
