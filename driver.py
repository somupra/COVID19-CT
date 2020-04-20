from simulation import simulate

simulate(path="../openpflow/sample.csv", population=100, days=100, tstamp_per_day=40)
simulate(path="../openpflow/sample.csv", population=100, days=100, tstamp_per_day=40, algo_mode='level0')
#simulate("../openpflow/final.csv")
