import pymel.core as pm


def make(heightCtrl, targetList, heightZero=0, offset=1.25):
    height = pm.getAttr('{}.ty'.format(heightCtrl))
    divide = pm.createNode('multiplyDivide', n='{}_divide_{}'.format(heightCtrl, height))
    divide.setAttr('input1X', height)
    divide.setAttr('input2Y', height)
    divide.setAttr('input1Z', height)
    divide.setAttr('operation', 2)
    pm.connectAttr('{}.ty'.format(heightCtrl), '{}.input1Y'.format(divide))
    pm.connectAttr('{}.ty'.format(heightCtrl), '{}.input2X'.format(divide))
    pm.connectAttr('{}.ty'.format(heightCtrl), '{}.input2Z'.format(divide))

    if heightZero != 0:
        pm.connectAttr('{}.ty'.format(heightZero), '{}.input2X'.format(divide))

    for target in targetList:
        offsetAttribute = '{}Offset'.format(target)
        if not pm.attributeQuery(offsetAttribute, node=heightCtrl, exists=True):
            pm.addAttr(heightCtrl, ln=offsetAttribute, min=0, max=(offset * 2), k=True, dv=offset)
            # pm.addAttr(heightCtrl, ln=offsetAttribute, k=True , dv=offset)
        power = pm.createNode('multiplyDivide', n='{}_power_{}'.format(heightCtrl, offset))
        power.setAttr('operation', 3)

        for axis in 'XYZ':
            pm.connectAttr('{}.{}'.format(heightCtrl, offsetAttribute), '{}.input2{}'.format(power, axis))
            divide.connectAttr('output{}'.format(axis), '{}.input1{}'.format(power, axis))
            power.connectAttr('output{}'.format(axis), '{}.scale{}'.format(target, axis))