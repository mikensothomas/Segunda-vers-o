import sys
import threading
import queue
import random
import time
from faker import Faker
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QProgressBar, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
from PyQt5.QtCore import QTimer

# Dados falsos para simulação
dados_falsos = Faker('pt_BR')

# Filas para simulação
fila_entrada = queue.Queue()
fila_saida = queue.Queue()
filas_processamento = [queue.Queue(maxsize=10) for _ in range(4)]
# Contadores de demandas em cada fila de processamento
contadores_filas = [0] * 4

# Função para gerar dados de passagem
def gerar_dados_passagem(id):
    data_atual = date.today()
    dias_aleatorios = random.randrange(365)
    data_em_texto = (data_atual + timedelta(days=dias_aleatorios)).strftime("%d/%m/%Y")
    return {
        "ID": id,
        "nome": dados_falsos.name(),
        "cpf": dados_falsos.cpf(),
        "data": data_em_texto,
        "hora": dados_falsos.time(),
        "assento": random.randint(1, 100)
    }

# Funções de processamento paralelo
def demandas_recebidas():
    id = 1
    for _ in range(20):
        dados_passagem = gerar_dados_passagem(id)
        fila_entrada.put(dados_passagem)
        id += 1
        time.sleep(0.01)  # Intervalo reduzido para garantir atualizações frequentes

def distribuir_demandas():
    idx = 0
    while True:
        if not fila_entrada.empty():
            dados = fila_entrada.get()
            fila_entrada.task_done()
            filas_processamento[idx].put(dados)
            contadores_filas[idx] += 1  # Incrementa o contador da fila correspondente
            idx = (idx + 1) % 4
        time.sleep(1)

def liberar_fila(fila, fila_saida, index):
    while True:
        if not fila.empty():
            dados = fila.get()
            fila.task_done()
            fila_saida.put(dados)
            contadores_filas[index] -= 1  # Decrementa o contador da fila correspondente
        time.sleep(10)

# Interface Gráfica em PyQt5
class PassagensUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulação de Compra de Passagens Aéreas")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principal
        main_layout = QVBoxLayout()

        # Configuração da tabela de entrada com scroll vertical
        self.tabela_entrada = QTableWidget()
        self.tabela_entrada.setColumnCount(6)  # Alterado para 6 colunas
        self.tabela_entrada.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Data", "Hora", "Assento"])  # Ajustado para incluir colunas adicionais
        self.tabela_entrada.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        entrada_scroll = QScrollArea()
        entrada_scroll.setWidget(self.tabela_entrada)
        entrada_scroll.setWidgetResizable(True)
        entrada_scroll.setFixedHeight(150)  # Altura fixa para exibir apenas parte da tabela e permitir scroll
        main_layout.addWidget(QLabel("Fila de Entrada"))
        main_layout.addWidget(entrada_scroll)

        # Barras de progresso das filas de processamento
        self.barras_filas = []
        self.labels_filas = []  # Para armazenar labels de contagem
        for i in range(4):
            barra = QProgressBar()
            barra.setMaximum(10)  # Máximo de 10 demandas por fila
            barra.setValue(0)
            label = QLabel(f"Fila de Processamento {i+1} - Demandas: {contadores_filas[i]}")
            main_layout.addWidget(label)
            main_layout.addWidget(barra)
            self.labels_filas.append(label)
            self.barras_filas.append(barra)

        # Configuração da tabela de saída com scroll vertical
        self.tabela_saida = QTableWidget()
        self.tabela_saida.setColumnCount(6)  # Alterado para 6 colunas
        self.tabela_saida.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Data", "Hora", "Assento"])  # Ajustado para incluir colunas adicionais
        self.tabela_saida.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        saida_scroll = QScrollArea()
        saida_scroll.setWidget(self.tabela_saida)
        saida_scroll.setWidgetResizable(True)
        saida_scroll.setFixedHeight(150)
        main_layout.addWidget(QLabel("Fila de Saída"))
        main_layout.addWidget(saida_scroll)

        # Timer para atualização da interface
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(1000)  # Atualização a cada segundo

        # Definir layout principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def atualizar_interface(self):
        # Atualizar a tabela de entrada
        self.tabela_entrada.setRowCount(fila_entrada.qsize())
        for i, item in enumerate(list(fila_entrada.queue)):
            self.tabela_entrada.setItem(i, 0, QTableWidgetItem(str(item["ID"])))
            self.tabela_entrada.setItem(i, 1, QTableWidgetItem(item["nome"]))
            self.tabela_entrada.setItem(i, 2, QTableWidgetItem(item["cpf"]))
            self.tabela_entrada.setItem(i, 3, QTableWidgetItem(item["data"]))
            self.tabela_entrada.setItem(i, 4, QTableWidgetItem(item["hora"]))
            self.tabela_entrada.setItem(i, 5, QTableWidgetItem(str(item["assento"])))

        # Atualizar as barras de progresso das filas de processamento
        for i, fila in enumerate(filas_processamento):
            self.barras_filas[i].setValue(fila.qsize())
            # Atualizar a contagem de demandas na interface
            self.labels_filas[i].setText(f"Fila de Processamento {i+1} - Demandas: {contadores_filas[i]}")

        # Atualizar a tabela de saída
        self.tabela_saida.setRowCount(fila_saida.qsize())
        for i, item in enumerate(list(fila_saida.queue)):
            self.tabela_saida.setItem(i, 0, QTableWidgetItem(str(item["ID"])))
            self.tabela_saida.setItem(i, 1, QTableWidgetItem(item["nome"]))
            self.tabela_saida.setItem(i, 2, QTableWidgetItem(item["cpf"]))
            self.tabela_saida.setItem(i, 3, QTableWidgetItem(item["data"]))
            self.tabela_saida.setItem(i, 4, QTableWidgetItem(item["hora"]))
            self.tabela_saida.setItem(i, 5, QTableWidgetItem(str(item["assento"])))

# Função principal
if __name__ == "__main__":
    # Iniciar threads de processamento
    threading.Thread(target=demandas_recebidas, daemon=True).start()
    threading.Thread(target=distribuir_demandas, daemon=True).start()
    for i, fila in enumerate(filas_processamento):
        threading.Thread(target=liberar_fila, args=(fila, fila_saida, i), daemon=True).start()

    # Iniciar aplicação gráfica
    app = QApplication(sys.argv)
    janela = PassagensUI()
    janela.show()
    sys.exit(app.exec_())