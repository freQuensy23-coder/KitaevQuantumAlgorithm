import numpy as np
from matplotlib import pyplot as plt

from algorithms import KitaevTruthScaling, Kitaev

field_range = (f_min, f_max) = (75, 100)
N = 10

alg = Fourier(field_range=field_range, measurements_iterations=1) # TODO убрать measurments iterations в метод work
dfs = np.zeros(N)
times = np.zeros(N)
for i in range(N):
    alg.draw_truth().show()
    alg.work()
    dfs[i] = alg.f_max - alg.f_min
    times[i] = alg.field_manger.total_time
print(alg.field_manger.field)
plt.plot(np.log(times), np.log(dfs))
plt.plot(np.log(times), np.log(dfs))
plt.xlabel("log(t)")
plt.ylabel("log($\\Delta$ F)")

plt.plot(np.log(times), np.log(1/times))

plt.show()
