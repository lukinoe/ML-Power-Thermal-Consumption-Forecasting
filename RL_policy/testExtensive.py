import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from importlib import reload
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (8,5.8)
import sys
sys.path.insert(0, 'C:/Users/lukas/OneDrive - Johannes Kepler Universität Linz/Projekte/DLinear/data')
import datafactory
from datafactory import DataSet
plt.rcParams["figure.figsize"] = (20,8)

dataset = DataSet(start_date="2022-01-01", target="i_m1sum", scale_target=False, scale_variables=False, time_features=False, resample=None,dynamic_price=False, demand_price=0.5, feedin_price=0.5).pipeline()

from extensiveSearch import Tree, Experiment, Experiment_Concat

levels = 15
start_date = "2022-07-24 12:00:00"

args = {
    "max_storage_tank": dataset.kwh_eq_state.max(),
    "optimum_storage": dataset.kwh_eq_state.max() * 0.9,
    "gamma1": 1,    # financial
    "gamma2": 0.05,      # distance optimum
    "gamma3": 0.0,      # tank change
    "demand_price": 0.5,
    "feedin_price": 0.2
}

dataset = DataSet(start_date="2022-01-01", target="i_m1sum", scale_target=False, scale_variables=False, time_features=False, dynamic_price=False, demand_price=args["demand_price"], feedin_price=args["feedin_price"]).pipeline()
dataset = dataset[["date", "i_m1sum" , "demand_price", "feedin_price", "power_consumption_kwh", "thermal_consumption_kwh",  "kwh_eq_state"]]
print(dataset)

e = Experiment(levels, n_samples=2, dataset=dataset, args=args, exploit=True, start_date=start_date) 



res = e.results()
plt.plot(res[0][0], label="kwH Tank")
plt.axhline(y=args["optimum_storage"], color='g', linestyle='--')
plt.plot(res[0][1], label="Strategie 0|1", linestyle='--')
plt.xticks(np.arange(len(res[0][1])))
plt.xlabel("Zeitpunkt (t)")
plt.ylabel("kwh")
plt.legend()
plt.show()


