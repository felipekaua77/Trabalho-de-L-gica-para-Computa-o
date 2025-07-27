import random
import copy

def gerar_estado_inicial(estado_final, num_movimentos=15):
    atual = copy.deepcopy(estado_final)
    for _ in range(num_movimentos):
        movs = movimentos_validos(atual)
        mov = random.choice(movs)
        atual = aplicar_movimento(atual, mov)
    return atual

def movimentos_validos(estado):
    linha = coluna = None
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                linha, coluna = i, j
    if linha is None or coluna is None:
        raise ValueError("Estado inválido: não encontrou o zero.")
    movimentos = []
    if linha > 0: movimentos.append('C')
    if linha < 2: movimentos.append('B')
    if coluna > 0: movimentos.append('E')
    if coluna < 2: movimentos.append('D')
    return movimentos

def aplicar_movimento(estado, movimento):
    novo = [linha[:]for linha in estado]

    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                linha, coluna = i, j
    if movimento == 'C' and linha > 0:  # Cima
        novo[linha][coluna], novo[linha - 1][coluna] = novo[linha - 1][coluna], novo[linha][coluna]
    elif movimento == 'B' and linha < 2:  # Baixo
        novo[linha][coluna], novo[linha + 1][coluna] = novo[linha + 1][coluna], novo[linha][coluna]
    elif movimento == 'E' and coluna > 0:  # Esquerda
        novo[linha][coluna], novo[linha][coluna - 1] = novo[linha][coluna - 1], novo[linha][coluna]
    elif movimento == 'D' and coluna < 2:  # Direita
        novo[linha][coluna], novo[linha][coluna + 1] = novo[linha][coluna + 1], novo[linha][coluna]
    return novo
        

def print_estado(estado):
    for linha in estado:
        print(' '.join(str(x) for x in linha))
    print()

def print_estado(estado):
    print("+---+---+---+")
    for linha in estado:
        print("| " + " | ".join(str(x) if x != 0 else " " for x in linha) + " |")
        print("+---+---+---+")
    print()