import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from pywinauto.application import Application
import time
import csv
import pandas as pd
import yaml

configs=None

def loadConfigs():
    global configs
    with open('C:/Users/user/Desktop/Valence/Valence_Python/valence-battery/config.yaml', 'r') as file:
        configs = yaml.safe_load(file)
        print(str(configs['strings'][1]))
        # print(prime_service['prime_numbers'][0])
        # print(prime_service['rest']['url'])
loadConfigs()
#app.ModuleDiagG2.print_control_identifiers()

#set up data structures


root = Tk() #root is the root window
root.title("Covalent") #snazzy name
root.geometry(str(configs['resolution']['x'])+"x"+str(configs['resolution']['y'])) #resize root window

e_id = Entry(root)
e_path = Entry(root,width=50)
e_com = Entry(root)
e_id.insert(0,"19")
e_path.insert(0,"C:\\Users\\user\\Desktop\\Valence\\Valence_Logs")
e_com.insert(0,"COM6")
stringFrame = Frame(root)
for i in range(5):
    l1=Listbox(stringFrame,height=5).pack()
stringFrame.grid(row=7,column=1,columnspan=3)

## Collects a single sample from the specified module
# id - integer Module ID number
# comPort - string with COM port # formatted as "COM#"
def CollectSample(id,comPort):
    app=Application(backend='uia').start('C:\Program Files (x86)\Valence Technology Inc\Valence U-Charge XP Module Diagnostics Software\ModuleDiagG2.exe')

    #Set COM port
    comPort=app.ModuleDiagG2.child_window(title="COM Port", auto_id="1001", control_type="Edit").wrapper_object()
    comPort.click_input()
    comPort.type_keys(e_com.get())

    #set module ID
    modId=app.ModuleDiagG2.child_window(title="Module ID", auto_id="ComboBoxModuleID", control_type="ComboBox").wrapper_object()
    modId.click_input()
    modId.type_keys(id)

    #type filename in box
    valence_path=app.ModuleDiagG2.child_window(auto_id="TxtPath", control_type="Edit").wrapper_object()
    valence_path.select()
    valence_path.type_keys(e_path.get())

    #click the set filename button
    valence_btnSetPath=app.ModuleDiagG2.child_window(title="Set Filename", auto_id="Button1", control_type="Button").wrapper_object()
    valence_btnSetPath.click_input()
    time.sleep(1)

    #dismiss messagebox
    valence_btnClosePath = app.ModuleDiagG2.child_window(title="OK", control_type="Button").wrapper_object()
    valence_btnClosePath.click_input()
    time.sleep(3)

    #Start rs485
    btn_start=app.ModuleDiagG2.child_window(title="Start Read", auto_id="ButtonRead", control_type="Button").wrapper_object()
    btn_start.click_input()
    time.sleep(3)

    #click single sample button
    btn_sample=app.ModuleDiagG2.child_window(title="Single Sample", auto_id="Button7", control_type="Button").wrapper_object()
    btn_sample.click_input()
    time.sleep(1)

    #dismiss messagebox
    btn_exit = app.ModuleDiagG2.child_window(title="OK", auto_id="2", control_type="Button").wrapper_object()
    btn_exit.click_input()
    time.sleep(2)

    #stop rs485
    btn_start.click_input()
    time.sleep(2)

    #Close the Valence window
    btn_CloseWindow = app.ModuleDiagG2.child_window(title="Close", control_type="Button").wrapper_object()
    btn_CloseWindow.click_input()

def readCSV():
    # global
    with open('C:/Users/user/Desktop/Valence/Valence_Python/valence-battery/battery.CSV') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\ttime:{row[0]}:({row[1]}), SN:{row[2]}, #{row[3]}')
                tmax=[float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9])]
                tmax=np.amax(tmax)
                print(f'\thighest temp:{tmax}')
                curr=float(row[11])

                vmax=[row[12],row[13],row[14],row[15],row[16],row[17]]
                i=0
                for item in vmax:
                    if (item==""):
                        vmax[i]=0
                    else:
                        vmax[i]=float(item)
                    i=i+1

                vmax=np.amax(vmax)
                print(f'\thighest voltage:{vmax}')
                line_count += 1
        print(f'Processed {line_count} lines.')


btn_getSample = Button(root,text="Collect a Sample",pady=10,command=lambda: CollectSample(e_id.get(),e_com.get()))
btn_readCSV = Button(root,text="Read CSV",pady=10,command=readCSV)


l_id = Label(root,text="Module ID #:")
l_path = Label(root,text="Log Folder:")
l_com = Label(root,text="COM port:")
l_id.grid(row=1,column=0)
l_path.grid(row=2,column=0)
l_com.grid(row=3,column=0)

e_id.grid(row=1,column=1)
e_path.grid(row=2,column=1)
e_com.grid(row=3,column=1)

btn_getSample.grid(row=5,column=0,columnspan=2)
btn_readCSV.grid(row=6,column=0,columnspan=2)

#TODO: add data visualization
#TODO: add a subfolder creation feature if they don't already exist.
#TODO: have a subfolder for each module ID's CSV files (..\Valence_Logs\19)
#TODO: add a config file for critical settings changes
#TODO: traverse all individual CSVs and compile a master CSV for pandas
#TODO: implement a "Strings" Customizer so that IDs can be added to ListBoxes and statistics can be done per string
#TODO: implement a Frame for the Listboxes that can have ListBoxes PACKED in, with buttons for adding/removing strings

root.mainloop()
