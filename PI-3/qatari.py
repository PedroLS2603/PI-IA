import numpy as np
from problema import Problema
from collections import defaultdict

class QAtari:
    def __init__(self, problema: Problema, gamma = 0.1, alpha = 0.1, e=0.4, Q: dict = None):

        self.problema = problema


        # Configurações de exploração
        self.e_inicial =  e
        self.e = self.e_inicial
        self.e_minimo = 0.4
        self.e_decay = 0.95
        
        # Configurações de aprendizado
        self.alpha_inicial=alpha
        self.alpha = self.alpha_inicial
        self.alpha_decay = 0.95
        self.alpha_minimo = 0.1

        # Configurações de desconto
        self.gamma_inicial=gamma
        self.gamma = self.gamma_inicial
        self.gamma_decay = 0.95
        self.gamma_minimo = 0.1

        self.recompensas = {}

        n_acoes = problema.env.action_space.__dict__['n']

    
        if Q:
             self.Q = defaultdict(lambda: np.zeros(n_acoes), Q)
        else:
            self.Q = defaultdict(lambda: np.zeros(n_acoes))
            
    def proxima_acao(self, estado):
        estado = int(estado)

        if np.random.random() < self.e:
            acao = self.problema.env.action_space.sample()
            return acao
        else:
            return int(np.argmax(self.Q[estado]))

    def atualizar_q_table(self, estado, acao, recompensa, prox_estado): 
        estado = int(estado)
        prox_estado = int(prox_estado)

        self.Q[estado][acao] = self.Q[estado][acao] + self.alpha * (recompensa + self.gamma * (self.Q[prox_estado][acao] - self.Q[estado][acao]))  

    def registrar_recompensa(self, ciclo, recompensa):
         self.recompensas[ciclo] = recompensa

    def get_q_table(self):
         copy = {}
         for estado, valores in self.Q.items():
              copy[estado] = valores
         
         return copy
    
    def reduzir_e(self):
         if self.e > self.e_minimo:
            self.e = self.e * self.e_decay
    
    def reduzir_y(self):
         if self.gamma > self.gamma_minimo:
            self.gamma = self.gamma * self.gamma_decay
    
    def reduzir_a(self):
         if self.alpha > self.alpha_minimo:
            self.alpha = self.alpha * self.alpha_decay