import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from pywinauto.application import Application
import time

#app.ModuleDiagG2.print_control_identifiers()

root = Tk() #root is the root window
root.title("Covalent") #snazzy name
root.geometry("500x200") #resize root window

e_id = Entry(root)
e_path = Entry(root,width=50)
e_com = Entry(root)
e_id.insert(0,"19")
e_path.insert(0,"C:\\Users\\user\\Desktop\\Valence\\Valence_Logs")
e_com.insert(0,"COM6")

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


btn_getSample = Button(root,text="Collect a Sample",pady=10,command=lambda: CollectSample(e_id.get(),e_com.get()))

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

#TODO: add data visualization
#TODO: add a subfolder creation feature if they don't already exist.
#TODO: have a subfolder for each module ID's CSV files (..\Valence_Logs\19)
#TODO: add a config file for critical settings changes

root.mainloop()
