# -*- coding: utf-8 -*-

import hashlib
import requests
import mysql.connector
from bs4 import BeautifulSoup

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


def generate_unique_id(word):
    hash_object = hashlib.sha256(word.encode('utf-8'))
    unique_id = hash_object.hexdigest()
    return unique_id


def put_db(conn, words):
    cursor = conn.cursor()
    theme = 'Dictionary'
    language = 'pt-br'
    for word in words:
        id_ = generate_unique_id(word)
        try:
            statement = f"INSERT INTO crosswords.words (hash_id, language, word, theme) VALUES ('{id_}', '{language}', '{word}', '{theme}');"
            cursor.execute(statement)
            conn.commit()
        except:
            pass


def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_qty_words(soup):
    select_fs = soup.find('select', {'name': 'fs'})
    if select_fs:
        options = select_fs.find_all('option')
        option_values = [int(option.text) for option in options]
    max_qty_words = max(option_values)
    return max_qty_words


def get_type(soup):
    select_fs2 = soup.find('select', {'name': 'fs2'})
    if select_fs2:
        for option in select_fs2.find_all('option'):
            type_ = option.text.strip()
            if 'completo' in type_.lower():
                number_type = option.get('value')
                return number_type


def get_words(max_qty_words, number_type):
    url = f'https://www.palavrasaleatorias.com/?fs={max_qty_words}&fs2={number_type}&Submit=Nova+palavra'
    soup = fetch_url(url)
    divs = soup.find_all('div', {'style': 'font-size:3em; color:#6200C5;'})
    return [d.text.strip().replace(' ', '').lower() for d in divs]


def main(url, lifetime):
    conn = connection(DB_CONFIG)
    life = 0
    while life < lifetime:
        soup_initial = fetch_url(url)
        max_qty_words = get_qty_words(soup_initial)
        number_type = get_type(soup_initial)
        words = get_words(max_qty_words, number_type)
        put_db(conn, words)
        life += 1

    
if __name__ == '__main__':
    url = 'https://www.palavrasaleatorias.com'
    lifetime = 3
    main(url, lifetime)
