# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_option_menu import option_menu
import populate_db
import generate_games

st.set_page_config(
    page_title="Gerador de Caça-Palavras",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    choice = option_menu("Início",
                            ["Popular Banco", "Gerar caça-palavra"], 
                            icons=["plus", "book"],
                            menu_icon="house",
                            default_index=0
                        )
    
if choice == "Popular Banco":
    populate_db.run()
if choice == "Gerar caça-palavra":
    generate_games.run()
