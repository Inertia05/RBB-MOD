# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 18:21:05 2021

@author: Administrator
"""

import RBB

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
    
    

