import nurbShapes
import pymel.core as pm
import basicTools
import ensemble

ctrlsDictionary = {}
ctrlGroup = ensemble.grouper(hierarchy=['main', 'POS', 'OFFSET'])
jntGroup = ensemble.grouper(hierarchy=['OFFSET'])

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
    print(nameList)

    return nameList[0]

def ctrlCurve(side, shape, name, size):
    Curve = nurbShapes.shapes[shape](name, size)
    pm.addAttr(Curve, ln='subCtrlVis', k=True, min=0, max=1)
    ctrlGrp = ctrlGroup.linearHierarchy(Curve, side)

    return ctrlGrp

def jointConstraint(name, driver):
    jnt = pm.joint(n='{}_DRV_JNT'.format(name))
    grp = jntGroup.createHierarchy(jnt, 'N')
    pm.parentConstraint(driver, jnt, mo=True)
    pm.scaleConstraint(driver, jnt, mo=True)

    return jnt

def translate(ctrlsHierarchy, positions):
    positionGroupList = []

    for posGrp, pos in zip(ctrlsHierarchy.values(), positions):
        positionGroupList.append(posGrp[1])
        posGrp[1].setAttr('t', pos)

    return positionGroupList

def makeJoints(name, amount, category, radius):
    pm.select(cl=True)
    jointList = []
    digits = len(str(amount))
    for i in range(amount):
        jnt = pm.joint(n='{}_{:0{}d}_{}_JNT'.format(name, i + 1, digits, category), rad=radius)
        pm.parent(jnt, w=True)
        jointList.append(jnt)
        
    return jointList

def makeControls(side, name, shape, size, amountOfSubCtrls, JointList):
      
    positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), JointList))
    rotation = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, rotation=True), JointList))
    nameList = basicTools.numberedName(name, None, None, len(JointList))
    
    for jnt, pos, rot, nam in zip(JointList, positions, rotation, nameList):
        
        ctrl = make(side, shape, nam, size, amountOfSubCtrls)
        ctrlsDictionary[ctrl][1].setAttr('t', pos)
        ctrlsDictionary[ctrl][1].setAttr('r', rot)
        pm.parentConstraint(ctrlsDictionary[ctrl][-1], jnt)
        pm.scaleConstraint(ctrlsDictionary[ctrl][-1], jnt)

    mainGroups = map(lambda g : ctrlsDictionary[g][0], ctrlsDictionary.keys() )
    grp = ctrlGroup.flatHierarchy(name, 'CTRL', side, mainGroups)
    ctrlsDictionary.clear()
    return grp

def makeFk(side, name, shape, size, amountOfSubCtrls, translation = (0,0,0), rotation = (0,0,0)):
    
    jnt = makeJoints(name, amountOfSubCtrls, 'FK', 1) 
    
    print(jnt[0], translation, rotation)

    jnt[0].setAttr('t', translation)
    jnt[0].setAttr('r', rotation)

    ctrl = makeControls(side, name, shape, size, amountOfSubCtrls, jnt)
    jntGroup = ctrlGroup.flatHierarchy(name ,'FKJNT', side, jnt)
    
    grp = ctrlGroup.flatHierarchy(name, 'FK', side, [ctrl, jntGroup])
    
    fkDictionary = {'ctrl' : ctrl, 'driverJoints' : jnt, 'group' : grp}
    
    pm.select(cl=True)
    ctrlGroup.clearflatGroups()    
    return fkDictionary
    
    
