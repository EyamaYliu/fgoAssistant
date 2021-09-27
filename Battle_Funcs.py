# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:08:29 2020

@author: McLaren
"""

import time
import random
import Serial_wormhole as Serial 
import Base_func_wormhole as Base_func
import FGO_func as mainOperations
import Mystic_Codes


def battle_script(servant):
    if servant == "Caster_Altria":
        
        # Turn 1
        character_skill(3,3,2)
        character_skill(2,1)
        card(2)
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    
        
        # Turn 2
        character_skill(3,1)
        character_skill(3,2,1)
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3,3,4)
        character_skill(3,1)
        character_skill(3,2,2)
        character_skill(3,3,2)
        card(2)
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    

        # Turn 3
        character_skill(1,1)
        character_skill(1,3)
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 1)
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 2)
        card()
        time.sleep(10)                          #等待战斗动画播放完成
        mainOperations.WaitForBattleStart()    
        budao()
    


def Master_skill(func = Mystic_Codes.Chaldea_Combat_Uniform, *args):
    # mstSkill,mstSkillPos = Base_func.match_template("master_skill")
    # Serial.touch(mstSkillPos[0],mstSkillPos[1]) #御主技能按键
    Serial.touch([976, 325])
    func(*args)
    # time.sleep(1)    
    mainOperations.WaitForBattleStart()
    # print(" Master skill{} has pressed".format(args[0]))
    time.sleep(1)

    
def character_skill(character_no,skill_no,para=None):   #角色编号，技能编号，选人（可选）
    time.sleep(0.5)         #等待技能动画时间  
    charPos = (70+(character_no-1)*230+(skill_no-1)*60,488)
    Serial.touch(charPos)    
    if para != None:
        targetPos = (280+(para-1)*250,350)  #技能选人
        Serial.touch(targetPos)     
    mainOperations.WaitForBattleStart()
    print(" Character{}'s skill{} has pressed".format(character_no,skill_no))

    
def card(NoblePhantasm_no=1):    
    
    attack,attackBtnPos = Base_func.match_template("Attack_button")
    Serial.touch(attackBtnPos)   #点击attack按钮 
    time.sleep(2)  
    pantasmCardPos = [350+(NoblePhantasm_no-1)*200,200]     
    Serial.touch(pantasmCardPos)   #打手宝具,参数可选1-3号宝具位
    Card_index = random.sample(range(0,4),2) #随机两张牌   

    card1Pos = [125+(Card_index[0])*210,430]
    card2Pos = [125+(Card_index[1])*210,430]

    Serial.touch(card1Pos)  
    Serial.touch(card2Pos)    
    print(" Card has pressed")


def budao():   
    print("看看要不要补刀啦")
    finFlag,Position = Base_func.match_template("Battlefinish_sign")
    attackFlag = False
    while not(finFlag):
        Serial.touch(960,510)   #点击attack按钮 
        time.sleep(1)       
        Card_index = random.sample(range(0,4),3) #随机三张牌   
        Serial.touch([115+Card_index[0]*215,430])          
        Serial.touch([115+Card_index[1]*215,430])  
        Serial.touch([115+Card_index[2]*215,430])
        print(" Card has pressed")
        while not(finFlag or attackFlag):
            finFlag,Position = Base_func.match_template("Battlefinish_sign")
            attackFlag,Position = Base_func.match_template("Attack_button")
    print("补完了")
 
    




