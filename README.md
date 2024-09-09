# Gerador de Caça-Palavras
---
* Esse projeto tem como intuito gerar caça-palavras e salva-los para impressão.

<p align="center">
    <img loading="lazy" src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-%23FFA500"/>
</p>

---

## Funcionalidades :hammer: 
* `make_grid`: Cria uma matriz de acordo com os valores passados, nesse caso para impressão em A5 consideramos matrizes de 18x18.
* `verify_word`: Primeiro verifica se é possivel inserir a palavra dentro da matriz (validação de tamanho), em seguida verificamos se já existe alguma letra nesse espaço onde a palavra se encaixa.
* `insert_word`: Faz a inserção da palavra letra a letra dentro dos espaços da matriz.
* `insert_random_letters`: Após inserir todas as palavras dentro da matriz, é feito a inserção de letras aleatórias dentro dos espaços que ficaram vazios.
* `print_grid`: Nesse caso estamos printando o resultado do grid com as palavras inseridas e as letras aleatórias.
* `make_crosswords`: Função responsável por organizar e chamar as demais funções.

## Implementar :thought_balloon:
1. Leitura das palavras em um banco de dados, ao invés de uma lista manual;
2. Salvamento dos resultados em arquivos, ao invés de printar em tela;
3. Geração de matrizes com dois tamanhos para criação de retangulos, ao invés de sempre ser uma matriz quadrada.

## Tecnologias
* `Python`
