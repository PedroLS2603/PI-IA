import ag

import pandas as pd

itens = pd.read_csv("itens.csv")
deslocamentos = pd.read_csv("deslocamentos.csv")

ag.configurar_dominio(itens=itens, deslocamentos=deslocamentos)

aa = (ag.DOMINIO_GENE + [cidade for cidade in ag.DOMINIO_GENE if cidade.nome == "Escondidos"])

print(aa)
b = aa[-1]

aa[-1] = aa[9]

aa[9] = b

individuo_inicial = ag.Rota(cidades=aa)

print(individuo_inicial)

algoritmo = ag.AlgoritmoGeneticoIndividuo(individuo=individuo_inicial)

final = algoritmo.rodar()

print(final)