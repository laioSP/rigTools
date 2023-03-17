import ensemble

ctrlGroup = ensemble.grouper(hierarchy=['main', 'POS', 'OFFSET'])
nurbRigGrp = ensemble.grouper(hierarchy=['offset'])


allGroups = {'ctrl' : ctrlGroup.groupDictionary, 'nurbRig' : nurbRigGrp.groupDictionary}




