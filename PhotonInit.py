#!/usr/bin/env python3

from tkinter import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
import time

root = Tk()
root.title('Photon Intitialization')
rootFrame = Frame(root)
rootFrame.pack()

photonid = StringVar()
photonid.set('')
response1 = StringVar()
response2 = StringVar()
response3 = StringVar()
response4 = StringVar()
idStr = StringVar()

def setWifiCallback():
    result = subprocess.run(['particle', 'identify'], stdout=subprocess.PIPE)
    tempstr = result.stdout.decode('utf-8')
    #print(tempstr)
    tempid = tempstr.split()[4]
    #print(photonid)

    if tempid == 'port':
        response1.set('Error: No photon detected.')
        photonid.set('')
        idStr.set("Current Device ID: " + photonid.get())

    elif tempid == 'out':
        response1.set('Error: Photon not in listen mode.')
        photonid.set('')
        idStr.set("Current Device ID: " + photonid.get())

    elif tempid == 'undefined':
        response1.set('Error: Photon not in listen mode.')
        photonid.set('')
        idStr.set("Current Device ID: " + photonid.get())

    elif len(tempid) == 24:
        photonid.set(tempid)
        idStr.set("Current Device ID: " + photonid.get())

        if ssidEntry.get() == '' or passEntry.get() == '':
            response1.set("Error: No Wifi Credentials detected.")
        else :
            
            p = Popen(['particle', 'serial', 'wifi'], stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)

            print('n', file=p.stdin, flush=True)
            print(p.stdout.readline())
            time.sleep(2)
            print(ssidEntry.get(), file=p.stdin, flush=True)
            print(p.stdout.readline())
            print(p.stdout.readline())
            print(p.stdout.readline())
            print(p.stdout.readline())
            print(p.stdout.readline())
            time.sleep(2)
            print('', file=p.stdin, flush=True)
            print(p.stdout.readline())
            time.sleep(2)
            print(passEntry.get(), file=p.stdin, flush=True)
            print(p.stdout.readline())
            print(p.stdout.readline())

            response1.set('Wifi Credentials properly saved! Your Device should restart.')

    else:
        response1.set('Unknown Error')

def setKeysCallback():
    if photonid.get() == '':
        response2.set('Error: No Device ID Set')
    else:
        result = subprocess.run(['particle', 'keys', 'server', '--host', '192.168.4.1:5683', '/spark/spark-server/data/default_key.pub.pem'], stdout=subprocess.PIPE)
        tempstr = result.stdout.decode('utf-8')
        #print(tempstr)
        if 'Okay!  New keys in place, your device will not restart.' in tempstr:
            #print('success')
            result = subprocess.run(['particle', 'keys', 'doctor', photonid.get()], stdout=subprocess.PIPE)
            tempstr = result.stdout.decode('utf-8')
            #print(tempstr)
            if 'Okay!  New keys in place, your device should restart' in tempstr:
                strVar2.set('Keyes successfully traded and saved')
                result = subprocess.run('rm ./'+photonid.get()+'*', stdout=subprocess.PIPE, shell=True)
                result = subprocess.run('rm ./backup_rsa_*', stdout=subprocess.PIPE, shell=True)
            else:
                response2.set('Failed to save device keys on server')
        else:
            response2.set('No DFU device detected')

def setNameCallback():
    if photonid.get() == '':
        response3.set('Error: No Device ID Set')
    else:
        tryname = nameEntry.get()
        
        if tryname == '':
            response3.set('Error: No Name Input')
        else:
            result = subprocess.run(['particle', 'list'], stdout=subprocess.PIPE)
            tempstr = result.stdout.decode('utf-8')
            #print(tempstr)

            if tryname+' ' in tempstr:
                response3.set(tryname + ': Device name already exists')
            else:
                result = subprocess.run(['particle', 'device', 'rename', photonid.get(), tryname], stdout=subprocess.PIPE)
                tempstr = result.stdout.decode('utf-8')
                #print(tempstr)
                if 'Successfully renamed device' in tempstr:
                    response3.set('Device Successfully Renamed to ' + tryname)
                else:
                    response3.set('Failed to rename devie')

def setFlashCallback():
    if fileSelect.curselection():
        if photonid.get() == '':
            response4.set('Error: No Device ID Set')
        else:
            filepath = './binaries/'+fileSelect.get(fileSelect.curselection()[0])
            #print(filepath)
            result = subprocess.run(['particle', 'flash', photonid.get(), filepath], stdout=subprocess.PIPE)
            tempstr = result.stdout.decode('utf-8')
            #print(tempstr)
            if 'Flash device OK:  Update finished' in tempstr:
                response4.set('Flash successful!!')
            else:
                response4.set('Flash failed')
    else:
        response4.set('Error: No file selected')
    #result = subprocess.run(['particle', 'flash', photonid.get(), './binaries/'+

idFrame = Frame(rootFrame, bd=5)
idFrame.pack()
idLabel = Label(idFrame, bd=5, textvariable=idStr, wraplength=400, font=("Helvetica", 18))
idLabel.pack()
idStr.set("Current Device ID: ")

