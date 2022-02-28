from algorithms import Kitaev
from tqdm import tqdm

f_min = 0
f_max = 100
N = 10000

if __name__ == "__main__":
    g = 0
    b = 0
    for i in tqdm(range(1000)):
        algorithm = Kitaev(field_range=(f_min, f_max))
        l, r = algorithm.work()
        f = algorithm.field_manger.field
        if l <= f <= r:
            g += 1
        else:
            b += 1
            print(l, round(f, 2), r, "------")
        # print(l, round(f, 2), r)
    print(g, b)
