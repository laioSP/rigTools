import pymel.core as pm
from maya import cmds

class locator:
    def __init__(self, obj):
        self.obj = obj
        self.loc = ''
        self.dataList = {'geo': [self.obj]}
        self.newData = ['geo']

    def addData(self, type, data):
        if type in self.dataList:
            self.dataList[type].append(data)
        else:
            self.dataList[type] = [data]

        self.newData.append(type)
        return self.dataList

    def loadData(self):
        for dataType in self.newData:
            self.loc.addAttr(dataType, type='string')
            self.loc.setAttr(dataType, self.dataList[dataType])
        del self.newData[:]

    def makeLocator(self):
        loc = pm.spaceLocator(n="{}_LOC".format(self.obj))
        self.loc = pm.ls(loc)[0]
        return self.loc

class transform:
    def __init__(self):
        pass
        position = locator

    def match(self, target):
        pass
        pm.matchTransform(target, position.loc, pos=True, rot=True)
        position.addData(pm.objectType(target), target)
        position.loadData()

    def bySelection(self):
        pass
        for i in pm.ls(os=True, fl=True):
            match(self)

    def speculate(self):
        pass

class switch:
    def __init__(self, objects, attribute):
        self.objects = objects
        self.attribute = attribute
        self.mayaObject = {True : self.shiftMayaState , False : self.shiftPythonState}
        self.switcher = {True: False, False: True}

    def updateSwitch(self, newSwitch):
        self.switcher = newSwitch
        return self.switcher

    def shiftPythonState(self):
        oldState = self.attribute
        newState = self.switcher[self.attribute]
        self.attribute = newState
        return oldState, newState

    def shiftMayaState(self):
        for obj in pm.ls(self.objects):
            oldState = obj.getAttr(self.attribute)
            newState = self.switcher[oldState]
            obj.setAttr(self.attribute, newState)
            return oldState, newState

    def shift(self):
        oldState, newState = self.mayaObject[pm.objExists(self.objects)]()
        #print '{}_>_{}'.format(oldState, newState)
        return [oldState, newState]


geoVisibility = switch('RootGeometry_Grp', 'v')
jntVisibility = switch("Settings_Ctrl", "jointVis")
ctrlVisibility = switch("Settings_Ctrl", "controlVis")


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

class rope:
    def __init__(self):
        self.groupManager={}

    def makeGroup(self, knot, direction):
        grp=cmds.group(n='{}_{}_Grp'.format(knot, direction), em=True)
        return grp

    def constraintIt(self, linksList, direction):
        anchor, hood = self.groupManager[direction]
        weight=0.33
        for link in range(len(linksList) - 1):
            pm.parentConstraint(linksList[link], linksList[link + 1], mo=True, w=weight)
            pm.scaleConstraint(linksList[link], linksList[link + 1], mo=True, w=weight)
            pm.parentConstraint(anchor, linksList[link], mo=True, w=weight)
            pm.scaleConstraint(anchor, linksList[link], mo=True, w=weight)

    def chain(self,knotsList, direction):
        groupList=[]
        for knot in knotsList:
            groupList.append(self.makeGroup(knot, direction))

        anchor = self.makeGroup('anchor', direction)
        hood = self.makeGroup('hood', direction)
        self.groupManager[direction]= [ anchor, hood]

        pm.parent(anchor, hood)
        for grp in groupList:
            pm.parent(grp,hood)

        return groupList

    def tie(self, knotsList):

        driven = self.chain(knotsList, 'driven')
        forward = self.chain(knotsList, 'forward')
        backward = self.chain(knotsList, 'backward')

        self.constraintIt(forward, 'forward')
        backward.reverse()
        self.constraintIt(backward, 'backward')
        backward.reverse()
        weight = 0.33
        ctrlGrp = self.makeGroup('ctrl', 'ctrl')

        for up, down, drv, knot in zip(forward, backward, driven, knotsList):
            pm.parentConstraint(up, drv, mo=True, w=0.5)
            pm.parentConstraint(down, drv, mo=True, w=0.5)
            pm.scaleConstraint(up, drv, mo=True, w=0.5)
            pm.scaleConstraint(down, drv, mo=True, w=0.5)

            pm.parent(knot, drv)

            ctrl=pm.circle(nr=(0, 0, 1), c=(0, 0, 0))[0]
            pm.addAttr(ctrl, ln='offset', k=True, at='float')
            grp=pm.group(n='{}_offset_grp'.format(knot))
            pm.parent(grp, ctrlGrp)
            pm.matchTransform(grp, knot)
                        
            UpParent = pm.parentConstraint(ctrl, up, mo=True, w=weight)
            UpScale = pm.scaleConstraint(ctrl, up, mo=True, w=weight)
            DownParent = pm.parentConstraint(ctrl, down, mo=True, w=weight)
            DownScale = pm.scaleConstraint(ctrl, down, mo=True, w=weight)
            
            WeightDistribution = lambda node : pm.listAttr(node, k=True)[-1]
            
            ctrl.connectAttr('offset','{}.{}'.format(UpParent, WeightDistribution(UpParent)))
            ctrl.connectAttr('offset','{}.{}'.format(UpScale, WeightDistribution(UpScale)))
            ctrl.connectAttr('offset','{}.{}'.format(DownParent, WeightDistribution(DownParent)))
            ctrl.connectAttr('offset','{}.{}'.format(DownScale, WeightDistribution(DownScale)))
            
            ctrl.setAttr('offset', 0.34)
           



