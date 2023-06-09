import numpy as np
from problema import Problema

class QAtary:
    def __init__(self, problema: Problema, desconto = 0.1, tetha = 1e-6, alpha = 0.1):

        self.problema = problema
        self.desconto = desconto
        self.tetha=tetha
        self.alpha=alpha
        self.Q = {}
        self.e = 0.4
        self.recompensas = {}
    
        n_acoes = problema.env.action_space.__dict__['n']
        self.Q[problema.estado_inicial] = np.zeros(n_acoes)
            
    def proxima_acao(self, estado):
        if np.random.random() < self.e:
            acao = self.problema.env.action_space.sample()
            return acao
        else:
            if estado not in self.Q.keys():
                n_acoes = self.problema.env.action_space.__dict__['n']
                self.Q[estado] = np.zeros(n_acoes)
            return int(np.argmax(self.Q[estado]))

    def atualizar_q_table(self, estado, acao, recompensa, prox_estado):        
        if estado not in self.Q.keys():
                n_acoes = self.problema.env.action_space.__dict__['n']
                self.Q[estado] = np.zeros(n_acoes)

        if prox_estado not in self.Q.keys():
                n_acoes = self.problema.env.action_space.__dict__['n']
                self.Q[prox_estado] = np.zeros(n_acoes)

        self.Q[estado][acao] = self.Q[estado][acao] + self.alpha * (recompensa + self.desconto * (self.Q[prox_estado][acao] - self.Q[estado][acao]))  

    def registrar_recompensa(self, ciclo, recompensa):
         self.recompensas[ciclo] = recompensa