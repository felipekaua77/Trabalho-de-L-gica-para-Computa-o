from puzzleUtilitario import mostrar 

class SATEncoder:
    def __init__(self, max_p):
        self.max_p = max_p      # maximo de passos
        self.claus = []         # lista de clausulas
        self.vmap = {}          # mapa de variaveis
        self.count = 1          # contador de variaveis

    def var(self, simb):
        if simb not in self.vmap:        # cria variavel se nao existe
            self.vmap[simb] = self.count
            self.count += 1
        return self.vmap[simb]           # retorna o numero da variavel

    def add_ini(self, est):
        for i in range(3):      # cada linha
            for j in range(3):  # cada coluna
                k = est[i][j]   # valor da peca
                simb = f"0_P_{i}_{j}_{k}"  # nome da variavel
                v = self.var(simb)         # pega variavel
                self.claus.append([v])     # adiciona clausula

    def add_obj(self, est):
        t = self.max_p      # passo final
        for i in range(3):
            for j in range(3):
                k = est[i][j]
                simb = f"{t}_P_{i}_{j}_{k}"  # nome da variavel do objetivo
                v = self.var(simb)
                self.claus.append([v])       # adiciona clausula

    def add_pos(self):
        for t in range(self.max_p + 1):      # cada passo
            for i in range(3):
                for j in range(3):
                    clause = []
                    for k in range(9):
                        simb = f"{t}_P_{i}_{j}_{k}"  # nome da variavel pra cada peca
                        clause.append(self.var(simb))
                    self.claus.append(clause)         # tem que ter alguma peca

    def add_exc(self):
        for t in range(self.max_p + 1):     # cada passo
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        for m in range(k + 1, 9):
                            simb1 = f"{t}_P_{i}_{j}_{k}"  # variavel peca k
                            simb2 = f"{t}_P_{i}_{j}_{m}"  # variavel peca m
                            self.claus.append([-self.var(simb1), -self.var(simb2)])  # so pode ter uma peca

    def add_acs(self):
        for t in range(1, self.max_p + 1):    # cada passo (menos o zero)
            acs = []
            for acao in ['C', 'B', 'E', 'D']:  # cada acao possivel
                simb = f"{t}_A_{acao}"         # nome da variavel da acao
                acs.append(self.var(simb))
            self.claus.append(acs)             # tem que ter uma acao
            for i in range(4):
                for j in range(i + 1, 4):
                    self.claus.append([-acs[i], -acs[j]])  # so uma acao por vez

    def add_trans(self):
        for t in range(1, self.max_p + 1):    # cada passo (menos o zero)
            for i in range(3):
                for j in range(3):
                    simb_z = f"{t-1}_P_{i}_{j}_0"  # nome do espaco vazio
                    vz = self.var(simb_z)          # pega variavel do vazio
                    va_c = self.var(f"{t}_A_C")    # acao cima
                    if i == 0:
                        self.claus.append([-va_c, -vz])  # nao pode subir se ta no topo
                    va_b = self.var(f"{t}_A_B")    # acao baixo
                    if i == 2:
                        self.claus.append([-va_b, -vz])  # nao pode descer se ta embaixo
                    va_e = self.var(f"{t}_A_E")    # acao esquerda
                    if j == 0:
                        self.claus.append([-va_e, -vz])  # nao pode ir pra esquerda se ta na borda
                    va_d = self.var(f"{t}_A_D")    # acao direita
                    if j == 2:
                        self.claus.append([-va_d, -vz])  # nao pode ir pra direita se ta na borda
                    
                    # cima
                    if i > 0:
                        va = self.var(f"{t}_A_C")  # acao cima
                        vz_n = self.var(f"{t}_P_{i-1}_{j}_0")  # vazio vai pra cima
                        self.claus.append([-vz, -va, vz_n])    # faz a troca
                        for k in range(1, 9):
                            va_ant = self.var(f"{t-1}_P_{i-1}_{j}_{k}") 
                            va_troc = self.var(f"{t}_P_{i}_{j}_{k}")     
                            self.claus.append([-vz, -va, -va_ant, va_troc])  # troca
                        for x in range(3):
                            for y in range(3):
                                if (x, y) != (i, j) and (x, y) != (i-1, j):  
                                    for k in range(1, 9):
                                        va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")  # valor antigo
                                        va_novo = self.var(f"{t}_P_{x}_{y}_{k}")   # valor novo
                                        self.claus.append([-vz, -va, -va_ant, va_novo])  
                    # baixo
                    if i < 2:
                        va = self.var(f"{t}_A_B")  
                        vz_n = self.var(f"{t}_P_{i+1}_{j}_0")  # vazio vai pra baixo
                        self.claus.append([-vz, -va, vz_n])    
                        for k in range(1, 9):
                            va_ant = self.var(f"{t-1}_P_{i+1}_{j}_{k}")  
                            va_troc = self.var(f"{t}_P_{i}_{j}_{k}")     
                            self.claus.append([-vz, -va, -va_ant, va_troc]) 
                        for x in range(3):
                            for y in range(3):
                                if (x, y) != (i, j) and (x, y) != (i+1, j):  
                                    for k in range(1, 9):
                                        va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")  
                                        va_novo = self.var(f"{t}_P_{x}_{y}_{k}")   
                                        self.claus.append([-vz, -va, -va_ant, va_novo])  
                    # esquerda
                    if j > 0:
                        va = self.var(f"{t}_A_E")  
                        vz_n = self.var(f"{t}_P_{i}_{j-1}_0")  # vazio vai pra esquerda
                        self.claus.append([-vz, -va, vz_n])    
                        for k in range(1, 9):
                            va_ant = self.var(f"{t-1}_P_{i}_{j-1}_{k}")  
                            va_troc = self.var(f"{t}_P_{i}_{j}_{k}")     
                            self.claus.append([-vz, -va, -va_ant, va_troc])  
                        for x in range(3):
                            for y in range(3):
                                if (x, y) != (i, j) and (x, y) != (i, j-1):  
                                    for k in range(1, 9):
                                        va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")  
                                        va_novo = self.var(f"{t}_P_{x}_{y}_{k}")   
                                        self.claus.append([-vz, -va, -va_ant, va_novo])  
                    # direita
                    if j < 2:
                        va = self.var(f"{t}_A_D")  
                        vz_n = self.var(f"{t}_P_{i}_{j+1}_0")  # vazio vai pra direita
                        self.claus.append([-vz, -va, vz_n])    
                        for k in range(1, 9):
                            va_ant = self.var(f"{t-1}_P_{i}_{j+1}_{k}") 
                            va_troc = self.var(f"{t}_P_{i}_{j}_{k}")     
                            self.claus.append([-vz, -va, -va_ant, va_troc])  
                        for x in range(3):
                            for y in range(3):
                                if (x, y) != (i, j) and (x, y) != (i, j+1):  
                                    for k in range(1, 9):
                                        va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")  
                                        va_novo = self.var(f"{t}_P_{x}_{y}_{k}")   
                                        self.claus.append([-vz, -va, -va_ant, va_novo])  
        for i in range(3):      # se nao tem acao, tudo fica igual
            for j in range(3):
                simb_z = f"{t-1}_P_{i}_{j}_0"
                vz = self.var(simb_z)
                acs_vars = []
                if i > 0: acs_vars.append(self.var(f"{t}_A_C"))
                if i < 2: acs_vars.append(self.var(f"{t}_A_B"))
                if j > 0: acs_vars.append(self.var(f"{t}_A_E"))
                if j < 2: acs_vars.append(self.var(f"{t}_A_D"))
                if acs_vars:
                    claus_acs_neg = [-v for v in acs_vars]
                    for x in range(3):
                        for y in range(3):
                            for k in range(9):
                                va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")
                                va_novo = self.var(f"{t}_P_{x}_{y}_{k}")
                                self.claus.append(claus_acs_neg + [-va_ant, va_novo])  

    def mostrar_sol(self, modelo):
        modelo_set = set(v for v in modelo if v > 0)     # pega variaveis verdadeiras
        acao_map = { 'C': 'cima', 'B': 'baixo', 'E': 'esquerda', 'D': 'direita' }  # isso define os nomes das acoes
        for t in range(1, self.max_p + 1):
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                v = self.var(simb)
                if v in modelo_set:  
                    print(f"passo {t}: {acao_map[acao]}")
            est = [[-1 for _ in range(3)] for _ in range(3)]  # cria o tabuleiro vazio 
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        simb_est = f"{t}_P_{i}_{j}_{k}"
                        v_est = self.var(simb_est)
                        if v_est in modelo_set:  # se a peca ta aqui
                            est[i][j] = k
            print("estado apos passo", t)
            mostrar(est)  # mostra o tabuleiro