import pandas as pd

tit = pd.read_csv("C:/Users/user/Desktop/Valence/Valence_Python/valence-battery/battery.CSV")

# print(tit.columns)

# print("Max Voltage:",tit[["mVcell1","mVcell2", "mVcell3", "mVcell4", "mVcell5", "mVcell6"]].max())

print("Min Voltage:",tit["mVcell1"].min())
