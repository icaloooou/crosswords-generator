# -*- coding: utf-8 -*-

import random
import string
import pandas as pd
import mysql.connector
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql.config import DB_CONFIG

def connection(db_config):
    connection = mysql.connector.connect(
        host=f"{db_config['host']}",
        user=f"{db_config['user']}",
        password=f"{db_config['password']}",
        database=f"{db_config['database']}"
    )
    return connection


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
    table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
                        ('BOX',(0,0),(-1,-1),2, colors.black),
                        ('VALIGN',(0,-1),(-1,-1), 'MIDDLE')]))
    return table


def config_words(words):
    words.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
                        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                        ('BOX',(0,0),(-1,-1),2, colors.black)]))
    return words

def organize_vertically(data):
    cols = 3
    rows = (len(data) + cols - 1) // cols
    organized_data = [[] for _ in range(rows)]
    for idx, word in enumerate(data):
        organized_data[idx % rows].append(word)
    return organized_data


def save_grid_18(grid, num_life, num_game, words):
    pdf_name = ".\Jogo_{}_{}.pdf".format(num_game, num_life)
    pdf = SimpleDocTemplate(pdf_name, pagesize=A5, topMargin=20)
    t = Table(grid)
    table = config_pdf(t)
    words.sort()
    words = organize_vertically(words)
    w = Table(words, colWidths=120, rowHeights=18)
    word_list = config_words(w)

    elements = [table, Spacer(1, 20), word_list]
    pdf.build(elements)

def save_grid_9(grid_one, grid_two, num_life, num_game, words_one, words_two):
    pdf_name = ".\Jogo_{}_{}.pdf".format(num_game, num_life)
    pdf = SimpleDocTemplate(pdf_name, pagesize=A5, topMargin=20)
    
    t_one = Table(grid_one)
    table_one = config_pdf(t_one)
    words_one.sort()
    words_one = organize_vertically(words_one)
    w_one = Table(words_one, colWidths=120, rowHeights=18)
    word_list_one = config_words(w_one)

    t_two = Table(grid_two)
    table_two = config_pdf(t_two)
    words_two.sort()
    words_two = organize_vertically(words_two)
    w_two = Table(words_two, colWidths=120, rowHeights=18)
    word_list_two = config_words(w_two)
    
    elements = [table_one, Spacer(1, 20), word_list_one, Spacer(1, 10), table_two, Spacer(1, 20), word_list_two]
    pdf.build(elements)


def make_crosswords(words, size_row, size_column):
    grid = make_grid(size_row, size_column)
    directions = ['diagonal', 'vertical', 'horizontal']
    words_list = []
    qty_words = 0
    random.shuffle(words)
    for word in words:
        if qty_words < TOTAL_WORDS[size_row]:
            put = False
            attempts = 0
            while not put:
                if attempts < 3:
                    row = random.randint(0, size_row - 1)
                    column = random.randint(0, size_column - 1)
                    direction = random.choice(directions)
                    if verify_word(grid, word, row, column, direction):
                        insert_word(grid, word, row, column, direction)
                        put = True
                        qty_words += 1
                        words_list.append(word)
                    else:
                        attempts += 1
                else:
                    put = True
    insert_random_letters(grid)
    return grid, words_list


def get_words_from_db(conn):
    statement = 'SELECT * FROM words WHERE LENGTH(word) > 3 LIMIT 150 ' #total de palavras para todos os jogos (15)
    words = pd.read_sql(statement, conn)
    return words
    

def game():
    conn = connection(DB_CONFIG)
    df = get_words_from_db(conn)
    all_words_lower = df['word'].tolist()
    all_words_upper = [word.upper() for word in all_words_lower]

    life = 0
    while life < LIFETIME:
        for size_row in SIZE_ROW_LIST:
            for game in range(REPETITIONS_ROWS[size_row]):
                if size_row == 9:
                    grid_one, words_one = make_crosswords(all_words_upper, size_row, SIZE_COLUMN)
                    grid_two, words_two = make_crosswords(all_words_upper, size_row, SIZE_COLUMN)
                    num_game = game + size_row
                    save_grid_9(grid_one, grid_two, life, num_game, words_one, words_two)
                else:
                    grid, words = make_crosswords(all_words_upper, size_row, SIZE_COLUMN)
                    num_game = game + size_row
                    save_grid_18(grid, life, num_game, words)
        life += 1
    conn.close()

if __name__ == '__main__':
    LIFETIME = 3
    SIZE_ROW_LIST = [18, 9]
    SIZE_COLUMN = 18
    REPETITIONS_ROWS = {9: 1, 18: 1}
    TOTAL_WORDS = {18: 15, 9: 9}
    game()
