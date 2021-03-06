import csv
from tkinter import *


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

    def __str__(self):
        return self.getCode()

    def __repr__(self):
        return self.getCode()


class ClassButton(Button):
    def __init__(self, mygui, classToGo=None, row=0, column=0, text="", columnspan=2, height=0):
        self.text = StringVar()
        self.classToGo = classToGo
        self.text.set(text)
        if height == 0:
            super().__init__(mygui, textvariable=self.text, command=self.myCommand, font="Helvetica 12")
        else:
            super().__init__(mygui, textvariable=self.text, command=self.myCommand, font="Helvetica 12", height=height)
        super().grid(row=row, column=column, pady=5, sticky=N + E + W + S, columnspan=columnspan, padx=5)

    def myCommand(self):
        if self.classToGo is not None:
            changeCurrentClass(self.classToGo)
            update()

    def setText(self, text):
        self.text.set(text)

    def getClass(self):
        return self.classToGo


# variables and functions for gui
def search():
    global searchbartext
    global allNodes
    global currentClass
    global searchtextvariable
    text = searchbartext.get()
    text = text.upper()

    if allNodes.__contains__(text):
        currentClass = allNodes[text]
        searchbartext.set("")
        update()
    else:
        searchtextvariable.set("Unable to find " + searchbartext.get())


def keyevent(i):
    if i.keysym == "Return":
        search()


def destroyAll():
    global currentObjects
    global currentCanvasObjects
    global circleCanvas

    for obj in currentObjects:
        obj.destroy()
    currentObjects = []

    for obj in currentCanvasObjects:
        circleCanvas.delete(obj)
    currentCanvasObjects = []


def update():
    global currentClass
    global currentObjects
    global checkAllClasses
    global gui

    destroyAll()

    if currentClass is not None:
        recommendedClassLabel = Label(gui, text="Recommended Classes", font='Helvetica 12 underline')
        recommendedClassLabel.grid(row=3, column=0, columnspan=2, sticky=W + E + N + S)
        nextClassLabel = Label(gui, text="Next Classes", font='Halvetica 12 underline')
        nextClassLabel.grid(row=3, column=7, columnspan=2, sticky=W + E + N + S, pady=10)

        currentObjects.append(recommendedClassLabel)
        currentObjects.append(nextClassLabel)

        if checkAllClasses.get() == 1:
            rClassesToRender = currentClass.getAllRecommendeds()
        else:
            rClassesToRender = currentClass.getRequireds()

        nClassesToRender = currentClass.getNexts()

        if len(rClassesToRender) > 5:
            rClassesToRender = rClassesToRender[:5]

        if len(nClassesToRender) > 5:
            nClassesToRender = nClassesToRender[:5]

        row = 4
        for csclass in rClassesToRender:
            classObject = ClassButton(gui, classToGo=csclass, text=csclass.getCode(), row=row, column=0, height=1)
            row = row + 1
            currentObjects.append(classObject)

        row = 4
        for csclass in nClassesToRender:
            classObject = ClassButton(gui, classToGo=csclass, text=csclass.getCode(), row=row, column=7, columnspan=3,
                                      height=1)
            row = row + 1
            currentObjects.append(classObject)

        circle = circleCanvas.create_oval(75, 50, 225, 200, fill="#66b3ff", outline="")
        currentCanvasObjects.append(circle)

        classCode = circleCanvas.create_text(150, 125, text=currentClass.getCode(), font='Helvetica 20 bold')
        currentCanvasObjects.append(classCode)

        classNameLabel = Label(gui, text=currentClass.getName(), font='Helvetica 12', wraplength=250)
        classNameLabel.grid(row=8, column=2, columnspan=5, sticky=N + E + S + W)
        currentObjects.append(classNameLabel)

        currentClassType = currentClass.getType()
        if currentClassType > 0:
            if currentClassType == 1:
                classTypeLabel = Label(gui, text="This Class Fufills the Systems Requirement",
                                       font='Helvetica 12', wraplength=250)
            elif currentClassType == 2:
                classTypeLabel = Label(gui, text="This Class Fufills the Theory & Languages Requirement",
                                       font='Helvetica 12', wraplength=250)
            elif currentClassType == 3:
                classTypeLabel = Label(gui, text="This Class Fufills the Design Requirement",
                                       font='Helvetica 12', wraplength=250)
            elif currentClassType == 4:
                classTypeLabel = Label(gui, text="This Class Fufills the Social Implications Requirement",
                                       font='Helvetica 12', wraplength=250)
            elif currentClassType == 5:
                classTypeLabel = Label(gui, text="This Class Fufills the Probability Requirement",
                                       font='Helvetica 12', wraplength=250)
            elif currentClassType == 6:
                classTypeLabel = Label(gui, text="This Class Fufills the Statistics Requirement",
                                       font='Helvetica 12', wraplength=250)
            else:
                classTypeLabel = Label(gui, text="", font='Helvetica 12', wraplength=250)

            classTypeLabel.grid(row=9, column=2, columnspan=5, sticky=N + E + S + W)
            currentObjects.append(classTypeLabel)


def changeCurrentClass(newClass):
    global currentClass

    currentClass = newClass


gui = Tk(className='Improved CS Graph')
# gui.geometry('800x500')
searchbartext = StringVar()
searchbar = Entry(gui, width=50, textvariable=searchbartext, font='Helvetica 12')
searchbar.grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky=W + E + N + S)
searchbutton = Button(gui, text="Search", command=search, font='Helvetica 12')
searchbutton.grid(row=1, column=6, padx=10, pady=10, sticky=W + E + N + S)
searchtextvariable = StringVar()
searchtextvariable.set("Search a class to begin! Example: 'CS 1101'")
searchtext = Label(gui, textvariable=searchtextvariable, justify=LEFT, font='Helvetica 12')
searchtext.grid(row=2, column=0, columnspan=5, padx=10, sticky=W + E + N + S)
checkAllClasses = IntVar()
checkAllClasses.set(1)
checkbuttonForClasses = Checkbutton(gui, text="Student Recommendations?", command=update,
                                    variable=checkAllClasses, font='Helvetica 12')
checkbuttonForClasses.grid(row=1, column=7, columnspan=4, pady=10, sticky=W + E + N + S)
currentClass = None
currentObjects = []
currentCanvasObjects = []
gui.bind('<Key>', keyevent)

circleCanvas = Canvas(gui, height=300, width=300)
circleCanvas.grid(row=3, rowspan=6, column=2, columnspan=5)

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
