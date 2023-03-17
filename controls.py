import nurbShapes
import pymel.core as pm
import ensemble
import basicTools

ctrlGroup = ensemble.grouper(hierarchy=['main', 'POS', 'OFFSET'])
drvJntGroup = ensemble.grouper(hierarchy=['OFFSET'])

ctrlsDictionary = {}

def make(side, shape, name, size, amountOfSubCtrls, note=''):
    
    digits = len(str(amountOfSubCtrls))    
    counter = 1.5    
    nameList = basicTools.alphabetName(name, None, None, amountOfSubCtrls)
    
    for i, nam in zip(range(amountOfSubCtrls), nameList):
        sub = ctrlCurve(side, shape, '{}_CTRL'.format(nam), size / float(counter))

        if i != 0:
            ctrlsList = list(ctrlsDictionary.values())
            pm.parent(sub[0], ctrlsList[-1][-1])
            pm.connectAttr('{}.subCtrlVis'.format(ctrlsList[-1][-1]), '{}.v'.format(sub[0]))

        ctrlsDictionary[nam] = sub
        counter += 1

    return nameList[0]

def ctrlCurve(side, shape, name, size):
    Curve = nurbShapes.shapes[shape](name, size)
    pm.addAttr(Curve, ln='subCtrlVis', k=True, min=0, max=1)
    ctrlGrp = ctrlGroup.linearHierarchy(Curve, side)

    return ctrlGrp

def jointConstraint(name, driver):
    jnt = pm.joint(n='{}_DRV_JNT'.format(name))
    jntGrp = drvJntGroup.createHierarchy(jnt, 'N')
    pm.parentConstraint(driver, jnt)
    pm.scaleConstraint(driver, jnt)

    return jntGrp

def translate(ctrlsHierarchy, positions):
    positionGroupList = []

    for posGrp, pos in zip(ctrlsHierarchy.values(), positions):
        positionGroupList.append(posGrp[1])
        posGrp[1].setAttr('t', pos)

    return positionGroupList

def makeControls(side, name, shape, size, amountOfSubCtrls, JointList):
    
    ctrlsDictionary['ctrl'] = []    
    positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), JointList))
    nameList = basicTools.numberedName(name, None, None, len(JointList))
    for jnt, pos, nam in zip(JointList, positions, nameList):
        
        ctrl = make(side, shape, nam, size, amountOfSubCtrls)
        ctrlsDictionary[ctrl][1].setAttr('t', pos)
        pm.parentConstraint(ctrlsDictionary[ctrl][-1], jnt)
        pm.scaleConstraint(ctrlsDictionary[ctrl][-1], jnt)
        ctrlsDictionary['ctrl'].append(ctrlsDictionary[ctrl][-1])


    return ctrlsDictionary
