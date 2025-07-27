class SATEncoder:
    def __init__(self, max_passos):
        self.max_passos = max_passos
        self.clausulas = []
        self.varmap = {}
        self.counter = 1

    def get_var(self, simb):
        if simb not in self.varmap:
            self.varmap[simb] = self.counter
            self.counter += 1
        return self.varmap[simb]

    def adicionar_estado_inicial(self, estado):
        for i in range(3):
            for j in range(3):
                k = estado[i][j]
                simb = f"0_P_{i}_{j}_{k}"
                var = self.get_var(simb)
                self.clausulas.append([var])
        

    def adicionar_estado_objetivo(self, estado):
        t = self.max_passos
        for i in range(3):
            for j in range(3):
                k = estado[i][j]
                simb = f"{t}_P_{i}_{j}_{k}"
                var = self.get_var(simb)
                self.clausulas.append([var])

    def adicionar_regras_posicionamento(self):
        for t in range(self.max_passos + 1):
            for i in range(3):
                for j in range(3):
                    clause = []
                    for k in range(9):
                        simb = f"{t}_P_{i}_{j}_{k}"
                        clause.append(self.get_var(simb))
                    self.clausulas.append(clause)

    def adicionar_regras_exclusividade(self):
        for t in range(self.max_passos + 1):
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        for m in range(k + 1, 9):
                            simb1 = f"{t}_P_{i}_{j}_{k}"
                            simb2 = f"{t}_P_{i}_{j}_{m}"
                            var1 = self.get_var(simb1)
                            var2 = self.get_var(simb2)
                            self.clausulas.append([-self.get_var(simb1), -self.get_var(simb2)])

    def adicionar_acoes(self):
        for t in range(1, self.max_passos + 1):
            acoes = []
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                acoes.append(self.get_var(simb))

                self.clausulas.append(acoes)

                for i in range(4):
                    for j in range(i + 1, 4):
                        self.clausulas.append([-acoes[i], -acoes[j]])

    def adicionar_transicoes(self):
        for t in range(1, self.max_passos + 1):
            for i in range(3):
                for j in range(3):
                    simb_zero = f"{t-1}_P_{i}_{j}_0"
                    var_zero = self.get_var(simb_zero)
                    # Cima
                    if i > 0:
                        var_acao = self.get_var(f"{t}_A_C")
                        var_novo_zero = self.get_var(f"{t}_P_{i-1}_{j}_0")
                        self.clausulas.append([-var_zero, -var_acao, var_novo_zero])
                        for k in range(1, 9):
                            var_antigo = self.get_var(f"{t-1}_P_{i-1}_{j}_{k}")
                            var_trocado = self.get_var(f"{t}_P_{i}_{j}_{k}")
                            self.clausulas.append([-var_zero, -var_acao, -var_antigo, var_trocado])
                    # Baixo
                    if i < 2:
                        var_acao = self.get_var(f"{t}_A_B")
                        var_novo_zero = self.get_var(f"{t}_P_{i+1}_{j}_0")
                        self.clausulas.append([-var_zero, -var_acao, var_novo_zero])
                        for k in range(1, 9):
                            var_antigo = self.get_var(f"{t-1}_P_{i+1}_{j}_{k}")
                            var_trocado = self.get_var(f"{t}_P_{i}_{j}_{k}")
                            self.clausulas.append([-var_zero, -var_acao, -var_antigo, var_trocado])
                    # Esquerda
                    if j > 0:
                        var_acao = self.get_var(f"{t}_A_E")
                        var_novo_zero = self.get_var(f"{t}_P_{i}_{j-1}_0")
                        self.clausulas.append([-var_zero, -var_acao, var_novo_zero])
                        for k in range(1, 9):
                            var_antigo = self.get_var(f"{t-1}_P_{i}_{j-1}_{k}")
                            var_trocado = self.get_var(f"{t}_P_{i}_{j}_{k}")
                            self.clausulas.append([-var_zero, -var_acao, -var_antigo, var_trocado])
                    # Direita
                    if j < 2:
                        var_acao = self.get_var(f"{t}_A_D")
                        var_novo_zero = self.get_var(f"{t}_P_{i}_{j+1}_0")
                        self.clausulas.append([-var_zero, -var_acao, var_novo_zero])
                        for k in range(1, 9):
                            var_antigo = self.get_var(f"{t-1}_P_{i}_{j+1}_{k}")
                            var_trocado = self.get_var(f"{t}_P_{i}_{j}_{k}")
                            self.clausulas.append([-var_zero, -var_acao, -var_antigo, var_trocado])

    def interpretar_modelo(self, modelo):
        modelo_set = set(v for v in modelo if v > 0)  # Apenas variáveis verdadeiras
        acao_map = { 'C': 'Cima', 'B': 'Baixo', 'E': 'Esquerda', 'D': 'Direita' }
        for t in range(1, self.max_passos + 1):
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                var = self.get_var(simb)
                if var in modelo_set:
                    print(f"Passo {t}: {acao_map[acao]}")
            # Reconstruir e mostrar o estado do tabuleiro nesse passo
            estado = [[-1 for _ in range(3)] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    for k in range(9):
                        simb_estado = f"{t}_P_{i}_{j}_{k}"
                        var_estado = self.get_var(simb_estado)
                        if var_estado in modelo_set:
                            estado[i][j] = k
            print("Estado:")
            for linha in estado:
                print(linha)