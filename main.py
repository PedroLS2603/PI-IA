from checkers import Checkers
import os
import time

jogo = Checkers()

jogo.iniciar()

while not jogo.valida_fim_de_jogo():
    os.system("clear")
    jogo.print()

    jogador = jogo.quem_joga()
    placeholder = 'Brancas' if jogo.quem_joga() == "B" else "Pretas"
    print(f"Vez de {placeholder}")
    # try:
    linha_origem = int(input("Linha origem: ")) - 1
    coluna_origem = int(input("Coluna origem: ")) - 1

    linha_destino = int(input("Linha destino: ")) - 1
    coluna_destino = int(input("Coluna destino: ")) - 1
    jogo.acao(jogador=jogador, origem=[linha_origem, coluna_origem], destino=[linha_destino, coluna_destino])
    # except ValueError:
    #     print("Movimento inválido!")
    #     time.sleep(1)
    # except IndexError:
    #     print("Movimento inválido!")
    #     time.sleep(1)

os.system("clear")
jogo.print()
print(f"{jogo.vencedor} venceram!")