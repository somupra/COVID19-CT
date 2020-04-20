from simulation import simulate

simulate(path="../openpflow/final.csv", population=5000, days=100, tstamp_per_day=240)
simulate(path="../openpflow/final.csv", population=5000, days=100, tstamp_per_day=240, algo_mode='level0')
#simulate("../openpflow/final.csv")
simulate(path="../openpflow/final.csv", population=5000, days=100, tstamp_per_day=240, algo_mode='level1')
