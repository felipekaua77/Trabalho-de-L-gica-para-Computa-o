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
        # Para cada posição (i, j) insira a proposição:
        # 0_P_i_j_k, onde k é o número no estado inicial
        pass  # TODO

    def adicionar_estado_objetivo(self, estado):
        # Adicione proposições  N_P_i_j_k
        pass  # TODO

    def adicionar_regras_posicionamento(self):
        # Cada posição (i,j) em cada t deve conter algum valor
        # (t_P_i_j_0 v t_P_i_j_1 v ... v t_P_i_j_8)
        pass  # TODO

    def adicionar_regras_exclusividade(self):
        # Em t, uma posição (i,j) só pode conter UM valor
        # Se t_P_i_j_k então não t_P_i_j_m para m ≠ k
        pass  # TODO

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
