import threading
import queue
import random
import time
import json
from faker import Faker

dados_falsos = Faker('pt_BR')
fila = queue.Queue()
bloqueio = threading.Lock()

def produtor():
    while True:
        with bloqueio:
            for _ in range(1000):
                dados_passagem = {
                    "nome": dados_falsos.name(),
                    "cpf": dados_falsos.cpf(),
                    "data": dados_falsos.date(),
                    "hora": dados_falsos.date_time_this_year().strftime("%d/%m%Y"),
                    "assento": random.randint(1, 100)
                }
                print("Demanda gerada: ")
                for chave, valor, in dados_passagem.items():
                    print(f"{chave}: {valor}")
                print("_" * 20)

                json_dados = json.dumps(dados_passagem)
                fila.put(json_dados)
        time.sleep(3)

def consumidor():
    while True:
        with bloqueio:
            for _ in range(10):
                if not fila.empty():
                    dados = fila.get()
                    fila.task_done()
                    print(f"Demanda consumida: {dados}")
        time.sleep(10)

if __name__ == "__main__":
    thread_produtor = threading.Thread(target=produtor)
    thread_consumidor = threading.Thread(target=consumidor)

    thread_produtor.start()
    thread_consumidor.start()

    thread_produtor.join()
    thread_consumidor.join()