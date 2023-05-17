import pymel.core as pm
import navigate

groupName='tr4sh071'

def trashGroup():
    
    if pm.objExists(groupName):
        None
    else:
        pm.group(n=groupName, em=True)

    return pm.ls(groupName)[0]

def deleteGroup():
    pm.delete(groupName)

def make(name=''):
    grp = trashGroup()
    loc = pm.spaceLocator(n="{}_LOC".format(name))
    locator = pm.ls(loc)[0]
    pm.parent(locator, grp)
    return locator

def loadData(locator, dataType, data):
    strType = str(dataType)
    locator.addAttr(strType, type='string')
    locator.setAttr(strType, str(data), l=True)    

def snap(target, position):
    loc = make(target)
    for value, axis in zip(position, 'XYZ'):
        loadData(loc, "{}T{}".format(target, axis), value)

    navigate.inputAttributes(loc, position, ['t'], ['x', 'y', 'z'])

    return loc


