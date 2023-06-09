import gymnasium
from problema import Problema
from qatary import QAtary
import matplotlib.pyplot as plt
import json
from util import converter
import os

# https://pypi.org/project/colorama/
from colorama import just_fix_windows_console, init, Back, Fore

init(autoreset=True)
# jogo = "VideoPinball"

# use Colorama to make Termcolor work on Windows too
just_fix_windows_console()

num_episodio = 5
env = gymnasium.make("ALE/MsPacman-v5", obs_type="ram")


problema = Problema(env)
problema.reset()
# Obtendo estado inicial e de ações do agente

agente = QAtary(problema)




# ambiente_txt = "Ambiente [%s]" % convert(ambiente)
# print(ambiente_txt)
# print(ambiente_txt, "Tamanho: " + str(len(ambiente))) 

estado_atual = agente.problema.estado_inicial
for i in range(num_episodio):
  agente.problema.reset()
  recompensa_total = 0

  while True:
    # definição da política
    acao = agente.proxima_acao(estado_atual)

    prox_estado, recompensa, finalizado, paralizado, info = env.step(acao)
    prox_estado = converter(prox_estado)

    agente.atualizar_q_table(estado_atual, acao, recompensa, prox_estado)


    #TXT's
    # ambiente_txt = "Ambiente [%s]" % convert(ambiente)
    recompensa_txt = "Recompensa: [%s]" % recompensa
    fim_txt = "Finalizado: [%s]" % finalizado
    acao_txt = "Ação: [%s]" % acao

    if (recompensa < 0):
      recompensa_txt = Fore.RED + recompensa_txt + Fore.RESET
    elif (recompensa >= 0):
      recompensa_txt = Fore.GREEN + recompensa_txt + Fore.RESET

    if (finalizado):
      fim_txt = Fore.RED + fim_txt + Fore.RESET

    # print(recompensa_txt, fim_txt, acao_txt)

    estado_atual = prox_estado

    recompensa_total += recompensa


    if finalizado or paralizado:
      break
  
  agente.registrar_recompensa(i, recompensa_total)
    

plt.title("Recompensa x ciclo")
plt.plot(agente.recompensas.keys(), agente.recompensas.values())
plt.show()

qtable = json.dumps(agente.Q)

qtable_file_index = len(os.listdir(os.path.join(os.getcwd(), "/qtables")))

with open(f"qtable{qtable_file_index}.json", "w") as outfile:
    json.dump(qtable, outfile)

env.close()