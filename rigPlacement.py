import pymel as pm
import blueprint
import nurbRig
import ikRig



rigPositions = {}

def make(name, positions):

    groupList = []
    CurveList = nurbRig.makeCurve(name, 'rope', positions, 1)
    Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = nurbRig.driverJoints(name, len(positions), Curve, 'rope')
    groupList.append(CurveGroups)
    groupList.append(driverJNTs)

    return groupList



    # v = nurbRig.rigIt(name, len(positions), 0, 'rope', positions, (1,0,0))
    # print (v)




def IKPlacement(name):
    rig = make(name, [(0.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 20.0, 0.0)])
    rigPositions[name] = rig

    return rigPositions


































