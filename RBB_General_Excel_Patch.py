# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 00:06:10 2021

@author: N Z
"""
import RBB
import pandas
import numpy as np
import subprocess
import os


def WriteTAmmuPatchFromTable(sheet, typeArme = None, xlsx = "RBB.xlsx"):
    df = pandas.read_excel(xlsx, sheet, header = 1)
    firstTime = []
    #有武器Hash即默认改变武器性质，有单位Hash即默认基于单位Hash识别重名武器
    for i in range(df["武器名"].size):
        武器Hash值 = df["武器Hash值"][i]
        if not pandas.isna(武器Hash值):
            patchName = df["武器名"][i] + "(weapon), weapon hash = " +str(武器Hash值)
            if patchName in firstTime:
                print("Warning: repeated Weapon Name/Weapon Hash combo at line "+str(i+3)+" in sheet = "+sheet)
            else:
                firstTime.append(patchName)
                tAmmuConditions = WriteTAmmuConditionsFromDF(df, i)+(RBB.TAmmuConditions(TypeArme = typeArme) if typeArme else "")
                tAmmuChanges    = WriteTAmmuChangesFromDF(df, i)
                RBB.TAmmuPatch(patchName,
                               tAmmuConditions,
                               tAmmuChanges)
     
                
                
                
def WriteTAmmuConditionsFromDF(df, i):
    tAmmuConditions = ""

    directKeys = ["原版对地射程(m)", "最小原版对地射程(m)",  
                  "原版对直升机射程(m)",     "原版对空射程(m)",        "原版反舰射程(m)",     "原版反导射程(m)",
                  "最小原版对直升机射程(m)", "最小原版对空射程(m)",     "最小原版反舰射程(m)", "最小原版反导射程(m)",
                  "武器Hash值",  "原版静止精度(%)", "原版移动精度(%)", "原版连发数", "原版齐射数","原版HEAT", "原版KE"]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):
                if ("(%)" in key):
                    directValues[key] = value/100
                elif ("(m)" in key):
                    if (value %175) != 0:
                        raise ValueError("vanilla range is not multiple of 175 at line "+str(i+3)+" in the sheet used")
                    directValues[key] = int(RBB.Range(value))
                else:
                    directValues[key] = value
    shipOnly = False
    ground = [directValues["最小原版对地射程(m)"],     directValues["原版对地射程(m)"]]
    if (directValues["原版反舰射程(m)"] != None) or (directValues["最小原版反舰射程(m)"]!= None):       
        if (directValues["原版对地射程(m)"] != None) or (directValues["最小原版对地射程(m)"]!= None):
            raise ValueError("原版反舰射程和原版对地射程同时存在(反舰射程存在时默认该武器只能反舰)")
        shipOnly = True
        ground = [directValues["最小原版反舰射程(m)"],     directValues["原版反舰射程(m)"]]
        
    tAmmuConditions += RBB.TAmmuConditionsRange(shipOnly=shipOnly, ground = ground,
                             helo   = [directValues["最小原版对直升机射程(m)"],     directValues["原版对直升机射程(m)"]],
                             air    = [directValues["最小原版对空射程(m)"],         directValues["原版对空射程(m)"]],
                             projec = [directValues["最小原版反导射程(m)"],         directValues["原版反导射程(m)"]])
    
    tAmmuConditions += RBB.TAmmuConditionsROF(shotReload = None, shotFxReload  = None, salvoReload = None, 
                       salvoUILength = None, salvoLength = directValues["原版连发数"], 
                       shotSimutane = directValues["原版齐射数"])
    
    if directValues["原版HEAT"]:
        tAmmuConditions += RBB.TAmmuConditionsArme("HEAT", directValues["HEAT"])
        if directValues["原版KE"]:
            raise ValueError("原版KE和原版HEAT不能同时存在")
    elif directValues["原版KE"]:
        tAmmuConditions += RBB.TAmmuConditionsArme("KE", directValues["KE"])
        
    if directValues["武器Hash值"]:
        tAmmuConditions += RBB.TAmmuConditions(Name = directValues["武器Hash值"])
    
    if directValues["原版静止精度(%)"]:
        tAmmuConditions += RBB.TAmmuConditions(acc = [directValues["原版静止精度(%)"],directValues["原版移动精度(%)"]])
    return tAmmuConditions





def WriteTAmmuChangesFromDF(df, i):
    tAmmuChanges = ""

    directKeys = ["新武器Hash值", "HE", "HE半径", "压制", "压制半径","HEAT", "KE", "静止精度(%)", "移动精度(%)", 
                  "对空射程(km)", "对直升机射程(km)", "对地射程(km)", "反舰射程(km)", "反导射程(km)", 
                  "最小对空射程(km)", "最小对直升机射程(km)",	"最小对地射程(km)", "最小反舰射程(km)", "最小反导射程(km)"]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):
                if (key == "HE半径") or (key == "压制半径"):
                    directValues[key] = value*52
                elif ("(%)" in key):
                    directValues[key] = value/100
                elif ("(km)" in key):
                    directValues[key] = RBB.Range(RBB.GameDistanceFor(value))
                else:
                    directValues[key] = value
    
    shipOnly = False
    ground = [directValues["最小对地射程(km)"],     directValues["对地射程(km)"]]
    if (directValues["反舰射程(km)"] != None) or (directValues["最小反舰射程(km)"]!= None):
        if ((directValues["对地射程(km)"] != None) or (directValues["最小对地射程(km)"]!= None)):
            raise ValueError("反舰射程和对地射程同时存在(反舰射程存在时默认该武器只能反舰)")
        shipOnly=True
        ground = [directValues["最小反舰射程(km)"],     directValues["反舰射程(km)"]]
    #https://www.zhihu.com/question/22770770    De Morgan's laws
    tAmmuChanges += RBB.TAmmuChangesRange(shipOnly=shipOnly, ground = ground,
                                          helo   = [directValues["最小对直升机射程(km)"], directValues["对直升机射程(km)"]],
                                          air    = [directValues["最小对空射程(km)"],     directValues["对空射程(km)"]],
                                          projec = [directValues["最小反导射程(km)"],     directValues["反导射程(km)"]])


    if "类型" in df.keys():
       类型 = df["类型"][i]
       if not pandas.isna(类型):   
           if 类型 == "SEAD":
               tAmmuChanges += RBB.TAmmuChangesArme("HE")+RBB.TAmmuChanges(TirIndirect = ["Boolean", True])
               
    if directValues["HEAT"]:
        tAmmuChanges += RBB.TAmmuChangesArme("HEAT", directValues["HEAT"])
    elif directValues["KE"]:
        tAmmuChanges += RBB.TAmmuChangesArme("KE", directValues["KE"])
    
    if directValues["静止精度(%)"]:
        tAmmuChanges += RBB.TAmmuChanges(acc = [directValues["静止精度(%)"],directValues["移动精度(%)"]])
        
    if directValues["新武器Hash值"]:
        tAmmuChanges += RBB.TAmmuChanges(Name = ["LocalisationHash", directValues["新武器Hash值"]])
           
    tAmmuChanges += RBB.TAmmuChangesAOE(HE = [directValues["HE"], directValues["HE半径"]], Sup = [directValues["压制"], directValues["压制半径"]])
    return tAmmuChanges