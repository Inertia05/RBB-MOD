# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:10:04 2021

@author: Administrator
"""

import RBB_Patches as RP
import RBB_Create  as RC


RP.WMIAlterDictPatches()
RP.RBB.WMIPatch()    

RP.PrePatches()
RP.RBB.XMLPatch("RBB-Pre")

RP.PricePatches()
RP.RBB.XMLPatch("RBB-Price")

RP.TUnitPatchesRedeployable()
RP.RBB.XMLPatch("RBB-TUnitRedeployable")

RP.ReconPatches()
RP.RBB.XMLPatch("RBB-Recon")
    
RP.TAmmuPatches()
RP.RBB.XMLPatch("RBB-TAmmu")#OneWay

RP.TAmmuPatchesRedeployable()
RP.RBB.XMLPatch("RBB-TAmmuRedeployable")

#RBB-Air-HandWritten.xml #OneWay, Handwritten

#RBB-ReferencedBy.xml #Handwritten, Content: B-5, AVIA-28, F-117 Altitude, FOB Supply, Mi-35's Kokon, Musti-UI(commnented out)

#RBB-Bomb.xml #Handwritten, content: just cluster damage and supply

RP.TAmmuPatchesUniqueNameForTankMainGunsKERounds()
RP.RBB.XMLPatch("RBB-TAmmuUniqueTankKEName")#OneWay


RP.TAmmuPatchesUniqueName()
RP.RBB.XMLPatch("RBB-TAmmuUniqueName")#OneWay


RP.TAmmuPatchesReplaceRocketPodMountedWeapon()
RP.RBB.XMLPatch("RBB-TAmmuRocketPodReplace")#OneWay, start after rocketPod unique name patch

RP.TAmmuPatchesTankGuns()
RP.RBB.XMLPatch("RBB-TAmmuTankGuns")#OneWay

RP.TAmmuPatchesAllHETankGun()
RP.RBB.XMLPatch("RBB-TAmmuAllHETankGuns")#OneWay

RP.RBB.bombPatches(HESupplyFactor=3, HESupRadiFactor=2, CLUSSupplyFactor=100, CLUSSupRadiFactor=1)
RP.RBB.XMLPatch("RBB-Bomb")#Cluster and HE Bomb supply and damage for <1000kg

RP.TempPatch()
RP.RBB.XMLPatch("RBB-TempPatch")


initialNDFName = "NDF_Win"
patched = "_patched"
finalNDFName = "RBB-V3.0"
def renameCommand(fromFileName, toFileName):
    return """rename """+fromFileName+" "+toFileName+"\n\n\n\n"

def applyCommand(datFile, xmlFiles):
    ret = """\n\nWGPatcher apply """+datFile
    for xml in xmlFiles:
        ret += " "+xml
    return ret+"\n\n"

PreOneWayDeploy = "PreOneWayDeploy"
CreateFinal = "RBB-Create-Final"
HashChangeFinal = "RBB-HashChange-Final"
PreNoReturn ="RBB-PreNoReturn"
NoReturn_1 = "NoReturn-1"

dire = """D:
cd D:\WRD MOD\WGPatcher 2.4\n"""


def generateCmd(initialNDFName, dire, finalNDFName):
    orderedFileList = [[initialNDFName, 
                            "createHitRollCommands"],
                       [CreateFinal, 
                            ["RBB-Pre.xml" ,"RBB-Recon.xml", "RBB-Price.xml"]],
                       [PreOneWayDeploy+"-0", 
                            ["RBB-ReferencedBy.xml", "RBB-Bomb.xml"]],
                       [PreOneWayDeploy+"-1", 
                            ["RBB-TAmmuUniqueName.xml","RBB-TAmmuUniqueTankKEName.xml"]],
                       [HashChangeFinal,
                            ["RBB-TAmmuTankGuns.xml","RBB-TAmmuRedeployable.xml","RBB-TUnitRedeployable.xml"]],
                       [PreNoReturn, 
                            ["RBB-TAmmuAllHETankGuns.xml","RBB-Air-HandWritten.xml"]],
                       [NoReturn_1, 
                            ["RBB-TAmmu.xml", "RBB-TAmmuRocketPodReplace.xml"]],
                       ]
    cmd = "\n\n\n"
    cmd += dire
    for i, j in enumerate(orderedFileList):
        fileName = j[0]
        patches = j[1]
        if i != len(orderedFileList)-1:
            nextFileName = orderedFileList[i+1][0]
        else:
            nextFileName = finalNDFName
        if patches == "createHitRollCommands":
            cmd += RC.createHitRollCommands(fileName)
        else:
            cmd += applyCommand(fileName+".dat", patches)
            cmd += renameCommand(fileName.lower()+patched+".dat", nextFileName+".dat")
    cmd += """\n\n\n\nEND"""
    return cmd
        

print(generateCmd(initialNDFName, dire, finalNDFName))
    
    
print(dire+"WGPatcher apply "+finalNDFName+".dat RBB-TempPatch.xml")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


