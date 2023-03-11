import pymel.core as pm
import nurbShapes as sh



def ensure_list(item):
    putIntoAlist = {'str': [item], 'Transform': [item], 'list': item}
    listOfTargets = putIntoAlist[type(item).__name__]

    return listOfTargets










































