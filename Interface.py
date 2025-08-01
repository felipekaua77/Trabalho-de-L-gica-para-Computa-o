import tkinter as tk
from satEncoder import SATEncoder
from puzzleUtilitario import embaralhar
from pysat.solvers import Glucose3

class PuzzleGUI:
    def __init__(self, root, estados, acoes):
        self.root = root
        self.estados = estados
        self.acoes = acoes
        self.passo = 0
        self.labels = [[None for _ in range(3)] for _ in range(3)]
        self.info = tk.Label(root, text="")
        self.info.grid(row=3, column=0, columnspan=3)
        self.draw_board(self.estados[0])
        btn = tk.Button(root, text="Próximo passo", command=self.next_step)
        btn.grid(row=4, column=0, columnspan=3)

    def draw_board(self, estado):
        for i in range(3):
            for j in range(3):
                val = estado[i][j]
                txt = str(val) if val != 0 else " "
                if self.labels[i][j] is None:
                    self.labels[i][j] = tk.Label(self.root, text=txt, width=4, height=2, font=("Arial", 24), borderwidth=2, relief="groove")
                    self.labels[i][j].grid(row=i, column=j)
                else:
                    self.labels[i][j].config(text=txt)

    def next_step(self):
        self.passo += 1
        if self.passo < len(self.estados):
            self.draw_board(self.estados[self.passo])
            acao = self.acoes[self.passo-1] if self.passo-1 < len(self.acoes) else ""
            self.info.config(text=f"Passo {self.passo}: {acao}")
        else:
            self.info.config(text="Fim da solução!")

def extrair_solucao(enc, modelo):
    modelo_set = set(v for v in modelo if v > 0)
    estados = []
    acoes = []
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
        if t > 0:
            for acao in ['C', 'B', 'E', 'D']:
                simb = f"{t}_A_{acao}"
                var = enc.var(simb)
                if var in modelo_set:
                    acoes.append(acao_map[acao])
    return estados, acoes

if __name__ == "__main__":
    final = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    ini = embaralhar(final, passos=30)
    enc = SATEncoder(30)
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
        estados, acoes = extrair_solucao(enc, modelo)
        root = tk.Tk()
        root.title("8-Puzzle SAT Solver")
        gui = PuzzleGUI(root, estados, acoes)
        root.mainloop()
    else:
        print("Não foi possível encontrar solução.")