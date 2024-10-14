# import threading
# import queue
# import random
# import time
# import json
# from faker import Faker

# dados_falsos = Faker('pt_BR')
# fila = queue.Queue()
# bloqueio = threading.Lock()

# def fila_de_entrada(max_execucoes=1):
#     # while True:
#     for execucao in range(max_execucoes):
#         cont = 1
#         with bloqueio:
#             for _ in range(20):
#                 dados_passagem = {
#                     "nome": dados_falsos.name(),
#                     "cpf": dados_falsos.cpf(),
#                     "data": dados_falsos.date(),
#                     "hora": dados_falsos.date_time_this_year().strftime("%d/%m%Y"),
#                     "assento": random.randint(1, 100)
#                 }
#                 print(f"{cont}: Demanda gerada: ")
#                 for chave, valor, in dados_passagem.items():
#                     print(f"{chave}: {valor}")
#                 print("_" * 20)

#                 json_dados = json.dumps(dados_passagem)
#                 fila.put(json_dados)
#                 cont += 1
#         time.sleep(3)

# def fila_de_saida(max_execucoes=1):
#     # while True:
#     for execucao in range(max_execucoes):
#         cont = 1
#         with bloqueio:
#             for _ in range(10):
#                 if not fila.empty():
#                     dados = fila.get()
#                     fila.task_done()
#                     print(f"{cont}: Demanda consumida: {dados}")
#                     cont += 1
#         time.sleep(10)

# if __name__ == "__main__":
#     thread_produtor = threading.Thread(target=fila_de_entrada)
#     thread_consumidor = threading.Thread(target=fila_de_saida)

#     thread_produtor.start()
#     thread_consumidor.start()

#     thread_produtor.join()
#     thread_consumidor.join()

# import threading
# import queue
# import random
# import time
# import json
# from faker import Faker

# dados_falsos = Faker('pt_BR')

# # Criando as filas
# fila_entrada = queue.Queue()
# fila_saida = queue.Queue()
# fila1 = queue.Queue
# fila2 = queue.Queue
# fila3 = queue.Queue
# fila4 = queue.Queue

# def demandas_recebidas():

#     cont = 1
#     for _ in range(200):
#         dados_passagem = {
#             "nome": dados_falsos.name(),
#             "cpf": dados_falsos.cpf(),
#             "data": dados_falsos.date(),
#             "hora": dados_falsos.date_time_this_year().strftime("%d/%m/%Y"),
#             "assento": random.randint(1, 100)
#         }
#         print(f"{cont}: Demandas geradas: {dados_passagem}")
        
#         json_dados = json.dumps(dados_passagem)
#         fila_entrada.put(json_dados)
#         cont += 1
#     time.sleep(3)

# def demandas_consumidas():

#     cont = 1
#     for _ in range(3):
#         while not fila_entrada.empty():
#             dados = fila_entrada.get()
#             fila_entrada.task_done()
            
#             fila_saida.put(dados)
#             print(f"{cont}: Demandas consumidas: {dados}")
#             cont += 1
#     time.sleep(10)

# if __name__ == "__main__":
#     demandas_recebidas()
#     print("´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´")
#     print("______________________________________________________________________________________________")
#     demandas_consumidas()

import queue
import random
import time
import json
from faker import Faker

dados_falsos = Faker('pt_BR')

# Criando as filas
fila_entrada = queue.Queue()
fila_saida = queue.Queue()

def demandas_recebidas():
    """
    Gera 200 demandas e as coloca na fila de entrada a cada 3 segundos.
    """
    cont = 1
    for _ in range(200):
        dados_passagem = {
            "nome": dados_falsos.name(),
            "cpf": dados_falsos.cpf(),
            "data": dados_falsos.date(),
            "hora": dados_falsos.date_time_this_year().strftime("%d/%m/%Y"),
            "assento": random.randint(1, 100)
        }
        print(f"{cont}: Demandas geradas: {dados_passagem}")
        
        json_dados = json.dumps(dados_passagem)
        fila_entrada.put(json_dados)  # Coloca na fila de entrada
        cont += 1
    time.sleep(3)  # Simula intervalo de geração de demandas

def demandas_consumidas():
    """
    Processa no máximo 3 demandas a cada 10 segundos e coloca na fila de saída.
    """
    cont = 1
    while True:  # Continua processando indefinidamente
        if not fila_entrada.empty():
            for _ in range(3):  # Consome até 3 demandas por vez
                if not fila_entrada.empty():
                    dados = fila_entrada.get()
                    fila_entrada.task_done()
                    
                    fila_saida.put(dados)  # Move para a fila de saída
                    print(f"{cont}: Demandas consumidas: {dados}")
                    cont += 1
        else:
            print("Nenhuma demanda para consumir no momento.")
        
        time.sleep(10)  # Intervalo de 10 segundos entre os ciclos de consumo

if __name__ == "__main__":
    # Executa o produtor e consumidor em sequência
    demandas_recebidas()
    print("============================================================================================================")
    print("============================================================================================================")
    # O consumidor processa as demandas
    demandas_consumidas()