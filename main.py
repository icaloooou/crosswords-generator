# -*- coding: utf-8 -*-

import random
import string
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

LIFETIME = 3
SIZE_ROW_LIST = [18, 9]
SIZE_COLUMN = 18
REPETITIONS_ROWS = {9: 1, 18: 3}


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


def config_pdf(table):
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
                        ('BOX',(0,0),(-1,-1),2, colors.black),
                        ('VALIGN',(0,-1),(-1,-1), 'MIDDLE')]))
    return table


def config_words(words):
    words.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
                        ('BOX',(0,0),(-1,-1),2, colors.black)]))
    return words


def save_grid_18(grid, num_life, num_game, words):
    pdf_name = ".\Jogo_{}_{}.pdf".format(num_game, num_life)
    pdf = SimpleDocTemplate(pdf_name, pagesize=A5)
    t = Table(grid)
    table = config_pdf(t)
    w = Table([words])
    word_list = config_words(w)

    elements = [table, Spacer(1, 30), word_list]
    pdf.build(elements)

def save_grid_9(grid_one, grid_two, num_life, num_game, words):
    pdf_name = ".\Jogo_{}_{}.pdf".format(num_game, num_life)
    pdf = SimpleDocTemplate(pdf_name, pagesize=A5)
    
    t_one = Table(grid_one)
    table_one = config_pdf(t_one)
    t_two = Table(grid_two)
    table_two = config_pdf(t_two)
    w = Table([words])
    word_list = config_words(w)

    elements = [table_one, Spacer(1, 20), word_list, Spacer(1, 10), table_two, Spacer(1, 20), word_list]
    pdf.build(elements)


def make_crosswords(words, size_row, size_column):
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
    return grid


def game(words):
    life = 0
    while life < LIFETIME:
        for size_row in SIZE_ROW_LIST:
            for game in range(REPETITIONS_ROWS[size_row]):
                if size_row == 9:
                    grid_one = make_crosswords(words, size_row, SIZE_COLUMN)
                    grid_two = make_crosswords(words, size_row, SIZE_COLUMN)
                    num_game = game + size_row
                    save_grid_9(grid_one, grid_two, life, num_game, words)
                else:
                    grid = make_crosswords(words, size_row, SIZE_COLUMN)
                    num_game = game + size_row
                    save_grid_18(grid, life, num_game, words)
        life += 1

if __name__ == '__main__':
    words = ["PYTHON", "CHALLENGE", "ALGORITHM", "CROSSWORD", "SEARCH"]
    game(words)
