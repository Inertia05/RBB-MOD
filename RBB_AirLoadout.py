# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 18:21:05 2021

@author: Administrator
"""

import RBB
import RBB_Utilities as UT

def changeMissileModel(aircraftHash, aircraftName, missileModelIndex0th, missileSlot0Based, missileCount, missileModelName):
    
    table = "TMissileCarriageSubDepictionGenerator"
    
    patchName = "Change Model of Missile on plane "+aircraftName+" at weapon slot " + str(missileSlot0Based) +" to "+ missileModelName
    
    conditions = (
    RBB.GeneralConditionReferencedBy(table = "TDepictionTemplate", tableConditions = 
    RBB.GeneralConditionReferencedBy(table = "TTimelyReceiverFactoryCarrier", tableConditions =
    RBB.GeneralConditionReferencedBy(table = "TApparenceModelModuleDescriptor", tableConditions = 
    RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", tableConditions = 
    RBB.GeneralConditions(NameInMenuToken = aircraftHash))))))
    
                  
    changes = ""
    modelFileName = "GameData:/Assets/3D/Units/Ammo/Missiles/"+missileModelName+".Ase2NdfBin"
    for i in range(missileCount):
        index1Based = i+1
        tableConditions =  RBB.GeneralConditions(WeaponIndex = missileSlot0Based+1,
                                                 MissileIndex = index1Based)
        
        tableConditions += RBB.GeneralConditionReference(table = "TDepictionTemplate", tableConditions = 
                           RBB.GeneralConditionReference(table = "TDepictionDescriptor", tableConditions = 
                           RBB.GeneralConditionReference(table = "TResourceMultiMaterialMesh", tableConditions = 
                           RBB.GeneralConditions(FileName = modelFileName))))
        
        changes += RBB.GeneralChangeDictValueObject(prop = "Missiles", key = missileModelIndex0th+i, 
                                                   table = "TMissileCarriageSubDepictionMissileInfo",
                                                   tableConditions = tableConditions)
            
    RBB.GeneralPatch(table, patchName, conditions, changes)
    
#Structure
    

#TUniteAuSolDescriptor
#   TApparenceModelModuleDescriptor
#       TTimelyReceiverFactoryCarrier
#           TDepictionTemplate
#               TMissileCarriageSubDepictionGenerator         unique by unit, contain the missile list
#                   TMissileCarriageSubDepictionMissileInfo    unique by unit, one for each missile, contain weaponIndex and missileIndex
#                       TDepictionTemplate                    unique by unit, contain model, and one object detailing weapon and missile index
#                           TDepictionDescriptor              there are two per unit, one for missile model, one for missile LOD
#                               TResourceMultiMaterialMesh    unique by unit, contain model file name
def changeMissileModelIndirectlyUp1(aircraftIdentifier, aircraftName, missileModelIndex0th, missileSlot0Based, missileCount, missileModelName):
    
    table = "TDepictionDescriptor"#unique per unit
    
    
    patchName = "Change Model of Missile on plane "+aircraftName+" at weapon slot " + str(missileSlot0Based) +" to "+ missileModelName
    

    
                  
    changes = ""
    modelFileName = "GameData:/Assets/3D/Units/Ammo/Missiles/"+missileModelName+".Ase2NdfBin"
    for i in range(missileCount):
        index1Based = i+1
        conditions = (
        RBB.GeneralConditions(SelectorId = "high")+
        RBB.GeneralConditionReferencedBy(table = "TDepictionTemplate", tableConditions = 
        RBB.GeneralConditionReferencedBy(table = "TMissileCarriageSubDepictionMissileInfo", 
                                         tableConditions = 
            (
            RBB.GeneralConditions(WeaponIndex = missileSlot0Based+1,
                                  MissileIndex = index1Based)+
            RBB.GeneralConditionReferencedBy(table = "TMissileCarriageSubDepictionGenerator", tableConditions = 
            RBB.GeneralConditionReferencedBy(table = "TDepictionTemplate", tableConditions = 
            RBB.GeneralConditionReferencedBy(table = "TTimelyReceiverFactoryCarrier", tableConditions =
            RBB.GeneralConditionReferencedBy(table = "TApparenceModelModuleDescriptor", tableConditions = 
            RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", tableConditions = 
                                             UT.ConditionUnitIdentifier(aircraftIdentifier)
                                             )))))
            )
        )))
        

        
        changes += RBB.GeneralChangesObject(prop = "MeshDescriptor", table = "TResourceMultiMaterialMesh", 
                                            tableConditions = RBB.GeneralConditions(FileName = modelFileName))
        
        patchNameI = patchName + " for missile "+str(i) 
            
        RBB.GeneralPatch(table, patchNameI, conditions, changes)
    
    

