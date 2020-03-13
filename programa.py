import threading
import time
import queue
import concurrent.futures

def costuraMangas(blockMangas, canastaMangas):
    if not canastaMangas.full():
        canastaMangas.put("M")
        print("mangas: ", canastaMangas)
        time.sleep(1)
    else:
        blockMangas.acquire()

def costuraCuerpo(blockCuerpo, canastaCuerpos):
    if not canastaCuerpos.full():
        canastaCuerpos.put("C")
        print("cuerpo: ", canastaCuerpos)
        time.sleep(1)
    else:
        blockCuerpo.acquire()

def costuraEnsamble(blockMangas, blockCuerpo, canastaMangas, canastaCuerpos):
    if not canastaMangas.full() and not canastaCuerpos.full():
        canastaMangas.get()
        canastaMangas.get()
        canastaCuerpos.get()
        print("ensamblado")
        time.sleep(1)
        try:
            blockMangas.release()
            blockCuerpo.release()
        except:
            print("0")

def foo(bar):
    print('hello {}'.format(bar))
    return 'foo'

if __name__ == '__main__':

    limite = 10
    threads = []  # Arreglo hilos
    hilo_terminado = True
    canastaMangas = queue.Queue(limite)
    canastaCuerpos = queue.Queue(limite)
    blockMangas = threading.Lock()
    blockCuerpo = threading.Lock()

    while True:
        if threads[0] is None:
            threads.append(threading.Thread(target = costuraMangas, args=(blockMangas, canastaMangas))) # Lanzamos un hilo
            threads[0].start()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(foo, 'world!')
                return_value = future.result()
                print(return_value)
        threads.append(threading.Thread(target = costuraCuerpo, args=(blockCuerpo, canastaCuerpos)))  # Lanzamos un hilo
        threads.append(threading.Thread(target =  costuraEnsamble, args=(blockMangas, blockCuerpo, canastaMangas, canastaCuerpos)))  # Lanzamos un hilo

    for t in threads:
        t.start()

    while (not hilo_terminado):  # Espera a que termine el hilo
        pass
