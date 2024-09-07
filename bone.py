import pymel.core as pm


def make(name, label, position, radius=0.5, side='N'):
    jointList = []

    amount = len(position)
    pm.select(cl=True)
    if amount > 1 :

        digits = len(str(amount))
        nameSide = {'N': '{}_{:0{}d}_{}_JNT', 'C': 'C_{}_{:0{}d}_{}_JNT', 'L': 'L_{}_{:0{}d}_{}_JNT', 'R': 'R_{}_{:0{}d}_{}_JNT'}

        for i, pos in zip(range(amount), position):
            jnt = pm.joint(n=nameSide[side].format(name, i + 1, digits, label), rad=radius, p=pos)
            pm.parent(jnt, w=True)
            jointList.append(jnt)

    else:

        nameSide = {'N': '{}_{}_JNT', 'C': 'C_{}_{}_JNT', 'L': 'L_{}_{}_JNT', 'R': 'R_{}_{}_JNT'}
        jnt = pm.joint(n=nameSide[side].format(name, label), rad=radius, p=position[0])
        pm.parent(jnt, w=True)
        jointList.append(jnt)

    return jointList

def chain(name, label, position, radius=0.5, side='N'):

    jointList = make(name, label, position, radius, side)

    for jnt in range(len(jointList ) -1):
        pm.parent(jointList[jnt +1] ,jointList[jnt])

    return jointList



#155816