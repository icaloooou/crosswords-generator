# -*- coding: utf-8 -*-

import random
import string

LIFETIME = 3


def make_grid(size_r, size_c):
    return [[' ' for s in range(size_c)] for s in range(size_r)]


def verify_word(grid, word, row, column, direction):
    size_grid = len(grid)
    size_word = len(word)
    if direction == 'horizontal' and column + size_word > size_grid:
        return False
    if direction == 'vertical' and row + size_word > size_grid:
        return False
    if direction == 'diagonal' and (row + size_word > size_grid or column + size_word > size_grid):
        return False
    
    for i in range(size_word):
        if direction == 'horizontal' and grid[row][column + i] != ' ' and grid[row][column + i] != word[i]:
            return False
        if direction == 'vertical' and grid[row + i][column] != ' ' and grid[row + i][column] != word[i]:
            return False
        if direction == 'diagonal' and grid[row + i][column + i] != ' ' and grid[row + i][column + i] != word[i]:
            return False
    
    return True


def insert_word(grid, word, row, column, direction):
    for i in range(len(word)):
        if direction == 'horizontal':
            grid[row][column + i] = word[i]
        elif direction == 'vertical':
            grid[row + i][column] = word[i]
        elif direction == 'diagonal':
            grid[row + i][column + i] = word[i]


def insert_random_letters(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(string.ascii_uppercase)


def print_grid(grid):
    for linha in grid:
        print(' '.join(linha))

 
def make_crosswords(words):  
    size_row_list = [18, 9]
    size_column = 18
    repetition_rows = {9: 2, 18: 3}

    i = 0
    while i < LIFETIME:
        for r in size_row_list:
            for _ in range(repetition_rows[r]):
                size_row = r

                grid = make_grid(size_row, size_column)
                directions = ['diagonal', 'vertical', 'horizontal']
                for word in words:
                    put = False
                    while not put:
                        row = random.randint(0, size_row - 1)
                        column = random.randint(0, size_column - 1)
                        direction = random.choice(directions)
                        if verify_word(grid, word, row, column, direction):
                            insert_word(grid, word, row, column, direction)
                            put = True
                insert_random_letters(grid)
                print_grid(grid)
                i += 1

if __name__ == '__main__':
    words = ["PYTHON", "CHALLENGE", "ALGORITHM", "CROSSWORD", "SEARCH"]
    make_crosswords(words)
