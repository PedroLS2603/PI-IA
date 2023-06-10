from gymnasium import Env
from util import converter

class Problema:
    def __init__(self, env: Env, nome=None):
        self.env = env
        self.nome = nome
    
    def reset(self):
        self.estado_inicial = converter(self.env.reset()[0])
        


