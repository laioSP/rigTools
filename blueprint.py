import pymel.core as pm
import os
import json




def make():
    projectPath = pm.workspace(q=True, rootDirectory=True)
    blueprintPath = os.path.join(projectPath, 'blueprint.json')

    with open(blueprintPath, 'w')  as blueprint:
        json.dump()

    blueprint.close()




def writeOnBlueprint(data):
    print(data)











































