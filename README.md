# Gerador de Caça-Palavras
---
* Esse projeto tem como intuito gerar caça-palavras e salva-los para impressão.

<p align="center">
    <img loading="lazy" src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-%23FFA500"/>
</p>

---

## Funcionalidades :hammer: 
* `make_grid`: Cria uma matriz de acordo com os tamanhos de 18x18 e 9x18. Existe um lifetime para que a geração se repita 3 vezes e nesse caso, colocamos uma geração de 3 jogos de 18x18 e 2 de 9x18, somando 15 jogos.
* `verify_word`: Primeiro verifica se é possivel inserir a palavra dentro da matriz (validação de tamanho), em seguida verificamos se já existe alguma letra nesse espaço onde a palavra se encaixa.
* `insert_word`: Faz a inserção da palavra letra a letra dentro dos espaços da matriz.
* `insert_random_letters`: Após inserir todas as palavras dentro da matriz, é feito a inserção de letras aleatórias dentro dos espaços que ficaram vazios.
* `config_pdf`: Nessa função fazemos a configuração do nosso grid.
* `config_words`: Assim como configuramos o grid, nós também estilizamos as palavras que estão escondidas dentro do grid.
* `save_grid_18`: Configuramos para poder salvar em PDF os grids de 18x18.
* `save_grid_9`: Configuramos para poder salvar em PDF os grids de 9x18.
* `make_crosswords`: Função responsável por organizar e chamar as demais funções para formar o caça-palavras.
* `game`: Essa função organiza a chamada de todas as outras funções acima, gerando nossos caç-palavras.

## Implementar :thought_balloon:
1. Leitura das palavras em um banco de dados, ao invés de uma lista manual;
2. ~~Salvamento dos resultados em arquivos, ao invés de printar em tela;~~
3. ~~Geração de matrizes com dois tamanhos para criação de retangulos, ao invés de sempre ser uma matriz quadrada;~~
4. Geração de board com streamlit para podermos "rodar" nosso gerador de caça-palavras de forma mais amigável.

## Tecnologias e bibliotecas
- `Python`
    - `random`
    - `string`
    - `reportlab`
