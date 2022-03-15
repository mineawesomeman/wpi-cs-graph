import csv


class Node:

    def __init__(self, name="", musts=None, shoulds=None, classType=0):
        if musts is None:
            self.musts = []
        else:
            self.musts = musts

        if shoulds is None:
            self.shoulds = []
        else:
            self.shoulds = shoulds

        self.name = name
        self.clasType = classType
        self.nexts = []

    def getName(self):
        return self.name

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


# read csv
allNodes = {}
connectionsToAdd = []

with open('classes.csv') as csvfile:
    csvreader = csv.reader(csvfile)

    for line in csvreader:
        classname = line[0]
        classtype = int(line[1])
        mustCount = int(line[2])
        shouldCount = int(line[3])
        node = Node(name=classname, classType=classtype)

        for i in range(4, 4+mustCount):
            if allNodes.__contains__(line[i]):
                node.addRequired(allNodes[line[i]])
                allNodes[line[i]].addNext(node)
            else:
                connectionsToAdd.append((node, line[i], 0))

        for i in range(4+mustCount, 4+mustCount+shouldCount):
            if allNodes.__contains__(line[i]):
                node.addShould(allNodes[line[i]])
                allNodes[line[i]].addNext(node)
            else:
                connectionsToAdd.append((node, line[i], 1))

        allNodes[classname] = node

for connection in connectionsToAdd:
    originalNode = connection[0]
    missingNode = allNodes[connection[1]]

    if connection[2] == 0:
        originalNode.addRequired(missingNode)
        missingNode.addNext(originalNode)
    else:
        originalNode.addShould(missingNode)
        missingNode.addNext(originalNode)