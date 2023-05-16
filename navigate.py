import pymel.core as pm
import placeholder
import maya.cmds as cmds
from random import uniform

def unpackAxis(obj):
    verticesList = getVertexPosition(obj)
    x, y, z = verticesList[0]

    return x, y, z

def average(list):
    return sum(list) / (float(len(list)))

def averageAxis(verticesList):
    limit = len(verticesList)
    x = []
    y = []
    z = []

    for vtx in verticesList:
        x.append(vtx[0])
        y.append(vtx[1])
        z.append(vtx[2])

    return [average(x), average(y), average(z)]

def meshPiece(obj):
    check = obj.split('.')[-1].split('[')[0]
    checkedMesh = {
        'f': [averageAxis, getVertexPosition(obj)],
        'e': [averageAxis, getVertexPosition(obj)],
        'vtx': [unpackAxis, obj]
    }
    return checkedMesh[check][0](checkedMesh[check][1])

def getPosition(obj):
    meshOrTransform = {'transform': pm.objectCenter, 'mesh': meshPiece, 'joint': pm.objectCenter}
    return meshOrTransform[pm.objectType(obj)](obj)

def getListPosition(list):
    position = []
    for i in list:
        position.append(getPosition(i))
    return position

def getVertexPosition(obj):
    allVertexPositions = []
    vertexList = pm.ls(pm.polyListComponentConversion(obj, tv=True), fl=True)
    for i in vertexList:
        allVertexPositions.append(pm.pointPosition(i).get()[:3])

    return allVertexPositions

def ofAll(selected):
    x = [];
    y = [];
    z = []
    for i in selected:
        position = getPosition(i)
        x.append(position[0])
        y.append(position[1])
        z.append(position[2])

    position = [average(x) , average(y) , average(z)]
    placeholder.snap("{}_{}".format(selected[0], selected[-1]), position)

def ofEach(selected):
    for i in selected:
        placeholder.snap(i, getPosition(i))
    return placeholder.dataset

def ofStep(selected, step):
    for i in range(0,len(selected),step):
        ofAll(selected[i:i+step])

def subDivide(selection, amount):
    firstPosition = getPosition(selection[0])
    lastPosition = getPosition(selection[-1])
    incrementPostion = []

    if sum(firstPosition) - sum(lastPosition) < 0:
        startPosition = firstPosition
        endPosition = lastPosition

    else:
        startPosition = lastPosition
        endPosition = firstPosition

    for s,e in zip(startPosition, endPosition):
        incrementPostion.append((s-e)/ float(amount+1))

    for a in range(1,amount+1):
        newPosition=[]
        for s,i in zip(startPosition, incrementPostion):
            newPosition.append(s-i*a)

        placeholder.snap("{}to{}_{}".format(selection[0], selection[-1], a), newPosition)


def matchAttributes(source, target, attributeList, axisList):
    
    for axis in axisList:
        for attribute in attributeList:
            for s, t in zip(source, target):
                value = t.getAttr("{}{}".format(attribute, axis))
                s.setAttr("{}{}".format(attribute, axis), value)

def explode(target, minimum, maximum, attributeList, axisList):
    
    for axis in axisList:
        for attribute in attributeList:
            for t in target:
                t.setAttr("{}{}".format(attribute, axis), uniform(minimum, maximum))


class ConstraintRope:
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
           