class setDriven:
    def __init__(self, driverAttribute, drivenAttribute, value):
        self.driver = driverAttribute
        self.driven = drivenAttribute
        self.value = value
        self.abbreviationsDict = {'': 'plus', 'plus': 'plus', 'p': 'plus', 'mi': 'plus', 'minus': 'plus',
                                  'plusMinusAverage': 'plus', 'mu': 'multiply', 'd': 'multiply', 'divide': 'multiply',
                                  'multiply': 'multiply'}
        self.offsetNodeDict = {'plus': 'plusMinusAverage', 'multiply': 'multiplyDivide'}
        self.offsetNodeInput = {'plus': 'input1D[0]', 'multiply': 'input1X'}
        self.offsetNodeOutput = {'plus': 'output1D', 'multiply': 'outputX'}
        self.offsetNodeAttr = {'plus': 'input1D[1]', 'multiply': 'input2X'}
        self.offsetType = ''

    def offset(self, difference):
        pass

    def constrain(self):
        pass

    def network(self):
        node = self.abbreviationsDict[self.offsetType]

        offsetNode = pm.createNode(self.offsetNodeDict[node])
        pm.connectAttr(self.driver, '{}.{}'.format(offsetNode, self.offsetNodeInput[node]))
        offsetNode.connectAttr(self.offsetNodeOutput[node], self.driven)
        offsetNode.setAttr(self.offsetNodeAttr[node], self.value)



# dictionary for all functions = {name of the tab : {label of the button : function} }
dictionaryOfFunctions = {
    'common': {'geo vis': geoVisibility.shift, 'jnt vis': jntVisibility.shift,
               'ctrl vis': ctrlVisibility.shift,
               'center of each selection': center().ofEach,
               'center of \nthe selection': center().ofAll
               }
    , 'geo5': {'shpere': cmds.polySphere, 'cube': cmds.polyCube, 'pTorus': cmds.polyTorus,
               }
            }


def UI(functions):
    layoutList = []

    if cmds.window('riggingTools', ex=True):
        cmds.deleteUI('riggingTools')
    cmds.window('riggingTools', tbm=True, mnb=True, mxb=True)
    main = cmds.columnLayout(adj=True)
    lead = cmds.rowLayout(numberOfColumns=2, adj=True, p=main)
    gridFrame = cmds.columnLayout(adj=True, p=main, h=300)

    cmds.button(l='expand', p=lead, c='expand()')
    cmds.button(l='decrease', p=lead)

    tabBar = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=100, p=gridFrame)

    for makeLayout in functions:
        gridlayout = cmds.gridLayout(nrc=(50, 6), cr=True, p=tabBar, ag=True, cwh=[80, 40])

        for buttons in functions[makeLayout]:
            cmds.button(p=gridlayout, l=buttons, c='functions[makeLayout][buttons]()')

        layoutList.append((gridlayout, makeLayout))

    cmds.tabLayout(tabBar, edit=True, tabLabel=layoutList, mt=[2, 1])
    cmds.rowLayout(numberOfColumns=2, adj=True, p=main)
    cmds.button()
    cmds.showWindow()


#UI(dictionaryOfFunctions)

if (cmds.selectPref(tso=True, q=True)==0):
    cmds.selectPref(tso=True)

if cmds.window('riggingTools', ex=True):
    cmds.deleteUI('riggingTools')
cmds.window('riggingTools', tbm=True, mnb=True, mxb=True)
main = cmds.columnLayout(adj=True)
lead = cmds.rowLayout(numberOfColumns=2, adj=True, p=main)
gridFrame = cmds.columnLayout(adj=True, p=main)
tabBar = cmds.columnLayout(p=gridFrame)
centerLayout = cmds.gridLayout(nrc=(10, 10), cr=True, p=tabBar, ag=True, cwh=[80, 40])

step = cmds.intField(v=3,p=centerLayout)
cmds.button(p=centerLayout, l='center of \n selection', c='center().ofAll(pm.ls(os=True, fl=True))')
cmds.button(p=centerLayout, l='center of\n each selected', c='center().ofEach(pm.ls(os=True, fl=True))')
cmds.button(p=centerLayout, l='center of\n step', c='center().ofStep(pm.ls(os=True), cmds.intField(step, q=True, value=True))')
cmds.button(p=centerLayout, l='geo\n vis', c='geoVisibility.shift()')
cmds.button(p=centerLayout, l='joint\n vis', c='jntVisibility.shift()')
cmds.button(p=centerLayout, l='ctrl\n vis', c='ctrlVisibility.shift()')
cmds.button(p=centerLayout, l='subdivide', c='center().subDivide(pm.ls(os=True, fl=True), cmds.intField(step, q=True,  value =True))')
cmds.button(p=centerLayout, l='tie', c='pallete.rope().tie(pm.ls(os=True, fl=True))')

cmds.showWindow()



