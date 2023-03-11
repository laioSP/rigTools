import pymel.core as pm

dataset = {}

def make(name=''):
    loc = pm.spaceLocator(n="{}_LOC".format(name))
    locator = pm.ls(loc)[0]
    dataset[locator] = {}
    return locator

def loadData(locator, dataType, data):

    locator.addAttr(dataType, type='string')
    locator.setAttr(dataType, str(data), l=True)
    dataset.setdefault(locator, {})
    dataset[locator].setdefault(dataType, [])
    dataset[locator][dataType].append(data)
    return dataset

def setTranslate(locator, positions):
    return setParameter('translate', locator, positions)

def setRotate(locator, positions):
    return setParameter('rotate', locator, positions)

def setScale(locator, positions):
    return setParameter('scale', locator, positions)

def setTransform(locator, positions):
    setParameter('translate', locator, positions[0])
    setParameter('rotate', locator, positions[1])
    setParameter('scale', locator, positions[2])
    return dataset

def setParameter(attribute, locator, position):
    locator.setAttr(attribute, position)
    loadData(locator, 'placement_{}'.format(attribute), position)
    return dataset

def match(locator, target):
    listOfTargets = basicTools.ensure_list(target)
    listOfLocators = basicTools.ensure_list(locator)

    for loc, pos in zip(listOfLocators, listOfTargets):
        pm.matchTransform(loc, pos)
        loadData(loc, 'position_of', pos)

        translation = loc.getAttr('translate')
        rotation = loc.getAttr('rotate')
        loadData(loc, '{}_translate'.format(pos), translation)
        loadData(loc, '{}_rotate'.format(pos), rotation)

    return dataset

def snap(name, position):
    loc = make(name)
    setTranslate(loc, position)

    return loc