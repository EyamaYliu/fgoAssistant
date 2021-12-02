# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:08:29 2020

@author: McLaren
"""

import time
import Serial_wormhole as Serial 
import Base_func_wormhole as Base_func
import FGO_func as main
import Mystic_Codes
import Global_Config as gc


def battle_script(script,turn=1):
    if script == "Once":
        print("Fight once")
        
        # Turn 1
        if turn > 1:
            print("skip turn 1")
            pass
        else:
            # Serial.sync_set_zero()
            character_skill(2,1)
            character_skill(2,2,1)
            character_skill(2,3,1)
            character_skill(3,1)
            character_skill(3,2,1)
            character_skill(3,3,1)
            character_skill(1,1)
            character_skill(1,2,2)
            card(1)
            time.sleep(10)                          # 等待战斗动画播放完成
            main.WaitForBattleStart()    

        # Turn 2
        if turn > 2:
            print("skip turn 2")
            pass
        else:
            # Serial.sync_set_zero()
            card(1)
            time.sleep(10)                          # 等待战斗动画播放完成
            main.WaitForBattleStart()   
        
        # Turn 3 
        # Serial.sync_set_zero()
        card(1)
        time.sleep(13)                          # 等待战斗动画播放完成

    elif script == "Continues":

        # Turn 1
        Serial.sync_set_zero()
        character_skill(2,1)
        character_skill(2,2,3)
        character_skill(2,3,3)
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform,3,2,5)
        character_skill(2,1)
        character_skill(2,2,3)
        character_skill(2,3,3)
        character_skill(3,2)
        character_skill(1,3)
        card(3)
        time.sleep(10)                          # 等待战斗动画播放完成
        main.WaitForBattleStart()    

        # Turn 2
        Serial.sync_set_zero()
        card(1)
        time.sleep(10)                          # 等待战斗动画播放完成
        main.WaitForBattleStart()   
        
        # Turn 3 
        Serial.sync_set_zero()
        character_skill(1,3,3)
        card(3)
        time.sleep(13)                          # 等待战斗动画播放完成




def Master_skill(func = Mystic_Codes.Chaldea_Combat_Uniform, *args):
    # mstSkill,mstSkillPos = Base_func.match_template("master_skill")
    # Serial.touch(mstSkillPos[0],mstSkillPos[1]) #御主技能按键
    time.sleep(0.5)         #等待  
    mstSkillBtn = gc.MasterSkillBtn
    Serial.touch(mstSkillBtn)
    func(*args)
    # time.sleep(1)    
    main.WaitForBattleStart()
    # print(" Master skill{} has pressed".format(args[0]))
    time.sleep(1)

    
def character_skill(character_no,skill_no,para=None):   #角色编号，技能编号，选人（可选）
    charPos = [-40+(character_no-1)*230+(skill_no-1)*70,488]
    print(charPos)
    Serial.touch(charPos)    
    if para != None:
        targetPos = (180+(para-1)*240,350)  #技能选人
        Serial.touch(targetPos)     
    time.sleep(3)         #等待技能动画时间  
    main.WaitForBattleStart()
    print(" Character{}'s skill{} has pressed".format(character_no,skill_no))

    
def card(NoblePhantasm_no=1):    
    
    attackBtn = Base_func.match_template("Attack_button")
    attackBtn = gc.AttackBtn
    Serial.touch(attackBtn)   #点击attack按钮 
    time.sleep(2)  
    pantasmCardPos = [250+(NoblePhantasm_no-1)*200,200]     
    Serial.touch(pantasmCardPos)   #打手宝具,参数可选1-3号宝具位

    # Card_index = random.sample(range(0,4),2) #随机两张牌  
    # card1 = [125+(Card_index[0])*210,430]
    # card2 = [125+(Card_index[1])*210,430]

    # Use fixed card 1 and card 2
    card1 = [100,430]
    card2 = [275,430]

    Serial.touch(card1)  
    Serial.touch(card2)    
    print(" Card has pressed")


def budao():   
    print("看看要不要补刀啦")
    finFlag,Position = Base_func.match_template("Battlefinish_sign")
    attackFlag = False
    while not(finFlag):
        Base_func.match_template("Attack_button")
        attackBtn = gc.AttackBtn
        Serial.touch(attackBtn)   #点击attack按钮 
        time.sleep(1)       
        # Card_index = random.sample(range(0,4),3) #随机三张牌   
        # Serial.touch([115+Card_index[0]*215,430])          
        # Serial.touch([115+Card_index[1]*215,430])  
        # Serial.touch([115+Card_index[2]*215,430])
        
        # Use fixed card 1 and card 2   
        card1 = [100,430]
        card2 = [275,430]
        card3 = [420,430]

        Serial.touch(card1)  
        Serial.touch(card2)   
        Serial.touch(card3)  
        print(" Card has pressed")
        while not(finFlag or attackFlag):
            finFlag,Position = Base_func.match_template("Battlefinish_sign")
            attackFlag,Position = Base_func.match_template("Attack_button")
    print("补完了")
 
    




