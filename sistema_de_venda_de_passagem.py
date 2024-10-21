import threading
import queue
import random
import time
import json
from faker import Faker

dados_falsos = Faker('pt_BR')

fila_entrada = queue.Queue()
fila_saida = queue.Queue()
fila1 = queue.Queue(maxsize=20)
fila2 = queue.Queue(maxsize=20)
fila3 = queue.Queue(maxsize=20)
fila4 = queue.Queue(maxsize=20)

lock = threading.Lock()

def demandas_recebidas():
    id = 1
    for _ in range(50):
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
                    print(f"Demanda com ID {dados['ID']} foi colocada na fila {idx + 1}")
            idx = (idx + 1) % 4

        time.sleep(1)

def liberar_fila(fila, nome_fila):
    while True:
        with lock:
            if not fila.empty():
                dados = fila.get()
                fila.task_done()
                
                fila_saida.put(json.dumps(dados))
                print(f"Demanda com ID {dados['ID']} foi liberada da {nome_fila} e colocada na fila de saída.")      
        time.sleep(5)

if __name__ == "__main__":
    thread_receber_demandas = threading.Thread(target=demandas_recebidas)
    thread_distribuir_demandas = threading.Thread(target=distribuir_demandas)

    thread_liberar_fila1 = threading.Thread(target=liberar_fila, args=(fila1, "fila1"))
    thread_liberar_fila2 = threading.Thread(target=liberar_fila, args=(fila2, "fila2"))
    thread_liberar_fila3 = threading.Thread(target=liberar_fila, args=(fila3, "fila3"))
    thread_liberar_fila4 = threading.Thread(target=liberar_fila, args=(fila4, "fila4"))

    thread_receber_demandas.start()
    thread_distribuir_demandas.start()
    thread_liberar_fila1.start()
    thread_liberar_fila2.start()
    thread_liberar_fila3.start()
    thread_liberar_fila4.start()

    thread_receber_demandas.join()
    thread_distribuir_demandas.join()
    thread_liberar_fila1.join()
    thread_liberar_fila2.join()
    thread_liberar_fila3.join()
    thread_liberar_fila4.join()
