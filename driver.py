from simulation import simulate
from plot import final_plot

simulate(path="../openpflow/test1.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level0')
# final_plot(path='results_level0.txt', N=200)

simulate(path="../openpflow/test1.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level1')
# final_plot(path='results_level1.txt', N=200)

simulate(path="../openpflow/test1.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level3')
# final_plot(path='results_level3.txt', N=200)


