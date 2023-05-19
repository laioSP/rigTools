import pymel.core as pm
import navigate
import constants

def placeholdersGroup():
    
    if pm.objExists(constants.placeholderGroup):
        None
    else:
        pm.group(n=constants.placeholderGroup, em=True)

    return pm.ls(constants.placeholderGroup)[0]

def deleteGroup():
    pm.delete(constants.placeholderGroup)

def make(name=''):
    grp = placeholdersGroup()
    loc = pm.spaceLocator(n="{}_LOC".format(name))
    locator = pm.ls(loc)[0]
    
    locator.addAttr(constants.placeholderAttributes[0], type='string')
    locator.setAttr(constants.placeholderAttributes[0], name, l=True)  
    for attr in constants.placeholderAttributes[1:]:
        for axis in constants.axis:        
            locator.addAttr("{}{}".format(attr, axis.upper()), type='float')

    pm.parent(locator, grp)
    return locator

def update(locatorList):
    for locator in locatorList:
        for referenceAttribute, attribute in zip(constants.placeholderAttributes[1:], ['t','r','s']):
            for axis in constants.axis:
                value = locator.getAttr("{}{}".format(attribute, axis))
                locator.setAttr("{}{}".format(referenceAttribute, axis.upper()), value)
    

def snap(target, values, attributeList):
    loc = make(target)
    if type(values) != 'list':
        values = list(values)

    navigate.inputAttributes(loc, values, attributeList, constants.axis)
    update([loc])

    return loc

def reset(locatorList):
    for locator in locatorList:
        valueList = []
        for referenceAttribute in constants.placeholderAllAttributes[1:]:
            valueList.append(locator.getAttr(referenceAttribute))

        navigate.inputAttributes(locator, valueList, ['t','r','s'], constants.axis)


