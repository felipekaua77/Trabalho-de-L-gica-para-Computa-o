from satEncoder import SATEncoder
from puzzleUtilitario import embaralhar, mostrar
from pysat.solvers import Glucose3

final = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

try:
    ini = embaralhar(final, passos=30)
except Exception as e:
    print("Erro ao gerar estado inicial:", e)
    exit(1)

print("Estado inicial:")
mostrar(ini)

max_n = 100
for n in range(1, max_n + 1):
    print(f"Tentando resolver com {n} passos...")

    enc = SATEncoder(n)
    enc.add_ini(ini)
    enc.add_pos()
    enc.add_exc()
    enc.add_acs()
    enc.add_trans()
    enc.add_obj(final)

    solv = Glucose3()
    solv.append_formula(enc.claus)

    if solv.solve():
        modelo = solv.get_model()
        enc.mostrar_sol(modelo)
        print(f"Solução encontrada com {n} passos.")
        break
else:
    print(f"Não foi possível encontrar solução com até {max_n} passos.")