# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:08:29 2020

@author: McLaren
"""

import time
import FGO_func 
import FGO_func as mainOperations

def battle_script(servant):
    if servant == "CBA":
        
        # Turn 1
        mainOperations.character_skill(2,1)
        mainOperations.character_skill(3,3,2)
        mainOperations.card(2)
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    
        
        # Turn 2
        mainOperations.character_skill(3,1)
        mainOperations.character_skill(3,2,1)
        mainOperations.Master_skill(mainOperations.Mystic_Codes.Chaldea_Combat_Uniform, 3,3,4)
        mainOperations.character_skill(3,1)
        mainOperations.character_skill(3,2,2)
        mainOperations.character_skill(3,3,2)
        mainOperations.card(2)
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    

        # Turn 3
        mainOperations.character_skill(1,1)
        mainOperations.character_skill(1,3)
        mainOperations.Master_skill(mainOperations.Mystic_Codes.Chaldea_Combat_Uniform, 1)
        mainOperations.Master_skill(mainOperations.Mystic_Codes.Chaldea_Combat_Uniform, 2)
        mainOperations.card()
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    
    




