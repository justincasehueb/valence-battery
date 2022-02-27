from pywinauto.application import Application
import time

app=Application(backend='uia').start('C:\Program Files (x86)\Valence Technology Inc\Valence U-Charge XP Module Diagnostics Software\ModuleDiagG2.exe')

#app.ModuleDiagG2.print_control_identifiers()

comPort=app.ModuleDiagG2.child_window(title="COM Port", auto_id="1001", control_type="Edit").wrapper_object()
comPort.click_input()
comPort.type_keys("COM6")

modId=app.ModuleDiagG2.child_window(title="Module ID", auto_id="ComboBoxModuleID", control_type="ComboBox").wrapper_object()
modId.click_input()
modId.type_keys("19")

btn_start=app.ModuleDiagG2.child_window(title="Start Read", auto_id="ButtonRead", control_type="Button").wrapper_object()
btn_start.click_input()

time.sleep(3)

btn_sample=app.ModuleDiagG2.child_window(title="Single Sample", auto_id="Button7", control_type="Button").wrapper_object()
btn_sample.click_input()

#app.ModuleDiagG2.print_control_identifiers()

#popup = app.top_window()
btn_exit = app.ModuleDiagG2.child_window(title="OK", auto_id="2", control_type="Button").wrapper_object()
btn_exit.click_input()

time.sleep(2)

btn_start.click_input()

print("Done!")