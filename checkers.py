from no import No
import time

class Possibilidade:
    pass

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
            self.peso = 10
            if cor == "B":
                self.emoji = "⛁"
            else:
                self.emoji = "⛃"
        else:
            self.peso = 5
            if cor == "B":
                self.emoji = "⛀"
            else:
                self.emoji = "⛂"
    def __len__(self):
        return 1
    
    def __repr__(self):
        return f"{self.emoji}"
    
class Casa:
    def __init__(self, linha, coluna, peca: Peca = None):
        self.cor = None
        self.peca = peca
        self.linha = linha
        self.coluna = coluna
        self.peso = None

        if (linha % 2 == 0 and coluna % 2 == 0) or (linha % 2 == 1 and coluna % 2 == 1):
            self.cor = "B"
        else:
            self.cor = "P"

        if self.cor == "P":
            if linha == 0 or linha == 7 or coluna == 0 or coluna == 7:
                self.peso = 4
            elif linha == 1 or linha == 6 or coluna == 1 or coluna == 6:
                self.peso = 3
            elif linha == 2 or linha == 5 or coluna == 2 or coluna == 5:
                self.peso = 2
            else:
                self.peso = 1
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
                if ((i == 5 or i == 7) and j % 2 == 0) or (i == 6 and j % 2 == 1):
                    self.table[i].append(Casa(linha = i, coluna=j, peca=Peca("N", "B")))
                elif ((i == 0 or i == 2) and j % 2 == 1) or (i == 1 and j % 2 == 0):
                    self.table[i].append(Casa(linha = i, coluna=j, peca=Peca("N", "P")))
                else:
                    self.table[i].append(Casa(linha = i, coluna=j))
    
    def print(self):
        for linha in range(len(self.table)):
            print(f"{linha + 1} {self.table[linha]}")

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
    
    def calcular_possibilidades(self, destino):
        return [[destino[0] + 1, destino[1] + 1], [destino[0] + 1, destino[1] - 1], [destino[0] - 1, destino[1] + 1] ,[destino[0] - 1, destino[1] - 1]]
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
        captura = False
        if (casa_destino.cor != "P") or (casa_origem.peca == None)  or (jogador != self.quem_joga()) or (jogador != casa_origem.peca.cor) or (jogador == "B" and destino[0] > origem[0] and casa_origem.peca.tipo == "N") or (jogador == "P" and destino[0] < origem[0] and casa_origem.peca.tipo == "N") or (destino == origem) or (destino[0] - origem[0] >= 2 or destino[0] - origem[0] <= -2) or (destino[1] - origem[1] >= 2 or destino[1] - origem[1] <= -2):
            print("Movimento inválido!")
            time.sleep(1)
            return None
        
        #Captura
        while (casa_destino.peca != None):
            captura = False
            peca_origem = estado[origem[0]][origem[1]].peca

            #valida se não está capturando a própria peça
            if  (casa_destino.peca.cor == jogador):
                print("Movimento inválido!")
                return None
            elif destino[0] + 1 >= len(estado) or destino[1] + 1 >= len(estado):
                break
            elif (estado[destino[0] + 1][destino[1] + 1].peca == None and origem[0] < destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] + 1]
                captura = True
            elif (estado[destino[0] + 1][destino[1] - 1].peca == None and origem[0] < destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] + 1, destino[1] - 1]
                captura = True

            elif (estado[destino[0] - 1][destino[1] + 1].peca == None and origem[0] > destino[0] and origem[1] < destino[1]):
                estado[destino[0]][destino[1]].peca = None
                destino = [destino[0] - 1, destino[1] + 1]
                captura = True

            elif (estado[destino[0] - 1][destino[1] - 1].peca == None and origem[0] > destino[0] and origem[1] > destino[1]):
                estado[destino[0]][destino[1]].peca = None
                captura = True
                destino = [destino[0] - 1, destino[1] - 1]


            possibilidades = self.calcular_possibilidades(destino)
            nova_casa_origem = estado[destino[0]][destino[1]]         
            casas_possiveis = []
            for possibilidade in possibilidades:
                casa_a_ser_testada = estado[possibilidade[0]][possibilidade[1]]
                if casa_a_ser_testada.peca != None and casa_a_ser_testada.peca.cor != jogador:
                    diff_linha = casa_a_ser_testada.linha - nova_casa_origem.linha
                    diff_coluna = casa_a_ser_testada.coluna - nova_casa_origem.coluna
                    if diff_linha + casa_a_ser_testada.linha >= len(estado) or diff_linha + casa_a_ser_testada.coluna >= len(estado) or diff_linha + casa_a_ser_testada.linha < 0 or diff_linha + casa_a_ser_testada.coluna < 0:
                        break
                    if estado[possibilidade[0] + diff_linha][possibilidade[1] + diff_coluna].peca == None:
                        if (peca_origem.tipo == "N" and possibilidade[0] < nova_casa_origem.linha and peca_origem.cor == "P") or (peca_origem.tipo == "N" and possibilidade[0] > nova_casa_origem.linha and peca_origem.cor == "B"):
                            continue
                        casas_possiveis.append(casa_a_ser_testada)


            if len(casas_possiveis) == 1:
                casa_destino = casas_possiveis[0]
            elif len(casas_possiveis) > 0:
                print("Movimentos possíveis:")
                for movimento in casas_possiveis:
                    print(f"{casas_possiveis.index(movimento) + 1} Linha: {movimento.linha} - Coluna: {movimento.coluna}")
                opt = int(input("Escolha uma opção: "))
                casa_destino = casas_possiveis[opt - 1]

            peca_origem = casa_origem.peca

            if(casa_origem.peca.cor == "P" and destino[0] == 7) or (casa_origem.peca.cor == "B" and destino[0] == 0):
                estado[destino[0]][destino[1]].peca = Peca(tipo="D", cor=peca_origem.cor)
            else:
                estado[destino[0]][destino[1]].peca = casa_origem.peca
            estado[origem[0]][origem[1]].peca = None
            destino = [casa_destino.linha, casa_destino.coluna]
            origem = [nova_casa_origem.linha, nova_casa_origem.coluna]
            casa_origem = nova_casa_origem
        
        if not captura:
            if(casa_origem.peca.cor == "P" and destino[0] == 7) or (casa_origem.peca.cor == "B" and destino[0] == 0):
                estado[destino[0]][destino[1]].peca = Peca(tipo="D", cor=peca_origem.cor)
            else:
                estado[destino[0]][destino[1]].peca = casa_origem.peca
            estado[origem[0]][origem[1]].peca = None
        self.turnos.append(tuple([len(self.turnos) + 1, jogador, origem, destino]))

        novo_no = No(no_pai = no, heuristica=0, estado=estado)
        self.nos.append(novo_no)
        self.table = estado
        return novo_no

        