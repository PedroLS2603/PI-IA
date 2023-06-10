import gymnasium
from problema import Problema
from qatari import QAtari
import matplotlib.pyplot as plt
from util import converter
import os
import pickle
import argparse


load_folder = os.path.join(__file__.split('main')[0], "qtables/")
qtable_file_index = len(os.listdir(load_folder))

parser = argparse.ArgumentParser()
parser.add_argument("--eps",    default=10,     help="Iterações.", type=int)
parser.add_argument("--load",   default=f"qtable_{qtable_file_index - 1}.ql")
parser.add_argument("--dict",   default="dict", help="Dict ram/disk.")

args = parser.parse_args()

testes = [
  {"alpha": 0.1, "gamma": 1},
  {"alpha": 0.2, "gamma": 0.9},
  {"alpha": 0.3, "gamma": 0.8},
  {"alpha": 0.4, "gamma": 0.7},
  {"alpha": 0.5, "gamma": 0.6},
  {"alpha": 0.6, "gamma": 0.5},
  {"alpha": 0.7, "gamma": 0.4},
  {"alpha": 0.8, "gamma": 0.3},
  {"alpha": 0.9, "gamma": 0.2},
  {"alpha": 1, "gamma": 0.1},
]

def treinar(teste, eps, problema: Problema, q_load = None):
  problema.reset()
  agente = QAtari(problema, alpha=teste["alpha"], gamma=teste["gamma"], Q=q_load)
  

  estado_atual = agente.problema.estado_inicial
  for i in range(eps + 1):
    agente.problema.reset()
    recompensa_total = 0

    while True:
      acao = agente.proxima_acao(estado_atual)

      prox_estado, recompensa, finalizado, paralizado, info = problema.env.step(acao)
      prox_estado = converter(prox_estado)

      agente.atualizar_q_table(estado_atual, acao, recompensa, prox_estado)

      estado_atual = prox_estado
      recompensa_total += recompensa


      if finalizado or paralizado:
        break
    
    agente.registrar_recompensa(i, recompensa_total)
    agente.reduzir_e()
    agente.reduzir_y()
    agente.reduzir_a()

  return agente



env = gymnasium.make("ALE/MsPacman-v5", obs_type="ram")
problema = Problema(env)

if args.dict == "dict":
  for j in range(len(testes)):
    
    teste = testes[j]

    agente = treinar(teste=teste,eps=args.eps,problema=problema)

    x = [x for x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]
    y = [y for x,y in agente.recompensas.items() if x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]
    
    plt.clf()
    plt.title("Recompensa x ciclo")
    plt.xticks(x)
    plt.plot(x, y)

    plt.xlabel("Ciclo")
    plt.ylabel("Pontuação")


    plt.savefig(f"resultados/desempenho_{j}")

    f = open(os.path.join(load_folder, f"qtable_{j}.ql"), "wb")
    pickle.dump(agente.get_q_table(),f)
    f.close()
else:
  file_index = args.load.split(".")[0].split("_")[-1]
  q_file = open(os.path.join(load_folder, args.load), "rb")
  q_load = pickle.load(q_file)
  q_file.close()
  teste = {"alpha": 0.5, "gamma": 0.6}

  agente = treinar(teste=teste,eps=args.eps,problema=problema,q_load=q_load)

  x = [x for x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]
  y = [y for x,y in agente.recompensas.items() if x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]

  plt.clf()
  plt.title("Recompensa x ciclo")
  plt.xticks(x)
  plt.plot(x, y)

  plt.xlabel("Ciclo")
  plt.ylabel("Pontuação")


  plt.savefig(f"resultados/desempenho_{file_index}")

  f = open(os.path.join(load_folder, f"qtable_{file_index}.ql"), "wb")
  pickle.dump(agente.get_q_table(),f)
  f.close()

  
env.close()
