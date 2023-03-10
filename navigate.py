import pymel.core as pm
import placeholder
def unpackAxis(obj):
    verticesList = getVertexPosition(obj)
    x, y, z = verticesList[0]

    return x, y, z

def average(list):
    return sum(list) / (float(len(list)))

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

def meshPiece(obj):
    check = obj.split('.')[-1].split('[')[0]
    checkedMesh = {
        'f': [averageAxis, getVertexPosition(obj)],
        'e': [averageAxis, getVertexPosition(obj)],
        'vtx': [unpackAxis, obj]
    }
    return checkedMesh[check][0](checkedMesh[check][1])

def getPosition(obj):
    meshOrTransform = {'transform': pm.objectCenter, 'mesh': meshPiece, 'joint': pm.objectCenter}
    return meshOrTransform[pm.objectType(obj)](obj)

def getListPosition(list):
    position = []
    for i in list:
        position.append(getPosition(i))
    return position

def getVertexPosition(obj):
    allVertexPositions = []
    vertexList = pm.ls(pm.polyListComponentConversion(obj, tv=True), fl=True)
    for i in vertexList:
        allVertexPositions.append(pm.pointPosition(i).get()[:3])

    return allVertexPositions

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
    placeholder.snap("{}_{}".format(selected[0], selected[-1]), position)

def ofEach(selected):
    for i in selected:
        placeholder.snap(i, getPosition(i))
    return placeholder.dataset

def ofStep(selected, step):
    for i in range(0,len(selected),step):
        ofAll(selected[i:i+step])

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

        placeholder.snap("{}to{}_{}".format(selection[0], selection[-1], a), newPosition)













