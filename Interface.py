# Importa as bibliotecas necessárias para interface, lógica do puzzle e SAT solver
import tkinter as tk
from satEncoder import SATEncoder
from puzzleUtilitario import embaralhar
from pysat.solvers import Glucose3

# Classe que representa a interface gráfica do 8-puzzle
class PuzzleInterface:
    def __init__(self, root, estados, acoes):
        self.root = root
        self.estados = estados      # Lista com todos os estados do tabuleiro, do início até a solução
        self.acoes = acoes          # Lista com os movimentos realizados para chegar à solução
        self.passo = 0              # Indica em qual passo da solução estamos

        # Cria uma matriz de labels para desenhar cada célula do tabuleiro na tela
        self.labels = [[None for _ in range(3)] for _ in range(3)]

        # Label para mostrar informações sobre o passo atual ou ação realizada
        self.info = tk.Label(root, text="")
        self.info.grid(row=3, column=0, columnspan=3)

        # Desenha o estado inicial do tabuleiro na interface
        self.draw_board(self.estados[0])

        # Botão para avançar para o próximo passo da solução
        btn_next = tk.Button(root, text="Próximo passo", command=self.next_step)
        btn_next.grid(row=4, column=2)

        # Botão para voltar para o passo anterior da solução
        btn_prev = tk.Button(root, text="Voltar passo", command=self.prev_step)
        btn_prev.grid(row=4, column=0)

    def draw_board(self, estado):
        # Atualiza os labels para mostrar o estado atual do tabuleiro
        for i in range(3):
            for j in range(3):
                val = estado[i][j]
                # Mostra o zero como espaço vazio para facilitar a visualização
                txt = str(val) if val != 0 else " "
                if self.labels[i][j] is None:
                    # Cria o label se ainda não existe
                    self.labels[i][j] = tk.Label(
                        self.root, text=txt, width=4, height=2,
                        font=("Arial", 24), borderwidth=2, relief="groove"
                    )
                    self.labels[i][j].grid(row=i, column=j)
                else:
                    # Atualiza o texto do label existente
                    self.labels[i][j].config(text=txt)

    def next_step(self):
        # Avança para o próximo passo da solução, se possível
        if self.passo < len(self.estados) - 1:
            self.passo += 1
            self.draw_board(self.estados[self.passo])
            # Mostra qual ação foi realizada neste passo
            acao = self.acoes[self.passo-1] if self.passo-1 < len(self.acoes) else ""
            self.info.config(text=f"Passo {self.passo}: {acao}")
        else:
            # Se chegou ao fim, avisa o usuário
            self.info.config(text="Fim da solução!")

    def prev_step(self):
        # Volta para o passo anterior da solução, se possível
        if self.passo > 0:
            self.passo -= 1
            self.draw_board(self.estados[self.passo])
            # Mostra a ação realizada ou indica que é o estado inicial
            acao = self.acoes[self.passo-1] if self.passo-1 >= 0 and self.passo-1 < len(self.acoes) else ""
            if self.passo == 0:
                self.info.config(text="Estado inicial")
            else:
                self.info.config(text=f"Passo {self.passo}: {acao}")

# Função que extrai a sequência de estados e ações do modelo retornado pelo SAT solver
def extrair_solucao(enc, modelo):
    modelo_set = set(v for v in modelo if v > 0)
    estados = []
    acoes = []
    # Mapeia os códigos das ações para nomes mais amigáveis
    acao_map = { 'C': 'Cima', 'B': 'Baixo', 'E': 'Esquerda', 'D': 'Direita' }
    for t in range(0, enc.max_p + 1):
        estado = [[-1 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(9):
                    simb = f"{t}_P_{i}_{j}_{k}"
                    var = enc.var(simb)
                    if var in modelo_set:
                        estado[i][j] = k
        estados.append(estado)
        # Para cada passo, verifica qual ação foi realizada
        if t > 0:
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                var = enc.var(simb)
                if var in modelo_set:
                    acoes.append(acao_map[acao])
    return estados, acoes

# Bloco principal: resolve o puzzle e mostra a interface com o caminho mais curto
if __name__ == "__main__":
    # Define o estado final desejado do puzzle
    final = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    # Gera um estado inicial embaralhado a partir do final
    ini = embaralhar(final, passos=30)
    max_n = 100  # Número máximo de passos para tentar encontrar solução

    # Tenta encontrar a solução ótima (menor número de passos possível)
    for n in range(1, max_n + 1):
        enc = SATEncoder(n)  # Cria codificador SAT para n passos
        enc.add_ini(ini)
        enc.add_pos()
        enc.add_exc()
        enc.add_acs()
        enc.add_trans()
        enc.add_obj(final)
        solv = Glucose3()  # Cria solver SAT
        solv.append_formula(enc.claus)  # Carrega as cláusulas
        if solv.solve():  # Se encontrar solução
            modelo = solv.get_model()
            estados, acoes = extrair_solucao(enc, modelo)
            root = tk.Tk()
            root.title(f"8-Puzzle SAT Solver - {n} passos (ótimo)")
            gui = PuzzleInterface(root, estados, acoes)
            root.mainloop()
            break  # Para no primeiro caminho encontrado (ótimo)
    else:
        print("Não foi possível encontrar solução.")