listenFrame = Frame(rootFrame, bd=5)
listenFrame.pack(fill='x')

leftListenFrame = Frame(listenFrame, width=500)
leftListenFrame.pack(side=LEFT)
L1 = Label(leftListenFrame, anchor='w', bd=10, text="1) Enter Wifi Credentials", justify=LEFT, wraplength=300)
L1.pack(fill='x')
infoFrame = Frame(leftListenFrame)
infoFrame.pack()
labelFrame = Frame(infoFrame)
labelFrame.pack(side=LEFT)
ssidLabel = Label(labelFrame, text="SSID")
ssidLabel.pack()
passLabel = Label(labelFrame, text="Password")
passLabel.pack()
inputFrame = Frame(infoFrame)
inputFrame.pack(side=RIGHT)
ssidEntry = Entry(inputFrame, bd=5)
ssidEntry.pack()
passEntry = Entry(inputFrame, bd=5)
passEntry.pack()
L2 = Label(leftListenFrame, anchor='w', bd=10, text="2) Put Photon in Listen mode (hold setup until it flashes blue), then press Set Credentials", justify=LEFT, wraplength=300)
L2.pack(fill='x')
rightListenFrame = Frame(listenFrame, bd=10, width=300)
rightListenFrame.pack(side=RIGHT)
wifiButton = Button(rightListenFrame, text="Get ID and Set Wifi Credentials", width=15, wraplength=150, command = setWifiCallback)
wifiButton.pack()
response1Label = Label(rightListenFrame, bd=10, textvariable=response1, wraplength=200)
response1Label.pack()

dfuFrame = Frame(rootFrame, bd=5)
dfuFrame.pack(fill='x')

leftDFUFrame = Frame(dfuFrame, width=500)
leftDFUFrame.pack(side=LEFT)
L3 = Label(leftDFUFrame, anchor='w', bd=10, text="3) Set Photon into DFU mode (Hold both RESET and SETUP, then release RESET. Continue to hold SETUP until the LED starts to blink orange) and click Exchange keys with server.", justify=LEFT, wraplength=300)
L3.pack(fill='x')
rightDFUFrame = Frame(dfuFrame, bd=10, width=300)
rightDFUFrame.pack(side=RIGHT)
keyButton = Button(rightDFUFrame, text="Exchange keys with server", wraplength=150, width=15, command = setKeysCallback)
keyButton.pack()
response2Label = Label(rightDFUFrame, bd=10, textvariable=response2, wraplength=200)
response2Label.pack()

nameFrame = Frame(rootFrame, bd=5)
nameFrame.pack(fill='x')

leftNameFrame = Frame(nameFrame, width=500)
leftNameFrame.pack(side=LEFT)
L4 = Label(leftNameFrame, anchor='w', bd=10, text="Optional: Name Photon\n4) Input Name below, and press Name this Photon", justify=LEFT, wraplength=300)
L4.pack(fill='x')
nameInput = Frame(leftNameFrame)
nameInput.pack()
nameLabel = Label(nameInput, text="Name")
nameLabel.pack(side=LEFT)
nameEntry = Entry(nameInput, bd=5)
nameEntry.pack(side=RIGHT)
rightNameFrame = Frame(nameFrame, bd=10, width=300)
rightNameFrame.pack(side=RIGHT)
nameButton = Button(rightNameFrame, text="Name this Photon", wraplength=150, width=15, command = setNameCallback)
nameButton.pack()
response3Label = Label(rightNameFrame, bd=10, textvariable=response3, wraplength=200)
response3Label.pack()

flashFrame = Frame(rootFrame, bd=5)
flashFrame.pack(fill='x')

leftFlashFrame = Frame(flashFrame, width=500)
leftFlashFrame.pack(side=LEFT)
L5 = Label(leftFlashFrame, anchor='w', bd=10, text="Optional: Flash Photon\n5) Select binary file from list and click Flash Photon", justify=LEFT, wraplength=300)
L5.pack(fill='x')
fileSelectFrame = Frame(leftFlashFrame)
fileSelectFrame.pack()
fileLabel = Label(fileSelectFrame, text="File Name")
fileLabel.pack(side=LEFT)
fileSelect = Listbox(fileSelectFrame, selectmode=SINGLE)
fileSelect.pack(side=RIGHT)
L5 = Label(leftFlashFrame, anchor='w', bd=10, text="Note: This list is populated from the binary folder on the desktop", justify=LEFT, wraplength=300)
L5.pack(fill='x')
rightFlashFrame = Frame(flashFrame, bd=10, width=300)
rightFlashFrame.pack(side=RIGHT)
flashButton = Button(rightFlashFrame, text="Flash Photon", wraplength=150, width=15, command=setFlashCallback)
flashButton.pack()
response4Label = Label(rightFlashFrame, bd=10, textvariable=response4, wraplength=200)
response4Label.pack()

result = subprocess.run(['ls', './binaries'], stdout=subprocess.PIPE)
tempstr = result.stdout.decode('utf-8')
#print(tempstr)
for s in tempstr.split():
    fileSelect.insert(END, s);
fileSelect.config(height=len(tempstr.split()));

root.mainloop()
