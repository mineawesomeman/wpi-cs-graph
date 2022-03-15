import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk


class Node:

    def __init__(self, code="", name="", musts=None, shoulds=None, classType=0):
        if musts is None:
            self.musts = []
        else:
            self.musts = musts

        if shoulds is None:
            self.shoulds = []
        else:
            self.shoulds = shoulds

        self.code = code
        self.name = name
        self.classType = classType
        self.nexts = []

    def getName(self):
        return self.name

    def getType(self):
        return self.classType

    def getCode(self):
        return self.code

    def addNext(self, node):
        self.nexts.append(node)

    def addRequired(self, node):
        self.musts.append(node)

    def addShould(self, node):
        self.shoulds.append(node)

    def getRequireds(self):
        return self.musts

    def getAllRecommendeds(self):
        return self.musts + self.shoulds

    def getNexts(self):
        return self.nexts


# variables and functions for gui

def search():
    

gui = Tk(className='Improved CS Graph')
gui.geometry('700x500')
searchbar = Entry(gui, width=50)
searchbar.grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky=W + E + N + S)
searchbutton = Button(gui, width=5, text="Search", command=search)
searchbutton.grid(row=1, column=6, padx=10, pady=10, sticky=W + E + N + S)
searchtextvariable = StringVar()
searchtextvariable.set("Search a class to begin! Example: 'CS 1101'")
searchtext = Label(gui, textvariable=searchtextvariable, justify=LEFT)
searchtext.grid(row=2, column=0, columnspan=5, padx=10, sticky=W + E + N + S)
checkAllClasses = IntVar()
checkAllClasses.set(1)
checkbuttonForClasses = Checkbutton(gui, width=40,
                                    text="Include Classes Recommended by CS Students?", variable=checkAllClasses)
checkbuttonForClasses.grid(row=1, column=7, columnspan=4, padx=10, pady=10, sticky=W + E + N + S)
currentClass = None

# read csv
allNodes = {}
connectionsToAdd = []

with open('classes.csv') as csvfile:
    csvreader = csv.reader(csvfile)

    for line in csvreader:
        classcode = line[0]
        classname = line[1]
        classtype = int(line[2])
        mustCount = int(line[3])
        shouldCount = int(line[4])
        node = Node(code=classcode, name=classname, classType=classtype)

        for i in range(5, 5 + mustCount):
            if allNodes.__contains__(line[i]):
                node.addRequired(allNodes[line[i]])
                allNodes[line[i]].addNext(node)
            else:
                connectionsToAdd.append((node, line[i], 0))

        for i in range(5 + mustCount, 5 + mustCount + shouldCount):
            if allNodes.__contains__(line[i]):
                node.addShould(allNodes[line[i]])
                allNodes[line[i]].addNext(node)
            else:
                connectionsToAdd.append((node, line[i], 1))

        allNodes[classcode] = node

for connection in connectionsToAdd:
    originalNode = connection[0]
    missingNode = allNodes[connection[1]]

    if connection[2] == 0:
        originalNode.addRequired(missingNode)
        missingNode.addNext(originalNode)
    else:
        originalNode.addShould(missingNode)
        missingNode.addNext(originalNode)

gui.mainloop()
