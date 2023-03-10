import pymel.core as pm
import nurbShapes as sh

class groupMaker:
    hierarchy = []

    def __init__(self, hierarchy):
        self.hierarchy = hierarchy
        self.groupDictionary = {}

    def create(self, side, grpName, type):
        nameSide = {'N': '{}_{}', 'C': 'C_{}_{}', 'L': 'L_{}_{}', 'R': 'R_{}_{}'}

        groupName = nameSide[side].format(grpName, type)
        pm.select(cl=True)
        grp = pm.group(n=groupName, em=True)
        return grp

    def delete(self, target):
        pm.delete(target)

    def check(self, target):
        cmds.objExists(target)

    def sequenceParenting(self, target):
        for grp in range(len(self.groupDictionary[target]) - 1):
            pm.parent(self.groupDictionary[target][grp + 1], self.groupDictionary[target][grp])

    def createHierarchy(self, target, side):
        self.groupDictionary[target] = []
        for type in self.hierarchy:
            grp = self.create(side, target, type)
            self.groupDictionary[target].append(grp)

        self.groupDictionary[target].append(target)
        self.sequenceParenting(target)
        return self.groupDictionary[target]

    def emptyGroup(self, name, side):
        self.groupDictionary[name] = []
        for type in self.hierarchy:
            grp = self.create(side, name, type)
            self.groupDictionary[name].append(grp)

        self.sequenceParenting(name)
        return self.groupDictionary[name]

    def aggregate(self, name, target, side):
        grp = self.emptyGroup(name, 'N')


        for t in target:
            if t in self.groupDictionary:
                pm.parent(self.groupDictionary[t][0], grp[-1])
            else:
                pm.parent(t, grp[-1])

        return self.groupDictionary[name]


class center:

    def unpackAxis(self, obj):
        verticesList = self.getVertexPosition(obj)
        x, y, z = verticesList[0]

        return x, y, z

    def average(self, list):
        return sum(list) / (float(len(list)))

    def averageAxis(self, verticesList):
        limit = len(verticesList)
        x = []
        y = []
        z = []

        for vtx in verticesList:
            x.append(vtx[0])
            y.append(vtx[1])
            z.append(vtx[2])

        return [self.average(x), self.average(y), self.average(z)]

    def meshPiece(self, obj):
        check = obj.split('.')[-1].split('[')[0]
        checkedMesh = {
            'f': [self.averageAxis, self.getVertexPosition(obj)],
            'e': [self.averageAxis, self.getVertexPosition(obj)],
            'vtx': [self.unpackAxis, obj]
        }
        return checkedMesh[check][0](checkedMesh[check][1])

    def getPosition(self, obj):
        meshOrTransform = {'transform': pm.objectCenter, 'mesh': self.meshPiece, 'joint': pm.objectCenter}
        return meshOrTransform[pm.objectType(obj)](obj)

    def getListPosition(self, list):
        position = []
        for i in list:
            position.append(self.getPosition(i))
        return position

    def getVertexPosition(self, obj):
        allVertexPositions = []
        vertexList = pm.ls(pm.polyListComponentConversion(obj, tv=True), fl=True)
        for i in vertexList:
            allVertexPositions.append(pm.pointPosition(i).get()[:3])

        return allVertexPositions

    def makeLocator(self, obj, position):
        locatorObj = locator(obj).makeLocator()
        locatorObj.translateBy(position)
        pm.select(cl=True)
        return locatorObj

    def ofAll(self, selected):
        x = [];
        y = [];
        z = []
        for i in selected:
            position = self.getPosition(i)
            x.append(position[0])
            y.append(position[1])
            z.append(position[2])

        position = [self.average(x) , self.average(y) , self.average(z)]
        self.makeLocator("{}_{}".format(selected[0], selected[-1]), position)

    def ofEach(self, selected):
        for i in selected:
            position = self.getPosition(i)
            self.makeLocator(i, position)

    def ofStep(self, selected, step):
        for i in range(0,len(selected),step):
            self.ofAll(selected[i:i+step])

    def subDivide(self, selection, amount):
        firstPosion = self.getPosition(selection[0])
        lastPosion = self.getPosition(selection[-1])
        incrementPostion = []

        if sum(firstPosion) - sum(lastPosion) < 0:
            startPosition = firstPosion
            endPosition = lastPosion

        else:
            startPosition = lastPosion
            endPosition = firstPosion

        for s,e in zip(startPosition, endPosition):
            incrementPostion.append((s-e)/ float(amount+1))

        for a in range(1,amount+1):
            newPosition=[]
            for s,i in zip(startPosition, incrementPostion):
                newPosition.append(s-i*a)

            self.makeLocator("test{}".format(a), newPosition)



drvJntGroup = groupMaker(hierarchy=['OFFSET'])
ctrlGroup = groupMaker(hierarchy=['main', 'POS', 'OFFSET', 'CTRL'])

class ctrl:

    def makeCtrl(self, side, shape, name, size, amountOfSubCtrls, note=''):
        rootCtrl = self.ctrlCurve(side, shape, '{}{}_CTRL'.format(name, note), size)

        digits = len(str(amountOfSubCtrls))
        ctrlsList = [rootCtrl]
        counter = 1.5

        for i in range(amountOfSubCtrls):
            sub = self.ctrlCurve(side, shape, '{}_{:0{}d}_CTRL'.format(name, i + 1, digits), size / float(counter))

            pm.parent(sub[0], ctrlsList[-1][-1])

            pm.connectAttr('{}.subCtrlVis'.format(ctrlsList[-1][-1]), '{}.v'.format(sub[0]))

            ctrlsList.append(sub)
            counter += 1

        #self.jointConstraint(name, ctrlsList[-1][-1])
        return ctrlsList

    def ctrlCurve(self, side, shape, name, size):
        Curve = sh.shapes[shape](name, size)
        pm.addAttr(Curve, ln='subCtrlVis', k=True, min=0, max=1)
        ctrlGrp = ctrlGroup.createHierarchy(Curve, side)

        return ctrlGrp

    def jointConstraint(self, name, driver):
        jnt = pm.joint(n='{}_DRV_JNT'.format(name))
        jntGrp = drvJntGroup.createHierarchy(jnt, 'N')
        pm.parentConstraint(driver, jnt)
        pm.scaleConstraint(driver, jnt)

        return jntGrp


































