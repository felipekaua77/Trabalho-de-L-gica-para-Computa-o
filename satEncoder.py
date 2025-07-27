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
        # Em cada t, apenas uma ação (C, B, E, D) pode ocorrer
        pass  # TODO

    def adicionar_transicoes(self):
        # Se 0 está em certa posição e a ação é válida,
        # então aplique transição no estado seguinte
        pass  # TODO

    def interpretar_modelo(self, modelo):
        # Lê os inteiros do modelo e interpreta quais ações foram feitas
        # Exibe a sequência de estados e movimentos
        pass  # TODO
