import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import iFixDBHandler as db
import os
import uuid
import shutil
import subprocess, platform

thumbDir = os.path.join(os.getcwd(), "ifix_db_backup/Controller_Thumbs")
docsDir = os.path.join(os.getcwd(), "ifix_db_backup/Controller_Docs")
mfgList = []
mfgIDs = []
controllersList = []
controllersIDs = []
controllerPasswordNames = []
controllerPasswordData = []
passwordIDs = []
documentsList = []
documentsFilenames = []
selectedMfgID = 0
selectedControllerID = 0
selectedPasswordID = 0
selectedPasswordName = ""

def updateManufacturersList():
    global mfgIDs
    global mfgList

    for m in db.manufacturers():
        mfgIDs.append(m[0])
        mfgList.append(m[1])
        
def updateManufacturers():
    global mfgList
    mfrListBox.delete(0, "end")
    for m in mfgList:
        mfrListBox.insert("end", m)

def printAllControllerDocs():
    for m in db.manufacturers():
        manID = m[0]
        manString = m[1]
        print(manString)
        for c in db.controllersFromID(manID):
            print("   " + c[2])
            for d in db.docsForControllerFromID(c[0]):
                print("      +" + d[2])
                
        print("")

def mfrSelected(event):
    index = mfrListBox.curselection()
    global selectedMfgID
    selectedMfgID = mfgIDs[index[0]]
    updateControllersForManufacturer()
        
def updateControllersForManufacturer():
    global mfgIDs
    global controllersList
    global controllersIDs
    global selectedMfgID
    global thumbDir
    global passwordIDs
    global documentsList
    global documentsFilenames

    controllersList.clear()
    controllersIDs.clear()
    passwordIDs.clear()
    documentsList.clear()
    documentsFilenames.clear()
    controllerListBox.delete(0, "end")
    documentsListBox.delete(0, "end")
    passwordsListBox.delete(0, "end")
    passwordTextBox.delete(1.0, 'end')
    thumbLabel.configure(image='')
    addControllerButton.configure(state="normal")
    addPasswordButton.configure(state="disabled")
    addDocumentButton.configure(state="disabled")
    savePasswordButton.configure(state="disabled")

    for c in db.controllersFromID(selectedMfgID):
        controllersIDs.append(c[0])
        controllersList.append(c[2])
        controllerListBox.insert("end", c[2])
        thumbPath = os.path.join(thumbDir, db.controllerThumbFilenameFromID(c[0]))
    

def controllerSelected(event):
    index = controllerListBox.curselection()
    global selectedControllerID
    selectedControllerID = controllersIDs[index[0]]
    updateControllerData()

def updateControllerData():
    global controllersIDs
    global selectedControllerID
    global controllerPasswordNames
    global controllerPasswordData
    global passwordIDs
    global documentsList
    global documentsFilenames
    
    controllerPasswordNames.clear()
    controllerPasswordData.clear()
    passwordIDs.clear()
    documentsList.clear()
    documentsFilenames.clear()
    passwordsListBox.delete(0, "end")
    documentsListBox.delete(0, 'end')
    passwordTextBox.delete(1.0, 'end')
    addPasswordButton.configure(state="normal")
    addDocumentButton.configure(state="normal")
    savePasswordButton.configure(state="disabled")

    thumbString =  db.controllerThumbFilenameFromID(selectedControllerID)
    if not thumbString:
        thumbLabel.configure(image='')
    else:    
        thumbPath = os.path.join(thumbDir, thumbString)
        img = ImageTk.PhotoImage(Image.open(thumbPath))
        thumbLabel.configure(image=img)
        thumbLabel.image=img 

    for d in db.docsForControllerFromID(selectedControllerID):
        documentsListBox.insert("end", d[2])
        documentsFilenames.append(d[3])

    for p in db.codesForControllerFromID(selectedControllerID):
        passwordIDs.append(p[0])
        controllerPasswordNames.append(p[3])
        controllerPasswordData.append(p[4])
        passwordsListBox.insert("end", p[3])
    
def passwordSelected(event):
    global selectedPasswordID
    global selectedPasswordName
    
    index = passwordsListBox.curselection()
    passwordTextBox.delete(1.0, 'end')
    passwordTextBox.insert('end', controllerPasswordData[index[0]])
    selectedPasswordID = passwordIDs[index[0]]
    selectedPasswordName = controllerPasswordNames[index[0]]
    savePasswordButton.configure(state="normal")

