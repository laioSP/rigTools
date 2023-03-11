import nurbShapes
import pymel.core as pm
import ensemble

ctrlGroup = ensemble.grouper(hierarchy=['main', 'POS', 'OFFSET', 'CTRL'])
drvJntGroup = ensemble.grouper(hierarchy=['OFFSET'])

def make(side, shape, name, size, amountOfSubCtrls, note=''):
    digits = len(str(amountOfSubCtrls))
    ctrlsDictionary = {}
    counter = 1.5

    for i in range(amountOfSubCtrls):
        ctrlName = '{}_{:0{}d}'.format(name, i + 1, digits)
        sub = ctrlCurve(side, shape, '{}_CTRL'.format(ctrlName), size / float(counter))

        if i != 0:
            ctrlsList = list(ctrlsDictionary.values())
            pm.parent(sub[0], ctrlsList[-1][-1])
            pm.connectAttr('{}.subCtrlVis'.format(ctrlsList[-1][-1]), '{}.v'.format(sub[0]))

        ctrlsDictionary[ctrlName] = sub
        counter += 1
    ctrlsDictionary['ctrl'] = ctrlsDictionary['{}_{:0{}d}'.format(name, amountOfSubCtrls, digits)][-1]

    return ctrlsDictionary

def ctrlCurve(side, shape, name, size):
    Curve = nurbShapes.shapes[shape](name, size)
    pm.addAttr(Curve, ln='subCtrlVis', k=True, min=0, max=1)
    ctrlGrp = ctrlGroup.makeHierarchy(Curve, side)

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


