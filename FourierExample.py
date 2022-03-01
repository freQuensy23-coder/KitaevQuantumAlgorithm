from algorithms import Fourier
from flux_bias import FluxBiasController

field_range = (f_min, f_max) = (75, 100)

alg = Fourier(field_range=field_range, measurements_iterations=1)
for i in range(15):
    alg.draw_truth().show()
    alg.work()
print(alg.field_manger.field)
