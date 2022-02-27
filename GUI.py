from tkinter import *
from tkinter import messagebox

#This always has to be run to initialize Tkinter
root = Tk() #root is the root window
root.title("Covalent") #snazzy name
root.geometry("200x200") #resize root window

## Sometimes you gotta initialize some stuff early.
e=Entry(root,borderwidth=5) #needs to be before the functions
e.grid(row=1,column=0,columnspan=3) #because it is used in a function


## Functions
def popup():
    response=messagebox.askyesno("This is a popup","SORRY! uWu")
    if response ==1:
        Label(root,text="clicked yes").pack()
    else:
        Label(root,text="clicked no").pack()

def myClick():
    myLabel = Label(root, text="Hello " + e.get())
    myLabel.grid(row=2,column=0)



## Step 1: Create the thing

# myLabel1 = Label(root, text="Hello World!")

myButton1= Button(root, text="Click me",padx=50,pady=50, command=popup) #state=DISABLED


## Step 2: Put it in the window (several methods: pack, grid,



root.mainloop()
