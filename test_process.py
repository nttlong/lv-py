from multiprocessing import Process

def f(name,b):
    print('hello', name+b)

if __name__ == '__main__':
    p = Process(target=f, args=('bob','x',))
    p.start()
    p.join()