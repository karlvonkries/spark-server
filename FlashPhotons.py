#!/usr/bin/env python3

from tkinter import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
import time

root = Tk()
root.title('Flash Photons')
rootFrame = Frame(root)
rootFrame.pack()

IDs = []
names = []
response1 = StringVar()
response2 = StringVar()

def getPhotons():
    photonSelect.delete(0,photonSelect.size()-1)
    names.clear()
    IDs.clear()
    result = subprocess.run(['particle', 'list'], stdout=subprocess.PIPE)
    tempstr = result.stdout.decode('utf-8')
    splitstr = tempstr.split()
    for idx, s in enumerate(splitstr):
        if s == "(Photon)" or s == "(Product":
            IDs.append(splitstr[idx-1][1:25])
            name = splitstr[idx-2]
            if "variables..." in name:
                name = name[20:]
            names.append(name)    
    for n in names:
        photonSelect.insert(END, n)
    #photonSelect.config(height=(len(names));
    #print(names)
    #print(IDs)
    
def flashPhotons():
    if fileSelect.curselection():
        filepath = './binaries/'+fileSelect.get(fileSelect.curselection()[0])
        #print(filepath)
        if photonSelect.curselection():
            response2.set("Working...")
            root.update_idletasks()
            for itr, idx in enumerate(photonSelect.curselection()):
                result = subprocess.run(['particle', 'flash', IDs[idx], filepath], stdout=subprocess.PIPE)
                tempstr = result.stdout.decode('utf-8')
                #print(tempstr)
                if 'Flash device OK:  Update finished' in tempstr:
                    response2.set(response2.get()[:-3] + 'Flashing ' + names[idx] + ': Success\n...')
                else:
                    response2.set(response2.get()[:-3] + 'Flashing ' + names[idx] + ': Failed\n...')
                if itr == 0:
                    response2.set(response2.get()[7:])
                root.update_idletasks()
            response2.set(response2.get()[:-4])
        else:
            response2.set("No Photons Selected")
    else:
        response2.set("Binary File not selected")

flashFrame = Frame(rootFrame, bd=5)
flashFrame.pack(fill='x')

leftFlashFrame = Frame(flashFrame, width=500)
leftFlashFrame.pack(side=LEFT)
photonSelectFrame = Frame(leftFlashFrame)
photonSelectFrame.pack()
photonLabel = Label(photonSelectFrame, text="Photons: ")
photonLabel.pack(side=LEFT)
scrollbar = Scrollbar(photonSelectFrame)
scrollbar.pack(side=RIGHT, fill=Y)
photonSelect = Listbox(photonSelectFrame, yscrollcommand=scrollbar.set, height=20, selectmode=MULTIPLE, exportselection=0)
photonSelect.pack(side=RIGHT)
scrollbar.config(command=photonSelect.yview)
rightFlashFrame = Frame(flashFrame, bd=10, width=350)
rightFlashFrame.pack(side=RIGHT)
populateButton = Button(rightFlashFrame, text="Refresh Photon List", wraplength=150, width=15, command=getPhotons)
populateButton.pack()
fileSelectFrame = Frame(rightFlashFrame, bd=10)
fileSelectFrame.pack()
fileLabel = Label(fileSelectFrame, text="Binaries ")
fileLabel.pack(side=LEFT)
fileSelect = Listbox(fileSelectFrame, selectmode=SINGLE, exportselection=0)
fileSelect.pack(side=RIGHT)
flashButton = Button(rightFlashFrame, text="Flash Photons", wraplength=150, width=15, command=flashPhotons)
flashButton.pack()
response2Label = Label(rightFlashFrame, justify=LEFT, bd=10, textvariable=response2, wraplength=300)
response2Label.pack()

result = subprocess.run(['ls', './binaries'], stdout=subprocess.PIPE)
tempstr = result.stdout.decode('utf-8')
#print(tempstr)
for s in tempstr.split():
    fileSelect.insert(END, s);
fileSelect.config(height=len(tempstr.split()));

getPhotons()

root.mainloop()

