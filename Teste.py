from pysat.solvers import Glucose3
from random import choice, seed
import copy

# Constantes do puzzle
N = 3  # tamanho da grade (3x3)
NUM_PECAS = N * N  # 9 peças (0 a 8)

# Direções possíveis
MOVIMENTOS = {'C': (-1, 0), 'B': (1, 0), 'E': (0, -1), 'D': (0, 1)}

# Mapeamento de variáveis para inteiros
var_map = {}
rev_map = {}
id_counter = 1

def map_var(step, i, j, val):
    global id_counter
    key = f'{step}_{i}_{j}_{val}'
    if key not in var_map:
        var_map[key] = id_counter
        rev_map[id_counter] = key
        id_counter += 1
    return var_map[key]

def encode_pos(step, estado):
    """Gera as cláusulas que codificam uma configuração do tabuleiro"""
    clauses = []
    for i in range(N):
        for j in range(N):
            v = estado[i][j]
            clauses.append([map_var(step, i, j, v)])
    return clauses

def restricoes_unicidade(step):
    """Garante que cada célula tenha exatamente uma peça e vice-versa"""
    clauses = []
    for i in range(N):
        for j in range(N):
            # Pelo menos um valor
            clauses.append([map_var(step, i, j, v) for v in range(NUM_PECAS)])
            # No máximo um valor por posição
            for v1 in range(NUM_PECAS):
                for v2 in range(v1+1, NUM_PECAS):
                    clauses.append([-map_var(step, i, j, v1), -map_var(step, i, j, v2)])
    return clauses

def gerar_estado_final():
    return [[(i * N + j + 1) % NUM_PECAS for j in range(N)] for i in range(N)]

def gerar_estado_inicial(k=20):
    """Aplica k movimentos aleatórios no estado final para gerar o inicial"""
    seed(42)
    estado = gerar_estado_final()
    for _ in range(k):
        i, j = [(i, j) for i in range(N) for j in range(N) if estado[i][j] == 0][0]
        moves = []
        for d, (di, dj) in MOVIMENTOS.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N:
                moves.append((ni, nj))
        ni, nj = choice(moves)
        estado[i][j], estado[ni][nj] = estado[ni][nj], estado[i][j]
    return estado

def transicoes(step):
    """Gera cláusulas que descrevem as possíveis transições entre step e step+1"""
    clauses = []
    for i in range(N):
        for j in range(N):
            for dir, (di, dj) in MOVIMENTOS.items():
                ni, nj = i + di, j + dj
                if 0 <= ni < N and 0 <= nj < N:
                    for v in range(1, NUM_PECAS):
                        c1 = -map_var(step, i, j, 0)
                        c2 = -map_var(step, ni, nj, v)
                        c3 = map_var(step+1, i, j, v)
                        c4 = map_var(step+1, ni, nj, 0)
                        # Apenas a posição do 0 e a peça v trocam
                        stable = []
                        for x in range(N):
                            for y in range(N):
                                if (x, y) != (i, j) and (x, y) != (ni, nj):
                                    for val in range(NUM_PECAS):
                                        stable.append([-map_var(step, x, y, val), map_var(step+1, x, y, val)])
                        clauses.append([c1, c2, c3])
                        clauses.append([c1, c2, c4])
                        clauses.extend(stable)
    return clauses

def imprimir_solucao(modelo, passos):
    for t in range(passos + 1):
        tab = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for v in range(NUM_PECAS):
                    var = map_var(t, i, j, v)
                    if var in modelo:
                        tab[i][j] = v
        print(f"Passo {t}:")
        for linha in tab:
            print(' '.join(str(x) for x in linha))
        print()

def resolver():
    estado_inicial = gerar_estado_inicial(k=20)
    estado_final = gerar_estado_final()
    for passos in range(1, 31):
        solver = Glucose3()
        var_map.clear()
        rev_map.clear()
        global id_counter
        id_counter = 1

        clauses = []
        # Configuração inicial
        clauses += encode_pos(0, estado_inicial)
        # Estado final
        clauses += encode_pos(passos, estado_final)
        # Restrições de unicidade
        for t in range(passos+1):
            clauses += restricoes_unicidade(t)
        # Transições
        for t in range(passos):
            clauses += transicoes(t)

        for c in clauses:
            solver.add_clause(c)

        if solver.solve():
            print(f"\n✔ Solução encontrada com {passos} passos!")
            modelo = solver.get_model()
            modelo = set([l for l in modelo if l > 0])
            imprimir_solucao(modelo, passos)
            return
        else:
            print(f"Tentando com {passos} passos...")

    print("\n❌ Nenhuma solução encontrada até 30 passos.")

if __name__ == "__main__":
    resolver()
