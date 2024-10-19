# import threading
# import queue
# import random
# import time
# import json
# from faker import Faker

# dados_falsos = Faker('pt_BR')

# fila_entrada = queue.Queue()
# fila_saida = queue.Queue()
# fila1 = queue.Queue(maxsize=20)
# fila2 = queue.Queue(maxsize=20)
# fila3 = queue.Queue(maxsize=20)
# fila4 = queue.Queue(maxsize=20)

# lock = threading.Lock()

# def demandas_recebidas():
#     id = 1
#     for _ in range(4):
#         dados_passagem = {
#             "ID": id,
#             "nome": dados_falsos.name(),
#             "cpf": dados_falsos.cpf(),
#             "data": dados_falsos.date_time_this_year().strftime("%d/%m/%Y"),
#             "hora": dados_falsos.time(),
#             "assento": random.randint(1, 100)
#         }

#         json_dados = json.dumps(dados_passagem)
        
#         with lock:
#             fila_entrada.put(json_dados)
        
#         print(f"{dados_passagem['nome']} é a {dados_passagem['ID']}a pessoa na fila de entrada.")
#         for chave, valor in dados_passagem.items():
#             print(f"{chave}: {valor}")
#         print("\n")
#         id += 1
    
#     time.sleep(3)

# def distribuir_demandas():
#     filas = [fila1, fila2, fila3, fila4]
#     idx = 0
#     while True:
#         if not fila_entrada.empty():
#             with lock:
#                 dados = fila_entrada.get()
#                 fila_entrada.task_done()

#             dados = json.loads(dados)

#             with lock:
#                 if filas[idx].qsize() < 20:
#                     filas[idx].put(dados)
#                     print(f"{dados['nome']} com ID {dados['ID']} está na fila {idx + 1}")
#             idx = (idx + 1) % 4

#         time.sleep(1)

# def liberar_fila(fila, nome_fila):
#     while True:
#         with lock:
#             if not fila.empty():
#                 dados = fila.get()
#                 fila.task_done()
                
#                 fila_saida.put(json.dumps(dados))
#                 print(f"Demanda ID {dados['ID']} liberada da {nome_fila} e foi para fila de saída.")
        
#         time.sleep(3) 

# def consumir_fila_saida():
#     while True:
#         if not fila_saida.empty():
#             with lock:
#                 dados = fila_saida.get() 
#                 fila_saida.task_done()
                
#                 dados = json.loads(dados)
        
#         time.sleep(5) 

# if __name__ == "__main__":

#     thread_receber_demandas = threading.Thread(target=demandas_recebidas)
#     thread_distribuir_demandas = threading.Thread(target=distribuir_demandas)
    
#     thread_liberar_fila1 = threading.Thread(target=liberar_fila, args=(fila1, "fila1"))
#     thread_liberar_fila2 = threading.Thread(target=liberar_fila, args=(fila2, "fila2"))
#     thread_liberar_fila3 = threading.Thread(target=liberar_fila, args=(fila3, "fila3"))
#     thread_liberar_fila4 = threading.Thread(target=liberar_fila, args=(fila4, "fila4"))
    
#     thread_consumir_fila_saida = threading.Thread(target=consumir_fila_saida)

#     thread_receber_demandas.start()
#     thread_distribuir_demandas.start()
    
#     thread_liberar_fila1.start()
#     thread_liberar_fila2.start()
#     thread_liberar_fila3.start()
#     thread_liberar_fila4.start()
    
#     thread_consumir_fila_saida.start()

#     thread_receber_demandas.join()
#     thread_distribuir_demandas.join()
#     thread_liberar_fila1.join()
#     thread_liberar_fila2.join()
#     thread_liberar_fila3.join()
#     thread_liberar_fila4.join()
#     thread_consumir_fila_saida.join()

import threading
import queue
import random
import time
import json
from faker import Faker

dados_falsos = Faker('pt_BR')

# Filas
fila_entrada = queue.Queue()
fila_saida = queue.Queue()
fila1 = queue.Queue(maxsize=20)
fila2 = queue.Queue(maxsize=20)
fila3 = queue.Queue(maxsize=20)
fila4 = queue.Queue(maxsize=20)

# Lock para controlar as seções críticas
lock = threading.Lock()