def documentSelected(event):
    index = documentsListBox.curselection()
    filePath = os.path.join(docsDir, documentsFilenames[index[0]])
    print(filePath)
    
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filePath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filePath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filePath))
#    os.open(filePath, os.O_RDONLY)
#    os.startfile(filePath, 'open')

def addManufacturerClicked():
    text = askstring("Add Manufacturer", "Manufacturer Name")
    if not text:
        return

    db.addManufacturer(text)
    updateManufacturersList()
    updateManufacturers()

def addControllerClicked():
    text = askstring("Add Controller", "Controller Name")
    if not text:
        return

    global selectedMfgID
    db.addController(selectedMfgID,text)
    updateControllersForManufacturer()

def addPasswordClicked():
    text = askstring("Add Password", "Password Name")
    if not text:
        return

    global selectedMfgID
    global selectedControllerID
    db.addPassword(selectedMfgID,selectedControllerID,text)
    updateControllerData()

def addDocumentClicked():
    path = fd.askopenfilename()
    if not path:
        return
    
    description = askstring("Add Document", "Please provide a document description.")
    if not description:
        return

    global selectedControllerID
    destinationFilename = str(uuid.uuid1())
    filename, file_extension = os.path.splitext(path)
    destinationFilename = destinationFilename + file_extension
    destinationPath = os.path.join(docsDir, destinationFilename)

    shutil.copyfile(path, destinationPath)
    db.addControllerDocument(selectedControllerID, description, destinationFilename)
    updateControllerData()

def updatePasswordClicked():
    global selectedMfgID
    global selectedControllerID
    global selectedPasswordID
    global selectedPasswordName
    db.updatePassword(selectedMfgID, selectedControllerID, selectedPasswordID, selectedPasswordName, passwordTextBox.get('1.0', 'end'))

#db.initDocTable()
#printAllControllerDocs()

window = tk.Tk()
window.title("iFixControllersDB Manager")
window.columnconfigure([0,1,2,3], minsize=198, weight=2)
window.rowconfigure(0, minsize=140, weight=0)
window.rowconfigure(1, minsize=320, weight=1)
window.geometry("860x560")

updateManufacturersList()

mfrListBox = tk.Listbox(window,listvariable=tk.StringVar(value=mfgList),height=24,selectmode='single',exportselection=False)
mfrListBox.grid(column=0,row=0,rowspan=2,padx=5,pady=5,sticky="nsew")
mfrListBox.bind('<<ListboxSelect>>', mfrSelected)

controllerListBox = tk.Listbox(window,height=24,selectmode='single',exportselection=False)
controllerListBox.grid(column=1,row=0,rowspan=2,padx=5,pady=5,sticky="nsew")
controllerListBox.bind('<<ListboxSelect>>', controllerSelected)

documentsListBox = tk.Listbox(window,height=8,selectmode='single',exportselection=False)
documentsListBox.grid(column=2,row=0,padx=5,pady=5,sticky="nsew")
documentsListBox.bind('<Double-1>', documentSelected)

passwordsListBox = tk.Listbox(window,height=16,selectmode='single',exportselection=False)
passwordsListBox.grid(column=2,row=1,padx=5,pady=5,sticky="nsew")
passwordsListBox.bind('<<ListboxSelect>>', passwordSelected)

thumbLabel = tk.Label(window, text="", justify="center", width=128)
thumbLabel.grid(column=3,row=0,padx=5,pady=5,)

passwordTextBox = tk.Text(window,height=12,width=48,wrap='word')
passwordTextBox.grid(column=3,row=1,padx=5,pady=5,sticky="nsew")

addManufacturerButton = tk.Button(window, text="Add Manufacturer...", command=addManufacturerClicked)
addManufacturerButton.grid(column=0,row=2,padx=5,pady=5,sticky="nsew")

addControllerButton = tk.Button(window, text="Add Controller...", command=addControllerClicked,state="disabled")
addControllerButton.grid(column=1,row=2,padx=5,pady=5,sticky="nsew")

addPasswordButton = tk.Button(window, text="Add Password...", command=addPasswordClicked,state="disabled")
addPasswordButton.grid(column=2,row=3,padx=5,pady=5,sticky="nsew")

savePasswordButton = tk.Button(window, text="Save Details", command=updatePasswordClicked,state="disabled")
savePasswordButton.grid(column=3,row=2,padx=5,pady=5,sticky="nsew")

addDocumentButton = tk.Button(window, text="Add Document...", command=addDocumentClicked,state="disabled")
addDocumentButton.grid(column=2,row=2,padx=5,pady=5,sticky="nsew")

window.mainloop()
