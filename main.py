from satEncoder import SATEncoder                       
from puzzleUtilitario import embaralhar, mostrar        
from pysat.solvers import Glucose3                      

final = [                                               # define o estado final desejado
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

try:
    ini = embaralhar(final, passos=30)                  # gera estado inicial com 30 movimentos validos
except Exception as e:
    print("Erro ao gerar estado inicial:", e)           # se der erro na geracao, mostra e sai
    exit(1)

print("Estado inicial:")
mostrar(ini)                                            # mostra o estado inicial no terminal

max_n = 100                                             # maximo de passos
for n in range(1, max_n + 1):                           # tenta encontrar solucao de 1 ate 100 passos
    print(f"Tentando resolver com {n} passos...")

    enc = SATEncoder(n)                                 # cria o codificador sat para n passos
    enc.add_ini(ini)                                    # adiciona o estado inicial
    enc.add_pos()                                       # garante que cada posicao tem algum numero
    enc.add_exc()                                       # garante exclusividade de numeros por posicao
    enc.add_acs()                                       # adiciona acoes possiveis por passo
    enc.add_trans()                                     # adiciona as transicoes entre estados
    enc.add_obj(final)                                  # adiciona a meta como estado objetivo

    solv = Glucose3()                                   # cria o solver glucose3
    solv.append_formula(enc.claus)                      # carrega as clausulas no solver

    if solv.solve():                                    # se encontrar solucao satisfazendo as clausulas
        modelo = solv.get_model()                       # extrai o modelo
        enc.mostrar_sol(modelo)                         # mostra a sequencia de acoes e estados
        print(f"Solução encontrada com {n} passos.")    # mostra quantos passos foram usados
        break
else:
    print(f"Não foi possível encontrar solução com até {max_n} passos.")  # se nao achar solucao
