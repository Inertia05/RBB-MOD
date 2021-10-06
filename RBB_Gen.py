# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:10:04 2021

@author: Administrator
"""

import RBB_Patches as RP


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
RP.RBB.XMLPatch("RBB-TAmmu")

RP.TAmmuPatchesSAM()
RP.RBB.XMLPatch("RBB-TAmmuSAM")

RP.TAmmuPatchesSSM()
RP.RBB.XMLPatch("RBB-TAmmuSSM")

RP.TAmmuPatchesUniqueNameForTankMainGunsKERounds()
RP.RBB.XMLPatch("RBB-TAmmuUniqueTankKEName")

RP.TAmmuPatchesTankGuns()
RP.RBB.XMLPatch("RBB-TAmmuTankGuns")

RP.RBB.bombPatches(HESupplyFactor=3, HESupRadiFactor=2, CLUSSupplyFactor=100, CLUSSupRadiFactor=1)
RP.RBB.XMLPatch("RBB-Bomb")

initialNDFName = "NDF_Win"
patched = "_patched"

dire = """D:
cd D:\WRD MOD\WGPatcher 2.4"""
cmd =  dire + ("""
WGPatcher apply """+initialNDFName+".dat"+
""" RBB-Pre.xml RBB-Recon.xml RBB-Price.xml RBB-Unit.xml\n\n"""+
#Redeployable

"""WGPatcher apply """+initialNDFName.lower()+patched+".dat"+
""" RBB-ReferencedBy.xml RBB-TAmmuSSM.xml RBB-TAmmuSAM.xml RBB-Bomb.xml\n\n"""+
#Redeployable

"""WGPatcher apply """+initialNDFName.lower()+patched+patched+".dat"+
""" RBB-TAmmu.xml RBB-TAmmuUniqueTankKEName.xml RBB-TAmmuTankGuns.xml RBB-Air-HandWritten.xml\n\n"""+
#NOT Redeployable

"""END
""")


print(cmd)