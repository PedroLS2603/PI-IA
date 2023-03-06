from no import No
import time

class Peca:
    # Tipos
    # N - Normal
    # D - Dama

    # Cores
    # B - Brancas
    # P - Pretas
    def __init__(self, tipo, cor):
        self.tipo = tipo
        self.cor = cor
        if tipo == "D":
            if cor == "B":
                self.emoji = "⛁"
            else:
                self.emoji = "⛃"
        else:
            if cor == "B":
                self.emoji = "⛀"
            else:
                self.emoji = "⛂"
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
        self.vencedor = None

        for i in range(8):
            self.table.append([])
            for j in range(8):
                if (i == 5 or i == 7) and j % 2 == 0:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "B")))
                elif i == 6 and j % 2 == 1:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "B")))
                elif (i == 0 or i == 2) and j % 2 == 1:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "P")))
                elif i == 1 and j % 2 == 0:
                    self.table[i].append(Casa(cor="P", peca=Peca("N", "P")))
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
            no = self.nos[-1]

        count_pretas = 0
        count_brancas = 0

        for linha in no.estado:
            for casa in linha:
                if casa.peca:
                    if casa.peca.cor == "P":
                        count_pretas += 1
                    else:
                        count_brancas +=1
        if(count_pretas == 0):
            self.vencedor = "Brancas"
        elif(count_brancas == 0):
            self.vencedor = "Pretas"
        return count_pretas == 0 or count_brancas == 0
                
    def acao(self, jogador, origem, destino, no: No = None):
        if not no:
            no = self.nos[-1]
        estado = list.copy(no.estado)
        casa_origem = estado[origem[0]][origem[1]]
        casa_destino = estado[destino[0]][destino[1]]

        if (casa_destino.cor != "P") or (casa_origem.peca == None)  or (jogador != self.quem_joga()) or (jogador != casa_origem.peca.cor) or (jogador == "B" and destino[0] > origem[0] and casa_origem.peca.tipo == "N") or (jogador == "P" and destino[0] < origem[0] and casa_origem.peca.tipo == "N") or (destino == origem) or (destino[0] - origem[0] >= 2 or destino[0] - origem[0] <= -2) or (destino[1] - origem[1] >= 2 or destino[1] - origem[1] <= -2):
            print("Movimento inválido!")
            time.sleep(1)
            return None
        
        #Captura
        if (casa_destino.peca != None and casa_destino.peca.cor != jogador):
            #valida se não está capturando a própria peça
            if  (casa_destino.peca.cor == jogador):
                print("Movimento inválido!")
                return None
            elif (estado[destino[0] + 1][destino[1] + 1].peca == None and origem[0] < destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] + 1]
            elif (estado[destino[0] + 1][destino[1] - 1].peca == None and origem[0] < destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] - 1]
            elif (estado[destino[0] - 1][destino[1] + 1].peca == None and origem[0] > destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] + 1]
            elif (estado[destino[0] - 1][destino[1] - 1].peca == None and origem[0] > destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] - 1]
            casa_destino = estado[destino[0]][destino[1]]         
        peca_antiga = estado[origem[0]][origem[1]].peca


        if(casa_origem.peca.cor == "P" and destino[0] == 7) or (casa_origem.peca.cor == "B" and destino[0] == 0):
            estado[destino[0]][destino[1]].peca = Peca(tipo="D", cor=peca_antiga.cor)
        else:
            estado[destino[0]][destino[1]].peca = casa_origem.peca
        estado[origem[0]][origem[1]].peca = None

        self.turnos.append(tuple([len(self.turnos) + 1, jogador, origem, destino]))

        novo_no = No(no_pai = no, heuristica=0, estado=estado)
        self.nos.append(novo_no)
        self.table = estado
        return novo_no

        