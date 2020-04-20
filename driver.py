from simulation import simulate
from plot import final_plot

# simulate(path="../openpflow/sample.csv", population=100, days=100, tstamp_per_day=40)
# simulate(path="../openpflow/sample.csv", population=100, days=100, tstamp_per_day=40, algo_mode='level0')
# simulate("../openpflow/final.csv")

simulate(path="../openpflow/test.csv", population=100, days=50, tstamp_per_day=40, algo_mode='level0')
simulate(path="../openpflow/test.csv", population=100, days=50, tstamp_per_day=40, algo_mode='level1')
simulate(path="../openpflow/test.csv", population=100, days=50, tstamp_per_day=40, algo_mode='level3')


