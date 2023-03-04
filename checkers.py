from no import No

class Peca:
    # Tipos
    # N - Normal
    # D - Dama

    # Cores
    # B - Brancas
    # P - Pretas
    def __init__(self, tipo, cor, emoji):
        self.tipo = tipo
        self.cor = cor
        self.emoji = emoji
    
    def __len__(self):
        return 1
    
    def __repr__(self):
        return f"{self.emoji}"
    
class Casa:
    def __init__(self, cor, peca: Peca = None):
        self.cor = cor
        self.peca = peca
    
    def __repr__(self):
        if self.peca:
            return f"{self.peca.emoji}"
        
        return f" "
    
class Checkers:
    def __init__(self):
        self.table = []
        self.turnos = []
        self.raiz = None
        self.nos = []

        for i in range(8):
            self.table.append([])
            for j in range(8):
                if (i == 5 or i == 7) and j % 2 == 0:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "B", "⛀")))
                elif i == 6 and j % 2 == 1:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "B", "⛀")))
                elif (i == 0 or i == 2) and j % 2 == 1:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "P", "⛂")))
                elif i == 1 and j % 2 == 0:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "P", "⛂")))
                elif i == 3:
                    if j % 2 == 1:
                        self.table[i].append(Casa(cor="B"))
                    else:
                        self.table[i].append(Casa(cor="P"))
                elif i == 4:
                    if j % 2 == 0:
                        self.table[i].append(Casa(cor="B"))
                    else:
                        self.table[i].append(Casa(cor="P"))
                else: 
                    self.table[i].append(Casa(cor="P"))
    
    def print(self):
        for linha in self.table:
            print(linha)

    def iniciar(self):
        self.raiz = No(estado=self.table)
        self.nos.append(self.raiz)

    def quem_joga(self):
        if(len(self.turnos) % 2 == 0):
            return "B"
        else:
            return "P"
    
    def valida_estado(self, no):
        for linha in no.estado:
            for casa in linha:
                if casa.peca != None and casa.cor == "B":
                    return False

        return True
    

    def valida_fim_de_jogo(self, no = None):

        if no == None:
            return False

        count_pretas = 0
        count_brancas = 0

        for linha in no.estado:
            for casa in linha:
                if casa.peca:
                    if casa.peca.cor == "P":
                        count_pretas += 1
                    else:
                        count_brancas +=1
        
        return count_pretas == 0 or count_brancas == 0
                
    def acao(self, jogador, origem, destino, no: No = None):
        if not no:
            no = self.nos[-1]
        estado = list.copy(no.estado)
        
        casa_origem = estado[origem[0]][origem[1]]
        casa_destino = estado[destino[0]][destino[1]]

        if (casa_origem.cor != "P") or (casa_origem.peca == None)  or (jogador != self.quem_joga()) or (jogador != casa_origem.peca.cor):
            return None
        
        if (casa_destino.peca != None and casa_destino.peca.cor != jogador): 
            if (estado[destino[0] + 1][destino[1] + 1].peca == None and origem[0] > destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] + 1]
            elif (estado[destino[0] + 1][destino[1] + 1].peca == None and origem[0] > destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] + 1]
            elif (estado[destino[0] + 1][destino[1] - 1].peca == None and origem[0] < destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] - 1]
            elif (estado[destino[0] - 1][destino[1] - 1].peca == None and origem[0] < destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] - 1]
            elif (estado[destino[0] - 1][destino[1] + 1].peca == None and origem[0] > destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] - 1]
            elif (estado[destino[0] + 1][destino[1] + 1].peca == None and origem[0] < destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] + 1]
            elif (estado[destino[0] - 1][destino[1] - 1].peca == None and origem[0] > destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] - 1]
            casa_destino = estado[destino[0]][destino[1]]

        estado[destino[0]][destino[1]].peca = estado[origem[0]][origem[1]].peca
        estado[origem[0]][origem[1]].peca = None

        self.turnos.append(tuple([len(self.turnos) + 1, origem, destino]))

        novo_no = No(no_pai = no, heuristica=0, estado=estado)
        self.nos.append(novo_no)
        self.table = estado
        return novo_no

        