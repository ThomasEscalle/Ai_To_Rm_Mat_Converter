# Maya script to convert a Arnold Shader to a Renderman Shader
from maya import cmds

# Recursive function to process the connections of a node
# Convert the Arnold Nodes to Renderman Nodes
# Returns the output connection of the node
# Eg : If the node is a file node, convert it to PxrTexture
def processNode_AiSS_To_PxrSurface(node, expectedType="3"):

    # Check for the type of the node
    nodeType = cmds.nodeType(node)

    print("Processing " + node + " of type " + nodeType)

    # If the node is a "File" node
    if(nodeType == "file"):
        # Create a PxrTexture Node
        pxrTexture = cmds.shadingNode("PxrTexture", asTexture=True)
        # Rename the PxrTexture Node
        pxrTexture = cmds.rename(pxrTexture, "PxrT_" + node)

        # Copy the file texture path
        fileTexturePath = cmds.getAttr(node + ".fileTextureName")

        # Get the name of the fileTextureName attribute
        fileTextureName = fileTexturePath.replace("\\", "/").split("/")[-1]
        fileTextureName = fileTexturePath.split("/")[-1]

        # Get the path to the current project
        projectPath = cmds.workspace(q=True, rootDirectory=True)

        testPath = projectPath + "sourceimages/" + fileTextureName  
        if cmds.file(testPath, q=True, exists=True):
            fileTexturePath = "<ws>/sourceimages/" + fileTextureName


        cmds.setAttr(pxrTexture + ".filename", fileTexturePath, type="string")

        # Connect the PxrTexture Node to the PxrSurface Node
        if(expectedType == "3"):
            return pxrTexture + ".resultRGB"
        elif(expectedType == "1"):
            return pxrTexture + ".resultR"
        
        
    
    # If the node is a AiImage node
    elif(nodeType == "aiImage"):
        # Create a PxrTexture Node
        pxrTexture = cmds.shadingNode("PxrTexture", asTexture=True)
        # Rename the PxrTexture Node
        pxrTexture = cmds.rename(pxrTexture, "PxrT_" + node)

        # Copy the file texture path
        fileTexturePath = cmds.getAttr(node + ".filename")
        
        # Get the name of the fileTextureName attribute
        fileTextureName = fileTexturePath.replace("\\", "/").split("/")[-1]
        fileTextureName = fileTexturePath.split("/")[-1]

        # Get the path to the current project
        projectPath = cmds.workspace(q=True, rootDirectory=True)

        testPath = projectPath + "sourceimages/" + fileTextureName
        if cmds.file(testPath, q=True, exists=True):
            fileTexturePath = "<ws>/sourceimages/" + fileTextureName
        
        cmds.setAttr(pxrTexture + ".filename", fileTexturePath, type="string")




        # Connect the PxrTexture Node to the PxrSurface Node
        if(expectedType == "3"):
            return pxrTexture + ".resultRGB"
        elif(expectedType == "1"):
            return pxrTexture + ".resultR"
    
    # If the node is a remapColor node , convert it to PxrRemap
    elif(nodeType == "remapColor"):
        # Create a PxrRemap Node
        pxrRemap = cmds.shadingNode("PxrRemap", asTexture=True)
        # Rename the PxrRemap Node
        pxrRemap = cmds.rename(pxrRemap, "PxrR_" + node)

        # Copy the color values
        color = cmds.getAttr(node + ".color")[0]
        cmds.setAttr(pxrRemap + ".inputRGB", color[0], color[1], color[2], type="float3")

        # Copy the inputMin values, inputMax values, outputMin values, outputMax values
        inputMin = cmds.getAttr(node + ".inputMin")
        inputMax = cmds.getAttr(node + ".inputMax")
        outputMin = cmds.getAttr(node + ".outputMin")
        outputMax = cmds.getAttr(node + ".outputMax")
        cmds.setAttr(pxrRemap + ".inputMin", inputMin)
        cmds.setAttr(pxrRemap + ".inputMax", inputMax)
        cmds.setAttr(pxrRemap + ".outputMin", outputMin )
        cmds.setAttr(pxrRemap + ".outputMax", outputMax)



        # Check if there is a connection to the color input
        colorInput = cmds.listConnections(node + ".color")
        if colorInput:
            # Process the connection
            output = processNode_AiSS_To_PxrSurface(colorInput[0])
            # Connect the output to the PxrRemap Node
            cmds.connectAttr(output, pxrRemap + ".inputRGB", force=True)

        # Connect the PxrRemap Node to the PxrSurface Node
        if(expectedType == "3"):
            return pxrRemap + ".resultRGB"
        elif(expectedType == "1"):
            return pxrRemap + ".resultR"

    # If the node is a remapValue node , convert it to PxrRemap
    elif(nodeType == "remapValue"):
        # Create a PxrRemap Node
        pxrRemap = cmds.shadingNode("PxrRemap", asTexture=True)
        # Rename the PxrRemap Node
        pxrRemap = cmds.rename(pxrRemap, "PxrR_" + node)

        # Copy the color values
        value = cmds.getAttr(node + ".value")
        cmds.setAttr(pxrRemap + ".inputR", value)

        # Check if there is a connection to the value input
        valueInput = cmds.listConnections(node + ".input")
        if valueInput:
            # Process the connection
            output = processNode_AiSS_To_PxrSurface(valueInput[0], "1")
            # Connect the output to the PxrRemap Node
            cmds.connectAttr(output, pxrRemap + ".inputR", force=True)

        # Connect the PxrRemap Node to the PxrSurface Node
        if(expectedType == "3"):
            return pxrRemap + ".resultRGB"
        elif(expectedType == "1"):
            return pxrRemap + ".resultR"

    # If the node is a bump2d node , convert it to PxrBump
    elif(nodeType == "bump2d"):
        # Create a PxrBump Node
        pxrBump = cmds.shadingNode("PxrBump", asTexture=True)
        # Rename the PxrBump Node
        pxrBump = cmds.rename(pxrBump, "PxrB_" + node)

        # Copy the bump value
        bumpValue = cmds.getAttr(node + ".bumpValue")
        cmds.setAttr(pxrBump + ".inputBump", bumpValue)
        # Copy the bump depth
        bumpDepth = cmds.getAttr(node + ".bumpDepth")
        cmds.setAttr(pxrBump + ".scale", bumpDepth)

        # Check if there is a connection to the bumpValue input
        bumpValueInput = cmds.listConnections(node + ".bumpValue")
        if bumpValueInput:
            # Process the connection
            output = processNode_AiSS_To_PxrSurface(bumpValueInput[0], "1")
            # Connect the output to the PxrBump Node
            cmds.connectAttr(output, pxrBump + ".inputBump", force=True)

        # Connect the PxrBump Node to the PxrSurface Node
        if(expectedType == "3"):
            return pxrBump + ".resultN"
        elif(expectedType == "1"):
            return pxrBump + ".resultN"


