import pymel.core as pm
import placeholder
import maya.cmds as cmds
from random import uniform


# Retrieve the positions of the vertices and unpack the first vertex into x, y, z coordinates
def unpackAxis(obj):
    verticesList = getVertexPosition(obj)
    x, y, z = verticesList[0]

    return x, y, z

# Calculate the average of a list of numbers
def average(list):
    return sum(list) / (float(len(list)))

    # Compute the average position of a list of vertices in the x, y, and z axes
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

# Determine the type of mesh component (vertex, edge, or face) and apply the corresponding function
def meshPiece(obj):
    check = obj.split('.')[-1].split('[')[0]
    checkedMesh = {
        'f': [averageAxis, getVertexPosition(obj)],
        'e': [averageAxis, getVertexPosition(obj)],
        'vtx': [unpackAxis, obj]
    }
    return checkedMesh[check][0](checkedMesh[check][1])

# Get the world position of an object, depending on whether it is a transform, mesh, or joint
def getPosition(obj):
    meshOrTransform = {'transform': pm.objectCenter, 'mesh': meshPiece, 'joint': pm.objectCenter}
    return meshOrTransform[pm.objectType(obj)](obj)

# Get the positions of a list of objects
def getListPosition(list):
    position = []
    for i in list:
        position.append(getPosition(i))
    return position

# Get the world positions of all vertices of a given mesh object
def getVertexPosition(obj):
    allVertexPositions = []
    vertexList = pm.ls(pm.polyListComponentConversion(obj, tv=True), fl=True)
    for i in vertexList:
        allVertexPositions.append(pm.pointPosition(i).get()[:3])

    return allVertexPositions

# Snap a placeholder object to the average position of a group of selected objects
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
    placeholder.snap("{}_{}".format(selected[0], selected[-1]), position, ['t'])

def ofEach(selected):
    for i in selected:
        placeholder.snap(i, getPosition(i), ['t'])

# Snap a placeholder object to each selected object
def ofStep(selected, step):
    for i in range(0,len(selected),step):
        ofAll(selected[i:i+step])

# Subdivide the space between two objects into a specified number of increments and snap placeholders
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

        placeholder.snap("{}to{}_{}".format(selection[0], selection[-1], a), newPosition, ['t'])

# Match the attributes (e.g., translation, rotation) from source objects to target objects
def matchAttributes(source, target, attributeList, axisList, reference):    
    for s, t in zip(source, target):

        if reference == 'world':
            value = getPosition(t)
            s.setAttr('t', value)

        if reference == 'object':

            for axis in axisList:
                for attribute in attributeList:
                    value = t.getAttr("{}{}".format(attribute, axis))                
                    s.setAttr("{}{}".format(attribute, axis), value)

# Randomly move target objects within a specified range (explosion effect)
def explode(target, minimum, maximum, attributeList, axisList, keyCheck, firstKey, lastKey):
    
    for axis in axisList:
        for attribute in attributeList:
            for t in target:
                if keyCheck:
                    pm.setKeyframe(t, at='{}{}'.format(attribute, axis), time=firstKey)
                    t.setAttr("{}{}".format(attribute, axis), uniform(minimum, maximum))
                    pm.setKeyframe(t, at='{}{}'.format(attribute, axis), time=lastKey)
                else:
                    t.setAttr("{}{}".format(attribute, axis), uniform(minimum, maximum))


# Input specific attribute values for an object across specified axes
def inputAttributes(obj, targetValue, attributeList, axisList):  
    for attribute in attributeList: 
        for axis in axisList:

            obj.setAttr("{}{}".format(attribute, axis), targetValue[0])
            del targetValue[0]









