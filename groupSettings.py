import ensemble

ctrlGroup = ensemble.grouper(hierarchy=['main', 'POS', 'OFFSET'])
nurbRigGrp = ensemble.grouper(hierarchy=['offset'])


flatGroups = {'ctrl' : ctrlGroup.groupDictionary, 'nurbRig' : nurbRigGrp.groupDictionary}