def AiSS_To_PxrSurface():
    # Get the selection
    selection = cmds.ls(selection=True)

    # Check if the selection is a AiStandardSurface
    if not selection:
        cmds.warning("Please select a AiStandardSurface Shader")
        return
    
    for sel in selection:
        if cmds.nodeType(sel) != "aiStandardSurface":
            cmds.warning( sel + " is not a AiStandardSurface Shader")
            return
        
        print("Converting " + sel + " to PxrSurface Shader")

        # Get the shading group
        sg = cmds.listConnections(sel, type="shadingEngine")
        # If the shading group is not connected to the AiStandardSurface Shader
        if not sg:
            cmds.warning(sel + " is not connected to a shading group")
            continue


        # Create a PxrSurface Shader
        pxrSurface = cmds.shadingNode("PxrSurface", asShader=True)
        # Rename the PxrSurface Shader
        pxrSurface = cmds.rename(pxrSurface, "PxrS_" + sel)


        # Connect the PxrSurface Shader to the shading group
        cmds.connectAttr(pxrSurface + ".outColor", sg[0] + ".rman__surface", force=True)


        # Check if there is anything connected to the baseColor
        #region Base Color
        baseColor = cmds.listConnections(sel + ".baseColor")
        if baseColor:
            # Process the baseColor connection
            output = processNode_AiSS_To_PxrSurface(baseColor[0])
            # Connect the output to the PxrSurface Shader
            cmds.connectAttr(output, pxrSurface + ".diffuseColor", force=True)
        else :
            print("No baseColor connection found for " + sel)
            # Copy the baseColor value
            baseColor = cmds.getAttr(sel + ".baseColor")[0]
            cmds.setAttr(pxrSurface + ".diffuseColor", baseColor[0], baseColor[1], baseColor[2], type="float3")


        # region specular
        cmds.setAttr(pxrSurface + ".specularFresnelMode", 1)
        cmds.setAttr(pxrSurface + ".specularModelType", 1)        

        specularRoughness = cmds.listConnections(sel + ".specularRoughness")
        if specularRoughness:
            # Process the specularRoughness connection
            output = processNode_AiSS_To_PxrSurface(specularRoughness[0] , "1")
            # Connect the output to the PxrSurface Shader
            cmds.connectAttr(output, pxrSurface + ".specularRoughness", force=True)
        else :
            print("No specularRoughness connection found for " + sel)
            # Copy the specularRoughness value
            specularRoughness = cmds.getAttr(sel + ".specularRoughness" )
            cmds.setAttr(pxrSurface + ".specularRoughness", specularRoughness )


        # Copy the specular color
        specularColor = cmds.getAttr(sel + ".specularColor")[0]
        cmds.setAttr(pxrSurface + ".specularEdgeColor", specularColor[0], specularColor[1], specularColor[2], type="float3")
        cmds.setAttr(pxrSurface + ".specularFaceColor", specularColor[0], specularColor[1], specularColor[2], type="float3")

        specularColor = cmds.listConnections(sel + ".specularColor")
        if specularColor:
            # Process the specularColor connection
            output = processNode_AiSS_To_PxrSurface(specularColor[0])
            # Connect the output to the PxrSurface Shader
            cmds.connectAttr(output, pxrSurface + ".specularEdgeColor", force=True)
            cmds.connectAttr(output, pxrSurface + ".specularFaceColor", force=True)
        else :
            print("No specularColor connection found for " + sel)
            # Copy the specularColor value
            specularColor = cmds.getAttr(sel + ".specularColor")[0]
            cmds.setAttr(pxrSurface + ".specularEdgeColor", specularColor[0], specularColor[1], specularColor[2], type="float3")
            cmds.setAttr(pxrSurface + ".specularFaceColor", specularColor[0], specularColor[1], specularColor[2], type="float3")



        # region Bump
        bump = cmds.listConnections(sel + ".normalCamera")
        if bump:
            # Process the bump connection
            output = processNode_AiSS_To_PxrSurface(bump[0], "1")
            # Connect the output to the PxrSurface Shader
            cmds.connectAttr(output, pxrSurface + ".bumpNormal", force=True)
        else :
            print("No bump connection found for " + sel)
            # Copy the bump value
            bump = cmds.getAttr(sel + ".normalCamera")
            cmds.setAttr(pxrSurface + ".bumpNormal", bump)



AiSS_To_PxrSurface()