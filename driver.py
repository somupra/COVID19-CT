from simulation import simulate
from simulation import random_sim
from plot import final_plot

# simulate(path="test2.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level3')
# final_plot(path='results_level0.txt', N=200)

# simulate(path="../openpflow/test1.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level1')
# # final_plot(path='results_level1.txt', N=200)

# simulate(path="../openpflow/test1.csv", population=100, days=80, tstamp_per_day=40, algo_mode='level3')
# # final_plot(path='results_level3.txt', N=200)

init_cond = dict()
algo_modes = ['level0', 'level1', 'level3']

for mode in algo_modes:
    random_sim(init_cond, path="output1.csv", n_times=10, algo_mode= mode)

