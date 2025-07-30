import random
import copy

def embaralhar(final, passos=15):       # faz uma copia do estado final
    tab = copy.deepcopy(final)
    for _ in range(passos):       # embaralha a partir da copia aleatoriamente o tabuleiro
        movs = moves(tab)         # pega movimentos possíveis
        mov = random.choice(movs) # escolhe um movimento aleatorio
        tab = mover(tab, mov)     # aplica o movimento
    return tab

def moves(tab):     # encontra a posição do espaço sem nada
    for i in range(3):
        for j in range(3):
            if tab[i][j] == 0:
                x, y = i, j
    movs = []       # adiciona movimentos possiveis com base na posição do 0
    if x > 0: movs.append('C')   # move para cima
    if x < 2: movs.append('B')   # move para baixo
    if y > 0: movs.append('E')   # move para esquerda
    if y < 2: movs.append('D')   # move para direita
    return movs

def mover(tab, mov):      # clona o o tabuleiro para aplicar o movimento
    novo = [linha[:] for linha in tab]   
    for i in range(3):   # encontra a posição do espaço sem nenhuma peça
        for j in range(3):
            if tab[i][j] == 0:
                x, y = i, j
    if mov == 'C' and x > 0:     # troca o espaço sem nada com o espaço do lado
        novo[x][y], novo[x-1][y] = novo[x-1][y], novo[x][y]
    elif mov == 'B' and x < 2:
        novo[x][y], novo[x+1][y] = novo[x+1][y], novo[x][y]
    elif mov == 'E' and y > 0:
        novo[x][y], novo[x][y-1] = novo[x][y-1], novo[x][y]
    elif mov == 'D' and y < 2:
        novo[x][y], novo[x][y+1] = novo[x][y+1], novo[x][y]
    return novo

def mostrar(tab):       # mostra o tabuleiro no terminal
    print("+---+---+---+")
    for linha in tab:
        print("| " + " | ".join(str(n) for n in linha) + " |")
        print("+---+---+---+")
    print()  # organização