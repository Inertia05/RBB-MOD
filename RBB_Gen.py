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

RP.UnitPatches()
RP.RBB.XMLPatch("RBB-Unit")

RP.ReconPatches()
RP.RBB.XMLPatch("RBB-Recon")
    
RP.TAmmuPatches()
RP.RBB.XMLPatch("RBB-TAmmu")#OneWay

RP.TAmmuPatchesRedeployable()
RP.RBB.XMLPatch("RBB-TAmmuRedeployable")#OneWay

#RBB-Air-HandWritten.xml #OneWay

#RBB-ReferencedBy.xml #Content: B-5, AVIA-28, F-117 Altitude, FOB Supply, Mi-35's Kokon, Musti-UI
RP.TAmmuPatchesSAM()
RP.RBB.XMLPatch("RBB-TAmmuSAM")

RP.TAmmuPatchesSSM()
RP.RBB.XMLPatch("RBB-TAmmuSSM")

RP.TAmmuPatchesUniqueNameForTankMainGunsKERounds()
RP.RBB.XMLPatch("RBB-TAmmuUniqueTankKEName")#OneWay

RP.TAmmuPatchesTankGuns()
RP.RBB.XMLPatch("RBB-TAmmuTankGuns")#OneWay

RP.TAmmuPatchesAllHETankGun()
RP.RBB.XMLPatch("RBB-TAmmuAllHETankGuns")#OneWay

RP.RBB.bombPatches(HESupplyFactor=3, HESupRadiFactor=2, CLUSSupplyFactor=100, CLUSSupRadiFactor=1)
RP.RBB.XMLPatch("RBB-Bomb")#Cluster and HE Bomb supply and damage for <1000kg

initialNDFName = "NDF_Win"
patched = "_patched"

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
dire = """D:
cd D:\WRD MOD\WGPatcher 2.4"""

cmd =  dire + ("""
WGPatcher apply """+initialNDFName+".dat"+
""" RBB-Pre.xml RBB-Recon.xml RBB-Price.xml RBB-Unit.xml\n\n"""+
#Redeployable

"""WGPatcher apply """+initialNDFName.lower()+patched+".dat"+
""" RBB-ReferencedBy.xml RBB-TAmmuSSM.xml RBB-TAmmuSAM.xml RBB-Bomb.xml\n\n"""+
#Redeployable

renameCommand(initialNDFName.lower()+patched+patched+".dat", PreOneWayDeploy+".dat")
+"\n\n\n\n"
+RC.createHitRollCommands(PreOneWayDeploy)
#NOT Redeployable

+applyCommand(CreateFinal+".dat", [" RBB-TAmmuUniqueTankKEName.xml"])
+renameCommand(CreateFinal.lower()+patched+".dat", HashChangeFinal+".dat")
+applyCommand(HashChangeFinal+".dat",["RBB-TAmmuTankGuns.xml","RBB-TAmmuRedeployable.xml"])
+renameCommand(HashChangeFinal.lower()+patched+".dat", PreNoReturn+".dat")  

+applyCommand(PreNoReturn+".dat",["RBB-TAmmu.xml","RBB-TAmmuAllHETankGuns.xml","RBB-Air-HandWritten.xml"])
#NOT Redeployable

+renameCommand(PreNoReturn.lower()+patched+".dat", "RBB-V3.0.dat")  
+
"""\n\n\n\nEND
""")


print(cmd)
