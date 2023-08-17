# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:17:13 2021

@author: Michael
"""
import pandas
#df = pandas.read_excel("RBB MOD 需求数据.xlsx", "主炮Hash值分离", header = 1)
#df["新武器名"] = df["武器名"]+": "+df["单位名"]
#df.to_excel("RBB MOD 需求数据.xlsx", sheet_name = "主炮Hash值分离") 

def SingleToN(singleAcc, N):
    return 1-(1-singleAcc)**N

def NToSingle(NAcc, N):
    return 1-(1-NAcc)**(1/N)