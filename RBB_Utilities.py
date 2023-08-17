# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 01:57:25 2021

@author: Administrator
"""
import RBB
import RBB_General_Excel_Patch as GEP

ClassUnit = "TUniteAuSolDescriptor"
ClassModule = "TModuleSelector"
ClassWeaponManager = "TWeaponManagerModuleDescriptor"
#RBB.TurretType___
ClassMountedWeapon = "TMountedWeaponDescriptor"
ClassAmmo = "TAmmunition"


GCRB = RBB.GeneralConditionReferencedBy
GCR  = RBB.GeneralConditionReference


controller = {
                "ScannerConfiguration": "ScannerConfigurationController",
                "Position":             "PositionController",
                "Fuel":                 "FuelController",
                "MouvementHandler":     "MouvementHandlerController",
                "Supply":               "ModernWarfareSupplyController"
             }

def ConditionTurret(WeaponManagerCondition = None, WeaponHash = None):

    ret = ""
    if WeaponManagerCondition:
        ret += GCRB(table = ClassWeaponManager, tableConditions = WeaponManagerCondition)
        
    if WeaponHash:
        ret += GCR(table = ClassMountedWeapon, 
                   tableConditions = GCR(table = ClassAmmo, 
                                         tableConditions = RBB.TAmmuConditions(Name = WeaponHash)))
    return ret


def ConditionWeaponManager(unitHash = None, weaponHash = None, turretType = RBB.TurretTypeAxis, 
                           weaponManagerName = None):
    ret = ""
    if unitHash:
        RBB.checkHashValue(unitHash)
        ret += GCRB(table = ClassModule, 
                    tableConditions = GCRB(table = ClassUnit,
                                           tableConditions = ConditionUnitHash(unitHash)))
    
    if weaponHash:
        RBB.checkHashValue(weaponHash)
        ret += GCR(table = turretType, 
                   tableConditions = GCR(table = ClassMountedWeapon,
                                         tableConditions = GCR(table = ClassAmmo,
                                                               tableConditions = RBB.TAmmuConditions(Name = weaponHash))))
        
    if weaponManagerName:
        ret += RBB.GeneralConditions(_ShortDatabaseName = "WeaponDescriptor_Unit_"+weaponManagerName)
    return ret

def ConditionUnitIdentifier(unitIdentifier):
    ret = ""
    if "Descriptor" in unitIdentifier:
        ret += ConditionDBName(unitIdentifier)
    elif "-"  in unitIdentifier:
        ret += ConditionGUID(unitIdentifier)
    else:
        ret += ConditionUnitHash(unitIdentifier)
    return ret

def ConditionModuleByUnitIdentifier(unitIdentifier, moduleKey = None):
    ret = ""
    
    moduleNameCondition = ""
    if moduleKey in controller.keys():
        moduleNameCondition += RBB.GeneralConditions(ControllerName = controller[moduleKey])    
        
    ret += RBB.GeneralConditionReferencedBy(table = "TModuleSelector", 
                                            tableConditions = (moduleNameCondition+
                                                               RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                tableConditions = ConditionUnitIdentifier(unitIdentifier))
                                                              )
                                            )
    return ret    

def ChangeModuleByUnitHash(targetUnitHash, moduleKey = "MouvementHandler", tableRefered = "TMouvementHandlerLandVehicleDescriptor"):
    ret = ""
    if moduleKey == "ApparenceModel":
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = tableRefered, 
                                                tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                   tableConditions = ConditionUnitHash(targetUnitHash)))
    else:
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = "TModuleSelector", 
                                                tableConditions = RBB.GeneralConditionReference(table = tableRefered, 
                                                                                                tableConditions = RBB.GeneralConditionReferencedBy(table = "TModuleSelector", 
                                                                                                                                                   tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                                                                                                                      tableConditions = ConditionUnitHash(targetUnitHash)))))
    return ret

def ChangeModuleByUnitHashAppend(targetUnitHash, moduleKey = "MissileCarriage", tableRefered = "TMissileCarriageModuleDescriptor"):
    ret = ""
    if moduleKey == "TurretSkeleton":
        ret += RBB.GeneralChangeDictValueObjectAppendKey(prop = "Modules", keyType = "TableString", key = moduleKey, table = tableRefered, 
                                                     tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                        tableConditions = ConditionUnitHash(targetUnitHash)))
    else:
        ret += RBB.GeneralChangeDictValueObjectAppendKey(prop = "Modules", keyType = "TableString", key = moduleKey, table = "TModuleSelector", 
                                                         tableConditions = RBB.GeneralConditionReference(table = tableRefered, 
                                                                                                         tableConditions = RBB.GeneralConditionReferencedBy(table = "TModuleSelector", 
                                                                                                                                                            tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                                                                                                                               tableConditions = ConditionUnitHash(targetUnitHash)))))
    return ret

def ConditionUnitHash(unitHash):
    ret = ""
    RBB.checkHashValue(unitHash)
    
    ret += RBB.GeneralConditions(NameInMenuToken = unitHash)
    return ret

def ConditionGUID(GUID):
    ret = ""
    
    ret += RBB.GeneralConditions(DescriptorId = GUID)
    return ret

def ConditionDBName(DBName):
    ret = ""
    ret += RBB.GeneralConditions(_ShortDatabaseName = DBName)
    return ret

def ConditionInstanceFirst():
    ret = ""
    ret += RBB.GeneralConditions(__order = "first")
    return ret

def ConditionInstanceLast():
    ret = ""
    ret += RBB.GeneralConditions(__order = "last")
    return ret


def ChangeMissileModuleByMissileDBName(targetMissileName, moduleKey = "MouvementHandler", tableRefered = "TMouvementHandler_GuidedMissileDescriptor"):
    ret = ""
    if moduleKey == "Damage":
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = "TModuleSelector", 
                                                tableConditions = (
                                                                    RBB.GeneralConditions(ControllerName = "DamageController")
                                                                   +RBB.GeneralConditionReferencedBy(table = "TUniteDescriptor", 
                                                                                                     tableConditions = ConditionDBName(targetMissileName))
                                                                   )
                                                )
    elif moduleKey in ["MouvementHandler", "ApparenceModel"]:
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = tableRefered, 
                                                tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteDescriptor", 
                                                                                                   tableConditions = ConditionDBName(targetMissileName))
                                               )
    else:
        raise KeyError("Uncategorized module key = "+ moduleKey)
        
    return ret

def ChangeUnitModuleByUnitDBName(targetUnitDBName, moduleKey = "ScannerConfiguration", tableRefered = "TScannerConfigurationDescriptor"):
    ret = ""
    
    if moduleKey in controller.keys():
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = "TModuleSelector", 
                                                tableConditions = (
                                                                    RBB.GeneralConditions(ControllerName = controller[moduleKey])
                                                                   +RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                     tableConditions = ConditionDBName(targetUnitDBName))
                                                                   )
                                                )

    else:
        raise KeyError("Uncategorized module key = "+ moduleKey)
        ret += RBB.GeneralChangeDictValueObject(prop = "Modules", key = moduleKey, table = tableRefered, 
                                                tableConditions = RBB.GeneralConditionReferencedBy(table = "TUniteAuSolDescriptor", 
                                                                                                   tableConditions = ConditionDBName(targetUnitDBName))
                                               )
                                                
        
    return ret

