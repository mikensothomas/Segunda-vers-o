import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Simulador de Processamento de Demandas")

# Frame para Fila de Entrada
entrada_frame = tk.Frame(root)
entrada_frame.pack(side=tk.TOP)
tk.Label(entrada_frame, text="Fila de Entrada").pack()

# Frame para Filas de Processamento (fila1 a fila4)
processamento_frame = tk.Frame(root)
processamento_frame.pack(side=tk.TOP)
for i in range(1, 5):
    tk.Label(processamento_frame, text=f"Fila {i}").grid(row=i, column=0)
    ttk.Progressbar(processamento_frame, orient="horizontal", length=200, mode="determinate").grid(row=i, column=1)

# Frame para Fila de Saída
saida_frame = tk.Frame(root)
saida_frame.pack(side=tk.TOP)
tk.Label(saida_frame, text="Fila de Saída").pack()

root.mainloop()