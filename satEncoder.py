from puzzleUtilitario import mostrar

class SATEncoder:
    def __init__(self, max_p):
        # inicializa o codificador, guarda o maximo de passos, as clausulas, o mapa de variaveis e um contador
        self.max_p = max_p
        self.claus = []
        self.vmap = {}
        self.count = 1

    def var(self, simb):
        # pega o numero da variavel, se nao tem ainda, cria uma nova
        if simb not in self.vmap:
            self.vmap[simb] = self.count
            self.count += 1
        return self.vmap[simb]

    def add_ini(self, est):
        # adiciona as clausulas do estado inicial, cada posicao do tabuleiro
        for i in range(3):
            for j in range(3):
                k = est[i][j]
                simb = f"0_P_{i}_{j}_{k}"
                v = self.var(simb)
                self.claus.append([v])

    def add_obj(self, est):
        # adiciona as clausulas do objetivo, cada posicao do tabuleiro no ultimo passo
        t = self.max_p
        for i in range(3):
            for j in range(3):
                k = est[i][j]
                simb = f"{t}_P_{i}_{j}_{k}"
                v = self.var(simb)
                self.claus.append([v])

    def add_pos(self):
        # garante que cada posicao do tabuleiro tem alguma celula em cada passo
        for t in range(self.max_p + 1):
            for i in range(3):
                for j in range(3):
                    clause = []
                    for k in range(9):
                        simb = f"{t}_P_{i}_{j}_{k}"
                        clause.append(self.var(simb))
                    self.claus.append(clause)

    def add_exc(self):
        # garante que cada posicao tem so uma celula, exclusividade
        for t in range(self.max_p + 1):
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        for m in range(k + 1, 9):
                            simb1 = f"{t}_P_{i}_{j}_{k}"
                            simb2 = f"{t}_P_{i}_{j}_{m}"
                            self.claus.append([-self.var(simb1), -self.var(simb2)])

    def add_acs(self):
        # adiciona as clausulas das acoes, so pode fazer uma por vez
        for t in range(1, self.max_p + 1):
            acs = []
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                acs.append(self.var(simb))
            self.claus.append(acs)
            for i in range(4):
                for j in range(i + 1, 4):
                    self.claus.append([-acs[i], -acs[j]])

    def add_trans(self):
        # adiciona as clausulas de transicao, como o tabuleiro muda com cada acao
        for t in range(1, self.max_p + 1):
            for i in range(3):
                for j in range(3):
                    simb_z = f"{t-1}_P_{i}_{j}_0"
                    vz = self.var(simb_z)
                    # pre-condicoes pra cada acao
                    va_c = self.var(f"{t}_A_C")
                    if i == 0:
                        self.claus.append([-va_c, -vz])
                    va_b = self.var(f"{t}_A_B")
                    if i == 2:
                        self.claus.append([-va_b, -vz])
                    va_e = self.var(f"{t}_A_E")
                    if j == 0:
                        self.claus.append([-va_e, -vz])
                    va_d = self.var(f"{t}_A_D")
                    if j == 2:
                        self.claus.append([-va_d, -vz])
                    # cima
                    if i > 0:
                        va = self.var(f"{t}_A_C")
                        vz_n = self.var(f"{t}_P_{i-1}_{j}_0")
                        self.claus.append([-vz, -va, vz_n])
                        for k in range(1, 9):
                            va_ant = self.var(f"{t-1}_P_{i-1}_{j}_{k}")
                            va_troc = self.var(f"{t}_P_{i}_{j}_{k}")
                            self.claus.append([-vz, -va, -va_ant, va_troc])
                        for x in range(3):
                            for y in range(3):
                                if (x, y) != (i, j) and (x, y) != (i-1, j):
                                    for k in range(1, 9):
                                        va_ant = self.var(f"{t-1}_P_{x}_{y}_{k}")
                                        va_novo = self.var(f"{t}_P_{x}_{y}_{k}")
                                        self.claus.append([-vz, -va, -va_ant, va_novo])
                    # baixo
                    if i < 2:
                        va = self.var(f"{t}_A_B")
                        vz_n = self.var(f"{t}_P_{i+1}_{j}_0")
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
                        vz_n = self.var(f"{t}_P_{i}_{j-1}_0")
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
                        vz_n = self.var(f"{t}_P_{i}_{j+1}_0")
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
        # se nao tem acao, o estado repete igual, muda nada
        for i in range(3):
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
        # mostra a solucao, cada passo e estado do tabuleiro
        modelo_set = set(v for v in modelo if v > 0)
        acao_map = { 'C': 'cima', 'B': 'baixo', 'E': 'esquerda', 'D': 'direita' }
        for t in range(1, self.max_p + 1):
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                v = self.var(simb)
                if v in modelo_set:
                    print(f"passo {t}: {acao_map[acao]}")
            est = [[-1 for _ in range(3)] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        simb_est = f"{t}_P_{i}_{j}_{k}"
                        v_est = self.var(simb_est)
                        if v_est in modelo_set:
                            est[i][j] = k
            print("estado apos passo", t)
            mostrar(est)