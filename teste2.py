from multiprocessing import Pool, freeze_support

def f(x, y):
    return x*y

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.starmap(f, [[1, 50], [2, 60], [3, 70]]))