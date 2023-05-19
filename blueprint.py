import pymel.core as pm
import maya.cmds as cmds
import os
import sys
import json
import placeholder
import constants



def makeDictionary(locatorList):
    placeHolders = {}

    for loc in locatorList:
        key = loc.getAttr('reference')
        if key not in placeHolders:
            placeHolders[key] = {}

        for attr in constants.placeholderAllAttributes[1:]:    
            placeHolders[key][attr] = loc.getAttr(attr)

    return placeHolders



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

def readBlueprint(documentPath):
    with open(documentPath, 'r') as file:
        bluePrint = json.load(file)

    return bluePrint

def writeBluePrint(documentPath, data):
    with open(documentPath, 'w')  as blueprint:
        bluePrint = json.dump(data, blueprint, indent=4, ensure_ascii=False)

    return bluePrint

def exportBlueprint():
    placeHolders = makeDictionary(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False))    
    documentPath = getDocumentPath(cmds.file(query=True, sceneName=True, shortName=True).split('.')[0])
    writeBluePrint(documentPath, placeHolders)

    print('blueprint exported')
    print(documentPath)


def importBlueprint():

    documentPath = getDocumentPath(cmds.file(query=True, sceneName=True, shortName=True).split('.')[0])
    bluePrint = readBlueprint(documentPath)

    for placeholderData in bluePrint:
        placeholder.snap(placeholderData, list(bluePrint[placeholderData].values()), ['t', 'r', 's'])












































