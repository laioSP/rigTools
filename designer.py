import pymel.core as pm
import maya.cmds as cmds
import os
import sys
import json
import placeholder
import constants
import sys



def getProjectFolder(): 
    return pm.workspace(query=True, rootDirectory=True)


def getDocumentPath(fileName):

    home_dir = os.path.expanduser("~")

    if fileName == '':
        fileName = 'untitled'

    if sys.platform.startswith('win'):
        documentFolder = os.path.join(home_dir, 'Documents')
    elif sys.platform.startswith('darwin'):
        documentFolder = os.path.join(home_dir, 'Documents')
    else:
        documentFolder = os.path.join(home_dir, 'Documents')
        

    filePath = os.path.join(documentFolder, "{}.json".format(fileName))    

    return filePath 


def writeBlueprint(data):
    plans = []
    for leaf in data:
        plans.append(vars(leaf))
    path = getProjectFolder() + "blueprint.json"
    with open(path, 'w') as blueprint:
        json.dump(plans, blueprint, indent=4, separators=(', ', ': '))
    return blueprint

def readBlueprint():
    path = getProjectFolder() + "blueprint.json"
    with open(path, 'r') as blueprint:
        dict = json.load(blueprint)
    return dict


def exportBlueprint():
    placeHolders = makeDictionary(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False))    
    documentPath = getDocumentPath(cmds.file(query=True, sceneName=True, shortName=True).split('.')[0])
    writeBlueprint(documentPath, placeHolders)

    print('blueprint exported')
    print(documentPath)


def importBlueprint():

    documentPath = getDocumentPath(cmds.file(query=True, sceneName=True, shortName=True).split('.')[0])
    bluePrint = readBlueprint(documentPath)

    for placeholderData in bluePrint:
        placeholder.snap(placeholderData, list(bluePrint[placeholderData].values()), ['t', 'r', 's'])












































