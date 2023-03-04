from checkers import Checkers
import os

jogo = Checkers()

jogo.iniciar()

while not jogo.valida_fim_de_jogo():
    os.system("clear")
    jogo.print()

    jogador = jogo.quem_joga()
    print(f"Vez de {jogador}")

    linha_origem = int(input("Linha origem: ")) - 1
    coluna_origem = int(input("Coluna origem: ")) - 1

    linha_destino = int(input("Linha destino: ")) - 1
    coluna_destino = int(input("Coluna destino: ")) - 1

    jogo.acao(jogador=jogador, origem=[linha_origem, coluna_origem], destino=[linha_destino, coluna_destino])