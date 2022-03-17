import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from pywinauto.application import Application
import time
import csv
import pandas as pd
import yaml
import glob

dir = os.path.dirname(__file__)
os.chdir(dir)
# print(os.getcwd())
#app.ModuleDiagG2.print_control_identifiers()


configs=None
def loadConfigs():
    global configs
    with open(dir+"\\config.yaml", 'r') as file:
        configs = yaml.safe_load(file)
        # print(str(configs['strings'][1]))
        # print(prime_service['prime_numbers'][0])
        # print(prime_service['rest']['url'])
loadConfigs()

##GLOBAL VARIABLES##

root = Tk() #root is the root window
root.title("Covalent") #snazzy name
root.geometry(str(configs['resolution']['x'])+"x"+str(configs['resolution']['y'])) #resize root window

headFrame = Frame(root)
headFrame.pack(fill=BOTH, expand=1)

numStringColumns=configs['num_string_columns']
columnCounter=0

stringFrame = Frame(root)
stringFrame.pack(fill=BOTH, expand=1)
f=Frame(stringFrame)
f.pack(side=LEFT)

stringList = [] #List of frames that contain information on individual strings

##FUNCTIONS##

def CombineCSV(folder):
    os.chdir(dir+"\\Valence_Logs\\"+str(folder))
    # print(os.getcwd())
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
# CombineCSV("")

#generates the text in the strings section of the config.YAML file
def makeYAML():
    for i in range(1,20):
        print("\t"+str(i)+":")
        for j in range((i-1)*4,(i-1)*4+4):
            print("\t- "+str(j+1))

#creates all the folders for each battery
def makeFiles():
    path = dir+"\\Valence_Logs"
    for i in range(1,20):
        # print(path+str(i))
        if (os.path.isdir(path+str(i))==False):
            os.mkdir(path+str(i))

def AddString():
    global stringFrame, numStringColumns, columnCounter, f
    columnCounter=columnCounter+1
    if (columnCounter==1):
        f.pack(side='top',fill=X)
    elif ((columnCounter-1)%numStringColumns==0):
        f=Frame(stringFrame)
        f.pack(side='top',fill=X)
        # columnCounter=0

    lbl=Label(f,text="String #"+str(columnCounter),pady=50,padx=40)
    lbx=Listbox(f,height=5,width=10)
    lbl.pack(side='left')
    lbx.pack(side='left')
    stringList.insert(columnCounter,lbx)
    PopulateStrings()

def PopulateStrings():
    global stringList, configs
    for i in range(1, len(stringList)+1):
        for j in configs['strings'][i]:
            if(stringList[i-1].size()<4):
                stringList[i-1].insert('end',j)

for i in range(configs['num_strings']):
    # print(i)
    AddString()

e_id = Entry(headFrame)
e_path = Entry(headFrame,width=50)
e_com = Entry(headFrame)
e_id.insert(0,configs['ID'])
e_path.insert(0,configs['log_path'])
e_com.insert(0,configs['COM'])

## Collects a single sample from the specified module
# id - integer Module ID number
# comPort - string with COM port # formatted as "COM#"
def CollectSample(id,comPort):
    app=Application(backend='uia').start(configs['path_to_valence'])

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

btn_getSample = Button(headFrame,text="Collect a Sample",pady=10,command=lambda: CollectSample(e_id.get(),e_com.get()))
btn_addString = Button(headFrame,text="Add a String",pady=10,command=AddString)

l_id = Label(headFrame,text="Module ID #:")
l_path = Label(headFrame,text="Log Folder:")
l_com = Label(headFrame,text="COM port:")
l_id.grid(row=1,column=0)
l_path.grid(row=2,column=0)
l_com.grid(row=3,column=0)

e_id.grid(row=1,column=1)
e_path.grid(row=2,column=1)
e_com.grid(row=3,column=1)

btn_getSample.grid(row=5,column=0,columnspan=2)
btn_addString.grid(row=6,column=0,columnspan=2)

# stringFrame.grid(row=7,column=0,columnspan=10)

#TODO: add data visualization
#TODO: implement a "Strings" Customizer so that IDs can be added to ListBoxes and statistics can be done per string
#TODO: implement a Frame for the Listboxes that can have ListBoxes PACKED in, with buttons for adding/removing strings
#TODO: having all CSVs save to a single folder and get combined into a master CSV


root.mainloop()

# f=Frame(stringFrame)
# count=0
# perRow=3
# def populateStrings():
#     for i in range(1,configs['num_strings']+1):
#         print(i)
#         count=count+1
#         if (count==perRow):
#             f.pack()
#             f=Frame(stringFrame)
#             count=0
#         l=Label(f,text="String #"+str(i),pady=50,padx=40).pack(side='left')
#         l1=Listbox(f,height=5,width=10)
#         for j in configs['strings'][i]:
#             l1.insert('end',str(j))
#         l1.pack(side='left')
#         if (count>0 and i==configs['num_strings']):
#             f.pack()