def demandas_recebidas():
    id = 1
    while True:
        for _ in range(4):  # Simulando 4 rodadas de 20 demandas a cada 3 segundos
            dados_passagem = {
                "ID": id,
                "nome": dados_falsos.name(),
                "cpf": dados_falsos.cpf(),
                "data": dados_falsos.date_time_this_year().strftime("%d/%m/%Y"),
                "hora": dados_falsos.time(),
                "assento": random.randint(1, 100)
            }

            json_dados = json.dumps(dados_passagem)
            
            with lock:
                fila_entrada.put(json_dados)
            
            print(f"{dados_passagem['nome']} é a {dados_passagem['ID']}a pessoa na fila de entrada.")
            for chave, valor in dados_passagem.items():
                print(f"{chave}: {valor}")
            print("\n")
            id += 1

        time.sleep(3)

def distribuir_demandas():
    filas = [fila1, fila2, fila3, fila4]
    idx = 0
    while True:
        if not fila_entrada.empty():
            with lock:
                dados = fila_entrada.get()
                fila_entrada.task_done()

            dados = json.loads(dados)

            with lock:
                if filas[idx].qsize() < 20:
                    filas[idx].put(dados)
                    print(f"{dados['nome']} com ID {dados['ID']} foi colocada na fila {idx + 1}")
            idx = (idx + 1) % 4  # Alterna entre as filas 1, 2, 3 e 4

        time.sleep(1)

def liberar_fila(fila, nome_fila):
    while True:
        with lock:
            if not fila.empty():
                dados = fila.get()
                fila.task_done()
                
                fila_saida.put(json.dumps(dados))  # Manda a demanda para a fila de saída
                # print(f"Demanda ID {dados['ID']} foi atendida da {nome_fila} e foi para a fila de saída.")
        
        time.sleep(3)  # Simula liberar uma demanda por vez a cada 3 segundos

# def consumir_fila_saida():
#     while True:
#         if not fila_saida.empty():
#             with lock:
#                 dados = fila_saida.get()  # Pega uma demanda da fila de saída
#                 fila_saida.task_done()
                
#                 dados = json.loads(dados)
#                 print(f"Demanda com ID {dados['ID']} está na fila de saída")
        
#         time.sleep(5)  # Simula o tempo de processamento da demanda

def consumir_fila_saida():
    saida = []  # Lista para armazenar as demandas
    while True:
        if not fila_saida.empty():
            with lock:
                dados = fila_saida.get()  # Pega a demanda da fila de saída
                fila_saida.task_done()
                
                dados = json.loads(dados)  # Converte de JSON string para dicionário
                saida.append(dados)  # Adiciona à lista de saída

        # Imprime a lista ordenada por ID
        if saida:
            saida.sort(key=lambda x: x['ID'])  # Ordena a lista pela chave 'ID'
            for demanda in saida:
                print(f"Demanda com ID {demanda['ID']} está na fila de saída")  # Imprime cada demanda
            saida.clear()  # Limpa a lista após imprimir

        time.sleep(5)  # Espera antes de continuar

if __name__ == "__main__":
    # Criando as threads para cada fila
    thread_receber_demandas = threading.Thread(target=demandas_recebidas)
    thread_distribuir_demandas = threading.Thread(target=distribuir_demandas)
    
    thread_liberar_fila1 = threading.Thread(target=liberar_fila, args=(fila1, "fila1"))
    thread_liberar_fila2 = threading.Thread(target=liberar_fila, args=(fila2, "fila2"))
    thread_liberar_fila3 = threading.Thread(target=liberar_fila, args=(fila3, "fila3"))
    thread_liberar_fila4 = threading.Thread(target=liberar_fila, args=(fila4, "fila4"))

    thread_consumir_fila_saida = threading.Thread(target=consumir_fila_saida)

    thread_receber_demandas.start()
    thread_distribuir_demandas.start()

    thread_liberar_fila1.start()
    thread_liberar_fila2.start()
    thread_liberar_fila3.start()
    thread_liberar_fila4.start()

    thread_consumir_fila_saida.start()

    # Aguardando todas as threads finalizarem (nunca finalizam na prática)
    thread_receber_demandas.join()
    thread_distribuir_demandas.join()
    thread_liberar_fila1.join()
    thread_liberar_fila2.join()
    thread_liberar_fila3.join()
    thread_liberar_fila4.join()
    thread_consumir_fila_saida.join()
