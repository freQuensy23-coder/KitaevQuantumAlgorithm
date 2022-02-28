from algorithms import Fourier
from flux_bias import FluxBiasController

field_range = (f_min, f_max) = (75, 100)

alg = Fourier(field_range=field_range)
alg.draw_truth().show()
alg.work()
alg.draw_truth().show()
print(alg.field_manger.field)
