import pymel.core as pm
import navigate
import maya.cmds as cmds
import json
import os

defaultMaya = ['time1', 'sequenceManager1', 'hardwareRenderingGlobals', 'renderPartition', 'renderGlobalsList1',
               'defaultLightList1', 'defaultShaderList1', 'postProcessList1', 'defaultRenderUtilityList1',
               'defaultRenderingList1', 'lightList1', 'defaultTextureList1', 'lambert1', 'standardSurface1',
               'particleCloud1', 'initialShadingGroup', 'initialParticleSE', 'initialMaterialInfo',
               'shaderGlow1', 'dof1', 'defaultRenderGlobals', 'defaultRenderQuality', 'defaultResolution',
               'defaultLightSet', 'defaultObjectSet', 'defaultViewColorManager', 'defaultColorMgtGlobals',
               'hardwareRenderGlobals', 'characterPartition', 'defaultHardwareRenderGlobals', 'ikSystem',
               'hyperGraphInfo', 'hyperGraphLayout', 'globalCacheControl', 'strokeGlobals', 'dynController1',
               'persp', 'perspShape', 'top', 'topShape', 'front', 'frontShape', 'side', 'sideShape',
               'lightLinker1', 'layerManager', 'defaultLayer', 'renderLayerManager', 'defaultRenderLayer',
               'shapeEditorManager', 'poseInterpolatorManager', 'ikSCsolver', 'ikRPsolver', 'ikSplineSolver',
               'hikSolver']
unwantedTypes = [
    'animCurveTL', 'animCurveTA', 'animCurveTU', 'nodeGraphEditorInfo', 'dagPose', 'time',
    'sequenceManager', 'hardwareRenderingGlobals', 'partition', 'renderGlobalsList', 'defaultLightList',
    'defaultShaderList', 'postProcessList', 'defaultRenderUtilityList', 'defaultRenderingList', 'lightList',
    'defaultTextureList', 'lambert', 'standardSurface', 'particleCloud', 'shadingEngine', 'materialInfo',
    'dof', 'renderGlobals', 'renderQuality', 'resolution', 'viewColorManager', 'colorManagementGlobals',
    'hardwareRenderGlobals', 'hwRenderGlobals', 'hyperGraphInfo', 'hyperLayout', 'globalCacheControl',
    'strokeGlobals', 'dynController', 'camera', 'mesh', 'lightLinker', 'displayLayerManager', 'displayLayer',
    'renderLayerManager', 'renderLayer', 'shapeEditorManager', 'poseInterpolatorManager', 'polySphere',
    'polyCube', 'pCubeShape1', 'pCube1', 'pSphereShape1', 'pSphere1', 'polyCylinder', 'pCylinderShape1',
    'pCylinder1', 'polyCone', 'pConeShape1', 'pCone1', 'polyTorus', 'pTorusShape1', 'pTorus1', 'nurbsSphere',
    'nurbsSphereShape1', 'nurbsSphere1', 'nurbsCube', 'nurbsCubeShape1', 'nurbsCube1', 'nurbsCylinder',
    'nurbsCylinderShape1', 'nurbsCylinder1', 'nurbsCone', 'nurbsConeShape1', 'nurbsCone1', 'nurbsTorus',
    'nurbsTorusShape1', 'nurbsTorus1', 'subdivCube', 'subdivCubeShape1', 'subdivCube1', 'subdivSphere',
    'subdivSphereShape1', 'subdivSphere1', 'script'
]

class Unit:
    def __init__(self, name, rotation=None, connections=None, parent=None, children=None, mayaObjectType=None,
                 orientation=None, location=None, radius=None, weights=None):
        self.name = name
        self.rotation = rotation
        self.connections = connections
        self.parent = parent
        self.children = children
        self.type = mayaObjectType
        self.orientation=orientation
        self.location=location
        self.radius=radius
        self.weights=weights

