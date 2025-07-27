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
    # Retorna lista de movimentos possíveis (C, B, E, D)
    pass  # TODO

def aplicar_movimento(estado, movimento):
    # Move o 0 conforme o movimento e retorna novo estado
    pass  # TODO

def print_estado(estado):
    for linha in estado:
        print(" ".join(str(n) if n != 0 else " " for n in linha))
    print()
