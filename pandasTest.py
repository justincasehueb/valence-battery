import pandas as pd
import matplotlib.pyplot as plt
import time

tit = pd.read_csv("C:/Users/user/Desktop/Valence/Valence_Python/valence-battery/battery.CSV")

# print(tit.columns)

# print("Max Voltage:",tit[["mVcell1","mVcell2", "mVcell3", "mVcell4", "mVcell5", "mVcell6"]].max())

print(tit.keys())

#TODO: Implement a way to select the ID of interest and pass it this way to make a plot easily.
selectedID = 19
myDF = tit[tit["ID"] == selectedID]

voltagesDF = myDF[["mVcell1","mVcell2","mVcell3","mVcell4"]]#,"mVcell5","mVcell6"]]
# voltagesDF.plot(marker='o')

currentDF = myDF[["Current(A)"]]
# currentDF.plot(marker="o")

cellTempsDF = myDF[["CellTemp1(0.01C)","CellTemp2(0.01C)","CellTemp3(0.01C)","CellTemp4(0.01C)","CellTemp5(0.01C)","CellTemp6(0.01C)"]]
pcbTempsDF = myDF[["PCBATemp(0.01C)"]]
cellDiffDF = myDF[["CellDiff(mV)"]]
socDF = myDF[["SOC(%)"]]
minVoltDF = myDF[["VcellMin(mV)"]]
maxVoltDF = myDF[["VcellMax(mv)"]]

# print("MDF",myDF.head())
# print("Min Voltage:",tit["mVcell1"].min())

plt.show()
# time.sleep(100)
