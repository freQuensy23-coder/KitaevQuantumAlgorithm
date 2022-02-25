from algorithms import Kitaev

f_min = 10
f_max = 100
N = 1000


if __name__ == "__main__":
    algorithm = Kitaev(field_range=(f_min, f_max))
    print(algorithm.work())
    print(algorithm.field_manger.field)

