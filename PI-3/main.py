import gymnasium
from problema import Problema
from qatari import QAtari
import matplotlib.pyplot as plt
from util import converter
import os
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--eps",    default=10,     help="Iterações.", type=int)
parser.add_argument("--load",   default=f"qtable_0.ql")
parser.add_argument("--dict",   default="dict", help="Dict ram/disk.")
parser.add_argument("--mode",   default=None, help="Visualization mode")
parser.add_argument("--game",   default="MsPacman", help="Game to leaarn")
args = parser.parse_args()

proj_path = __file__.split('main')[0]
try:
  load_folder = os.path.join(proj_path, f"qtables_{args.game}/")
  qtable_file_index = len(os.listdir(load_folder))
except FileNotFoundError:
  os.mkdir(load_folder)


testes = [
  {"alpha": 0.1, "gamma": 1, "e": 1},
  {"alpha": 0.2, "gamma": 0.9, "e": 1},
  {"alpha": 0.3, "gamma": 0.8, "e": 1},
  {"alpha": 0.4, "gamma": 0.7, "e": 1},
  {"alpha": 0.5, "gamma": 0.6, "e": 1},
  {"alpha": 0.6, "gamma": 0.5, "e": 1},
  {"alpha": 0.7, "gamma": 0.4, "e": 1},
  {"alpha": 0.8, "gamma": 0.3, "e": 1},
  {"alpha": 0.9, "gamma": 0.2, "e": 1},
  {"alpha": 1, "gamma": 0.1, "e": 1},
]

def treinar(teste, eps, problema: Problema, q_load = None):
  problema.reset()
  agente = QAtari(problema, alpha=teste["alpha"], gamma=teste["gamma"], Q=q_load, e=teste["e"])
  

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


env = gymnasium.make(f"ALE/{args.game}-v5", obs_type="ram", render_mode=args.mode)
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


    try:
      plt.savefig(f"resultados_{args.game}/desempenho_{j}")

    except:
      os.mkdir(os.path.join(proj_path, f"resultados_{args.game}/"))
      plt.savefig(f"resultados_{args.game}/desempenho_{j}")

    f = open(os.path.join(load_folder, f"qtable_{j}.ql"), "wb")
    pickle.dump(agente.get_q_table(),f)
    f.close()
else:
  file_index = args.load.split(".")[0].split("_")[-1]
  q_file = open(os.path.join(load_folder, args.load), "rb")
  q_load = pickle.load(q_file)
  q_file.close()
  teste = {"alpha": 0.5, "gamma": 0.6, "e": 0.5}

  agente = treinar(teste=teste,eps=args.eps,problema=problema,q_load=q_load)

  x = [x for x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]
  y = [y for x,y in agente.recompensas.items() if x in list(agente.recompensas.keys()) if x % (args.eps/10) == 0]

  plt.clf()
  plt.title("Recompensa x ciclo")
  plt.xticks(x)
  plt.plot(x, y)

  plt.xlabel("Ciclo")
  plt.ylabel("Pontuação")

  try:
    plt.savefig(f"resultados/desempenho_{file_index}")

  except:
    os.mkdir(os.path.join(proj_path, f"resultados_{args.game}/"))
    plt.savefig(f"resultados_{args.game}/desempenho_{file_index}")


  f = open(os.path.join(load_folder, f"qtable_{file_index}.ql"), "wb")
  pickle.dump(agente.get_q_table(),f)
  f.close()

  
env.close()