class BlueprintManager:
    def __init__(self):
        # Initializes the BlueprintManager with sets for unit names, units, and joints.
        # Sets up the project path and the path for the blueprint file.
        self.UnitNames = set()
        self.UnitSet = set()
        self.jointSet = set()
        self.projectPath = pm.workspace(query=True, rootDirectory=True)
        self.blueprintPath = self.projectPath + "blueprint.json"

    def UnitToBlueprint(self, unit):
        # Adds a unit to the blueprint. If the unit is a joint, it also adds it to the joint set.
        # If the unit already exists, it refreshes the unit in both the unit and joint sets.
        if unit not in self.UnitSet:
            if unit.type == 'joint':
                self.jointSet.add(unit)
            self.UnitSet.add(unit)
            self.UnitNames.add(unit.name)

        else:
            self.jointSet.remove(unit)
            self.jointSet.add(unit)
            self.UnitSet.remove(unit)
            self.UnitSet.add(unit)

    def AddUnit(self, name):
        # Adds a unit to the manager if it doesn't already exist. Gathers necessary information
        # like rotation, connections, parent, children, object type, orientation, and location,
        # then creates a Unit object and adds it to the blueprint.
        if name not in self.UnitNames:
            self.UnitNames.add(name)
            rotation = None
            connections = {}
            parent = None
            children = []
            mayaObjectType = cmds.objectType(name)

            childrenList = cmds.listRelatives(name, children=True)
            if childrenList:
                for child in childrenList:
                    if cmds.objectType(child) == 'mesh':
                        continue
                    if child not in self.UnitNames:
                        children.append(self.AddUnit(child))
                    else:
                        children.append(self.getUnit(child))


            parentList = cmds.listRelatives(name, parent=True)
            if parentList:
                if parentList[0] not in self.UnitNames:
                    parent = self.AddUnit(parentList[0])
                else:
                    parent = self.getUnit(parentList[0])


            if mayaObjectType == "joint":
                orientation = cmds.getAttr(name + ".jointOrient")
                radius = cmds.getAttr(name + ".radius")
                weights = self.getWeights(name)
            else:
                orientation = None
                radius = None
                weights = None

            if mayaObjectType in ["joint", "transform"] and cmds.getAttr(name+'.t'):
                location = pm.xform(name, q=True, ws=True, t=True)
            else:
                location = None

            connectedAttrs = cmds.listConnections(name, s=1, p=1)
            if connectedAttrs:
                for connected in connectedAttrs:
                    if '.' in connected:
                        fullAttr = connected.split('.')[1]
                        if fullAttr not in connectedAttrs:
                            connections[fullAttr] = []
                        connections[fullAttr].append(connected)

            unit = Unit(name, rotation=rotation, connections=connections, parent=parent, children=children, mayaObjectType=mayaObjectType,
                        orientation=orientation, location=location, radius=radius, weights=weights)

            self.UnitToBlueprint(unit)
            return unit


    def setUnit(self, name, rotation=None, connections=None, parent=None, children=None, mayaObjectType=None,
                orientation=None, location=None, radius=None, weights=None, inputs=None, outputs=None, setAttribute=None):
        # Creates a new Unit object with the specified parameters and adds it to the blueprint.
        if name in self.UnitNames:
            return None
        else:
            unit = Unit(name, rotation=rotation, connections=connections, parent=parent, children=children,
                        mayaObjectType=mayaObjectType, orientation=orientation, location=location, radius=radius, weights=weights)
            self.UnitToBlueprint(unit)


    def getUnitConnections(self, driver):
        connectedNodes = {}
        connections = cmds.listConnections(driver, plugs=True, connections=True)

        if connections:
            for i in range(0, len(connections), 2):

                sourceAttr = connections[i]
                destAttr = connections[i + 1]

                # if sourceAttr !='message' and destAttr !='message':
                sourceNode, sourceAttrName = sourceAttr.split('.', 1)
                destNode, destAttrName = destAttr.split('.', 1)

                if (destNode not in connectedNodes and
                        cmds.objectType(destNode) not in unwantedTypes and
                        cmds.objectType(sourceNode) not in unwantedTypes):

                    connectedNodes[destNode] = []

                    connectedNodes[destNode].append({
                        'sourceAttr': sourceAttrName,
                        'destAttr': destAttrName,
                        'sourceNode': sourceNode
                    })

        return connectedNodes

    def getWeights(self, jnt):
        skin_clusters = cmds.ls(cmds.listConnections(jnt, type='skinCluster'), type='skinCluster')

        weights = {}

        for skin_cluster in skin_clusters:
            geometry = cmds.skinCluster(skin_cluster, query=True, geometry=True)[0]
            num_verts = cmds.polyEvaluate(geometry, vertex=True)

            for i in range(num_verts):
                vertex = '{}.vtx[{}]'.format(geometry, i)
                vertex_weight = cmds.skinPercent(skin_cluster, vertex, transform=jnt, query=True)
                weights[vertex] = vertex_weight

        return weights

    def refreshBlueprint(self):
        # Clears the current unit and joint sets, then repopulates them by adding all joints
        # in the scene to the blueprint.
        self.UnitSet.clear()
        self.jointSet.clear()
        for jnt in cmds.ls(typ="joint"):
            self.AddUnit(jnt)

    def getUnit(self, unitName):
        # Searches for and returns a unit by name from the unit set. Returns None if not found.
        result = None
        for unit in self.UnitSet:
            print(unit.name, unitName)
            if unit.name == unitName:
                result = unit

        if result == None:
            result = self.AddUnit(unitName)

        return result


    def writeBlueprint(self, refresh=False):
        # Saves the current blueprint to a JSON file. If a blueprint file already exists, it is removed first.
        # The blueprint is then written to the file with a formatted output.
        if os.path.exists(self.blueprintPath):
            os.remove(self.blueprintPath)
        # if refresh:
        #     for unit in self.UnitSet:
        #         cmds.delete(unit.name)
        self.UnitSet.clear()
        self.UnitNames.clear()
        self.jointSet.clear()
        for mayaObject in cmds.ls():
            if mayaObject not in defaultMaya and cmds.objectType(mayaObject) not in unwantedTypes:
                self.AddUnit(mayaObject)

        plans = []
        for unit in self.UnitSet:
            blueprintUnit = {
                "name": unit.name,
                "rotation": unit.rotation,
                "connections": unit.connections,
                "parent": unit.parent.name if unit.parent else None,
                "children": self.stringFromInstance(unit.children),
                "type": unit.type,
                "orientation": unit.orientation,
                "location": unit.location,
                "radius": unit.radius,
                "weights": unit.weights
            }

            plans.append(blueprintUnit)
        message(plans)
        with open(self.blueprintPath, 'w') as blueprint:
            json.dump(plans, blueprint, indent=4, separators=(', ', ': '))

        message("Blueprint saved at: {}".format(self.blueprintPath))

        return blueprint

    def stringFromInstance(self, instance):
        if isinstance(instance, Unit):
            stringList=[]
            for obj in instance:
                stringList.append(obj)
            return stringList
        else:
            return None

    def __str__(self):
        # Returns a formatted string representation of all units in the unit set.
        units_str = ""
        for unit in self.UnitSet:
            units_str += """
        name: {}
            connections = {}
            parent = {}
            children = {}
            type = {}""".format(unit.name, unit.connections, unit.parent, unit.children, unit.type)
        return units_str

    def toString(self):
        # Prints the string representation of the blueprint.
        print(self.__str__())

    def buildSkeleton(self):
        # Builds a skeleton in the scene based on the units in the blueprint.
        # It creates joints that don't already exist in the scene and parents child joints accordingly.
        currentJoints = cmds.ls(typ='joint')
        for unit in self.UnitSet:
            if unit.type == 'joint' and unit.name not in currentJoints:
                jnt = pm.joint(n=unit.name, o=unit.orientation[0], p=unit.location, rad=0.01, a=True)
                pm.select(cl=True)
            else:
                continue
        for unit in self.UnitSet:
            if unit.children:
                for child in unit.children:
                    print(child.name, unit.name)
                    pm.parent(child.name, unit.name)

    def rebuildNodeNetwork(self):
        attributeList = lambda node : cmds.listAttr(node, m=1)
        lateConnections = {}
        for unit in self.UnitSet:
            for destNode, attrs in unit.connections.items():
                if not cmds.objExists(destNode):
                    cmds.createNode(destNode.type, name=unit.name)

                for attr in attrs:
                    sourceNode = attr['sourceNode']
                    sourceAttr = attr['sourceAttr']
                    destAttr = attr['destAttr']

                    # Ensure the sourceNode exists before attempting to create or connect it
                    if not cmds.objExists(sourceNode):
                        cmds.createNode(unit.type, name=sourceNode)  # Adjusting to create the correct type
                    if sourceAttr not in attributeList(sourceNode) or destAttr not in attributeList(destNode):
                        lateConnections[f"{sourceNode}.{sourceAttr}"] = f"{destNode}.{destAttr}"
                    else:
                        cmds.connectAttr(f"{sourceNode}.{sourceAttr}", f"{destNode}.{destAttr}", force=True)

        for neverToLate in lateConnections:
            cmds.connectAttr(neverToLate, lateConnections[neverToLate], force=True)

    def loadConstraints(self):
        # Loads constraints for the joints in the joint set. Applies parent and scale constraints
        # based on the connections defined in the blueprint.
        for unit in self.jointSet:
            if unit.connections:
                for node in unit.connections:
                    if "parentConstraint" in node:
                        cmds.parentConstraint(unit.connections['joint'], unit.connections['transform'], mo=True)
                    if "scaleConstraint" in node:
                        cmds.scaleConstraint(unit.connections['joint'], unit.connections['transform'], mo=True)

    def loadWeights(self):
        for unit in self.jointSet:
            pass

    def rebuildSkeleton(self):
        # Rebuilds the skeleton by deleting existing joints and recreating them based on the blueprint.
        # Then re-establishes the parent-child relationships.
        newJointsList = []
        for oldJnt in cmds.ls(typ="joint"):
            if oldJnt in self.UnitNames:
                unit = self.getUnit(oldJnt)
                cmds.delete(oldJnt)
                newJnt = pm.joint(n=unit.name, o=unit.orientation[0], p=unit.location, rad=0.01, a=True)
                pm.select(cl=True)
                newJointsList.append(unit)

        for unit in newJointsList:
            if unit.children:
                for child in unit.children:
                    pm.parent(child.name, unit.name)

    def importBlueprint(self):
        # Imports a blueprint from a JSON file and sets up units in the manager.
        path = self.blueprintPath
        blueprintDictionary = {}
        with open(path, 'r') as blueprint:
            blueprintDictionary = json.load(blueprint)

        late=[]
        for mayaObject in blueprintDictionary:
            name = mayaObject["name"]
            rotation = mayaObject["rotation"]
            connections = mayaObject["connections"]
            parent = []
            children = []
            mayaObjectType = mayaObject["type"]
            orientation = mayaObject["orientation"]
            location = mayaObject["location"]

            if mayaObject["children"]:
                for child in mayaObject["children"]:
                    if child not in self.UnitNames:
                        late.append(mayaObject)
                        continue
                    else:
                        children.append(self.getUnit(child))

            if mayaObject["parent"]:
                for dad in mayaObject["parent"]:
                    if dad not in self.UnitNames:
                        late.append(mayaObject)
                        continue
                    else:
                        parent.append(self.getUnit(dad))

            self.setUnit(name, rotation, connections, parent, children, mayaObjectType,
                         orientation, location)

        message("Blueprint from: {}\nLoaded".format(self.projectPath))

    def loadBlueprint(self):
        # Loads a blueprint, builds the skeleton, and applies constraints in the scene.
        self.importBlueprint()
        self.buildSkeleton()
        # self.rebuildNodeNetwork()




def message(text):
    print("\n///////////////////////////\n"
          "{}"
          "\n///////////////////////////\n".format(text))


def getTree(root, visitedBranches=None):
    if visitedBranches is None:
        visitedBranches = {}

    if isinstance(root, list):
        for branch in root:
            if branch not in visitedBranches:
                visitedBranches[branch] = []
            if cmds.listRelatives(branch, children=True):
                children = cmds.listRelatives(branch, children=True)

                for child in children:
                    if child not in visitedBranches:
                        visitedBranches[branch].append(child)
                        getTree(child, visitedBranches)
    else:
        if root not in visitedBranches:
            visitedBranches[root] = []
            children = cmds.listRelatives(root, children=True)
            if children:
                for child in children:
                    if child not in visitedBranches:
                        visitedBranches[root].append(child)
                        getTree(child, visitedBranches)

    return visitedBranches