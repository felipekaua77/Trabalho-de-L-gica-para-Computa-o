import random
import copy

def embaralhar(final, passos=15):
    tab = copy.deepcopy(final)
    for _ in range(passos):
        movs = moves(tab)
        mov = random.choice(movs)
        tab = mover(tab, mov)
    return tab

def moves(tab):
    for i in range(3):
        for j in range(3):
            if tab[i][j] == 0:
                x, y = i, j
    movs = []
    if x > 0: movs.append('C')
    if x < 2: movs.append('B')
    if y > 0: movs.append('E')
    if y < 2: movs.append('D')
    return movs

def mover(tab, mov):
    novo = [linha[:] for linha in tab]
    for i in range(3):
        for j in range(3):
            if tab[i][j] == 0:
                x, y = i, j
    if mov == 'C' and x > 0:
        novo[x][y], novo[x-1][y] = novo[x-1][y], novo[x][y]
    elif mov == 'B' and x < 2:
        novo[x][y], novo[x+1][y] = novo[x+1][y], novo[x][y]
    elif mov == 'E' and y > 0:
        novo[x][y], novo[x][y-1] = novo[x][y-1], novo[x][y]
    elif mov == 'D' and y < 2:
        novo[x][y], novo[x][y+1] = novo[x][y+1], novo[x][y]
    return novo

def mostrar(tab):
    print("+---+---+---+")
    for linha in tab:
        print("| " + " | ".join(str(n) for n in linha) + " |")
        print("+---+---+---+")
    print()