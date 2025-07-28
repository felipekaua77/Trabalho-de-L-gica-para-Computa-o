from satEncoder import SATEncoder
from puzzleUtilitario import embaralhar, mostrar
from pysat.solvers import Glucose3

final = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

try:
    ini = embaralhar(final, passos=30) # Embaralha o estado final para criar um estado inicial
except Exception as e:
    print("Erro ao gerar estado inicial:", e)
    exit(1)

print("Estado inicial:")
mostrar(ini)

max_n = 100 
for n in range(1, max_n + 1):
    print(f"Tentando resolver com {n} passos...")

    encoder = SATEncoder(n) 
    encoder.add_ini(ini)
    encoder.add_pos()
    encoder.add_exc()
    encoder.add_acs()
    encoder.add_trans()
    encoder.add_obj(final)

    solver = Glucose3()
    solver.append_formula(encoder.claus)

    if solver.solve():
        modelo = solver.get_model()
        encoder.mostrar_sol(modelo)
        print(f"Solução encontrada com {n} passos.")
        break
else:
    print(f"Não foi possível encontrar solução com até {max_n} passos.")