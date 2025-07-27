from satEncoder import SATEncoder
from puzzle_utils import gerar_estado_inicial, print_estado, movimentos_validos
from pysat.solvers import Glucose3
import random

# Estado final desejado
estado_final = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

# Gerar estado inicial aplicando movimentos aleatórios com tratamento de exceção
try:
    estado_inicial = gerar_estado_inicial(estado_final, num_movimentos=15)
except Exception as e:
    print("Erro ao gerar estado inicial:", e)
    exit(1)

print("Estado inicial:")
print_estado(estado_inicial)

# Tente encontrar solução com N passos
max_passos = 1000
for n in range(1, max_passos + 1):
    print(f"Tentando resolver com {n} passos...")

    encoder = SATEncoder(n)
    encoder.adicionar_estado_inicial(estado_inicial)
    encoder.adicionar_regras_posicionamento()
    encoder.adicionar_regras_exclusividade()
    encoder.adicionar_acoes()
    encoder.adicionar_transicoes()
    encoder.adicionar_estado_objetivo(estado_final)

    solver = Glucose3()
    solver.append_formula(encoder.clausulas)

    if solver.solve():
        modelo = solver.get_model()
        encoder.interpretar_modelo(modelo)
        print(f"Solução encontrada com {n} passos.")
        break
else:
    print(f"Não foi possível encontrar solução com até {max_passos} passos.")