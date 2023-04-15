import pandas as pd
import numpy as np
import random

GERACOES_MAX = 10000000
ERRO_MIN = 0.1
DOMINIO_GENE = []
DESLOCAMENTOS = []

class Deslocamento:
    def __init__(self, origem, destino, tempo, valor):
        self.origem = origem
        self.destino = destino
        self.tempo = tempo
        self.valor = valor

    def __repr__(self) -> str:
      return f"{self.origem.nome} -> {self.destino.nome}"
class Cidade:
  def __init__(self, nome, peso=None, valor=None, tempo_roubo=None, item=None):
    self.peso = peso
    self.nome = nome
    self.valor = valor
    self.item = item
    self.tempo_roubo = tempo_roubo
    self.sigla = ''.join([palavra[0] for palavra in nome.split()])
  
  def __repr__(self):
    return f"{self.nome}"

class Rota:
  def __init__(self, cidades):
    self.dominio = cidades
    self.deslocamentos = []

    rota = self.dominio[1:self.dominio[1:].index([cidade for cidade in DOMINIO_GENE if cidade.nome == "Escondidos"][0]) + 1]
    for i in range(len(rota)):
      if i == len(rota) - 1:
        break
      origem = rota[i]
      destino = rota[i+1]

      self.deslocamentos.append([deslocamento for deslocamento in DESLOCAMENTOS if deslocamento.origem == origem and deslocamento.destino == destino][0])


  def __repr__(self):
    rota = self.dominio[1:self.dominio[1:].index([cidade for cidade in DOMINIO_GENE if cidade.nome == "Escondidos"][0]) + 1]

    return '->'.join([cidade.nome for cidade in rota])

  def fitness(self):

    rota = self.dominio[1:self.dominio[1:].index([cidade for cidade in self.dominio[1:] if cidade.nome == "Escondidos"][0]) + 1]

    tempo_roubo_total = np.array([cidade.tempo_roubo for cidade in rota]).sum()
    tempo_deslocamento_total = np.array([deslocamento.tempo for deslocamento in self.deslocamentos]).sum()
    tempo_total = tempo_roubo_total + tempo_deslocamento_total

    peso_total = np.array([cidade.peso for cidade in rota]).sum()

    montante_roubo = np.array([cidade.valor for cidade in rota]).sum()
    gasto_deslocamento = np.array([deslocamento.valor for deslocamento in self.deslocamentos]).sum()

    liquido = montante_roubo - gasto_deslocamento

    cidades_repetidas = 0
    for cidade in rota:
      cidades_repetidas += len([c for c in rota if c.nome == cidade.nome]) - 1

    if tempo_total > 72 or peso_total > 20 or cidades_repetidas > 0:
      return float("-inf")
    
    return (liquido/tempo_total) + (liquido/peso_total)


##TODO: FIX FLIP MUTATION
  def mutacao(self):

    possibilidades = list(range(len(self.dominio)))

    while True: 
        idx_substituto = random.choice(possibilidades)
        idx_substituido = random.choice(possibilidades)

        if(idx_substituto != idx_substituido and idx_substituido != 0 and idx_substituto != 0):
          substituto = self.dominio[random.choice(possibilidades)]
          substituido = self.dominio[random.choice(possibilidades)]
          self.dominio[self.dominio.index(substituido)] = substituto
          self.dominio[self.dominio.index(substituto)] = substituido
          break

    return Rota(self.dominio)


  def crossover(self):
    raise NotImplementedError("Implementar")

class AlgoritmoGeneticoIndividuo:
  def __init__(self, individuo, geracoes_max=GERACOES_MAX,
                          erro_min=ERRO_MIN):
    self.individuo = individuo
    self.geracoes_max = geracoes_max
    self.erro_min = erro_min
    self.erro = float('inf')
    self.geracoes = 1

  def erro_final(self):
    return self.erro

  def qtd_geracoes(self):
    return self.geracoes
    
  def rodar(self):
    ultimo_fitness = self.individuo.fitness() 
    while True:
      if self.geracoes <= self.geracoes_max and self.erro > self.erro_min:
        novo_individuo = self.individuo.mutacao()
        fitness = novo_individuo.fitness()
        if fitness > ultimo_fitness:
          self.erro = abs(fitness - ultimo_fitness)
          ultimo_fitness = fitness
          self.individuo = novo_individuo
        self.geracoes += 1
        if self.geracoes % 100000 == 0: print(f"Geração: {self.geracoes}, Erro: {self.erro}, Indivíduo: {self.individuo}, fitness: {ultimo_fitness}")
      else:
        break
    return self.individuo

def configurar_dominio(itens: pd.DataFrame, deslocamentos: pd.DataFrame):
  DOMINIO_GENE.append(Cidade(nome="Escondidos", tempo_roubo=0, peso=0, valor=0))
  for index, row in itens.iterrows():
    DOMINIO_GENE.append(Cidade(nome=row["Cidade"], peso=row["Peso"], valor=row["Valor"], tempo_roubo=row["Tempo_Roubo"], item=row["Item"]))

  for index, row in deslocamentos.iterrows():
    origem = [cidade for cidade in DOMINIO_GENE if row["Origem"] == cidade.nome][0]
    destino = [cidade for cidade in DOMINIO_GENE if row["Destino"] == cidade.nome][0]
    valor = row["Valor"]
    tempo = row["Tempo"]
    DESLOCAMENTOS.append(Deslocamento(origem=origem, destino=destino, tempo=tempo, valor=valor))
