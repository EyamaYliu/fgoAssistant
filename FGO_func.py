# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""
import time
import sys
import random
import Serial_wormhole as Serial 
import Base_func_wormhole as Base_func
import Mystic_Codes
import Global_Config as gc
import Battle_Funcs as bf
#from Notice import sent_message


sys.path.append(gc.default_dir) 
fuse = Base_func.Fuse()

def enter_battle():
    print("Lets enter battle ! \n")
    menuFlag,menuPos = Base_func.match_template("Menu_button")

    reenterFlag,reEnterPos = Base_func.match_template("reenter_battle")
    
    while not(menuFlag or reenterFlag):
        time.sleep(1)       #Original value is 1
        menuFlag,Position1 = Base_func.match_template("Menu_button")
        reenterFlag,Position2 = Base_func.match_template("reenter_battle")
        fuse.increase()
        fuse.alarm()        
    fuse.reset()
    
    if menuFlag:
        LastOrderFlag,Position3 = Base_func.match_template("LastOrder_sign")
        print("enter lastOrder")
        if LastOrderFlag:
            Serial.touch(Position3[0]+130,Position3[1]+50)
            print("Entered last order success")
            return "LastOrder"
        else:
            Serial.touch(menuPos[0],menuPos[1])
            print("Entered default success")
            return "Default"
    elif reenterFlag:
        Serial.touch(reEnterPos[0],reEnterPos[1]) 
        print("Reentered battle success") 
        return "Reenter"
    else:
        print("ReadyToBattle Error")
        sys.exit(0)
        
        
def WaitForBattleStart():
    Flag,Position = Base_func.match_template("Attack_button")
    while not(Flag):
        time.sleep(1)        
        Flag,Position = Base_func.match_template("Attack_button")  
        fuse.increase()
        fuse.alarm()
    fuse.reset()

        
def WaitForFriendShowReady():
    friendFlag,Position = Base_func.match_template("friend_sign")
    noneFlag,Position2 = Base_func.match_template("no_friend")    
    while not(friendFlag or noneFlag):
        time.sleep(1)       
        friendFlag,Position = Base_func.match_template("friend_sign")
        noneFlag,Position2 = Base_func.match_template("no_friend")
        fuse.increase()
        fuse.alarm()
    fuse.reset()

    
def apple_feed(): 
    
    time.sleep(1.5)
    confirmBtn = gc.confirmUseAppleBtnPos
    recoverFlag,Position = Base_func.match_template("AP_recover")
    if not(recoverFlag):
        print(" No need to feed apple")
        return
    
    silverFlag,silverPosition = Base_func.match_template("Silver_apple")          #check similarity between highlight and normal icon   
    if silverFlag:
        Serial.touch(silverPosition[0],silverPosition[1])
        time.sleep(1.5)            
        Serial.touch(confirmBtn[0],confirmBtn[1])   #决定
        gc.num_SilverApple_used += 1
        print(" Feed silver apple success")
        return

    goldFlag,goldPosition = Base_func.match_template("Gold_apple")
    if goldFlag:
        Serial.touch(goldPosition[0],goldPosition[1])
        time.sleep(0.5)                
        Serial.touch(confirmBtn[0],confirmBtn[1])   #决定
        gc.num_GoldApple_used += 1
        print(" Feed gold apple success")
        return
    
    print(" No apple remain")
    Serial.touch(0,0)                
    sys.exit(0)
        
        
def find_friend(servant):
    WaitForFriendShowReady()    
    print("Finding Servant")
    foundFlag,servantPos = Base_func.match_template(servant+"_skill_level")

    attemptnum = 1
    #找310CBA直到找到为止

    while not(foundFlag):
        print(" Didn't find {}, retry. Attempt{}".format(servant,attemptnum))
        #Flag,Position = Base_func.match_template('Refresh_friend')
        Serial.touch(720,110)   #refresh     
        time.sleep(0.5)
        #Flag,Position = Base_func.match_template('Refresh_decide')
        Serial.touch(705,475)   #decide
        WaitForFriendShowReady()   
        foundFlag,Position = Base_func.match_template(servant+"_skill_level")
        attemptnum += 1
        time.sleep(11) 
        
    print(" Success find",servant)
    Serial.touch(servantPos[0],servantPos[1])
    time.sleep(1.5)               

        
def quit_battle():
    print("开始结算本次战斗")
    # time.sleep(15)
    finFlag,Position = Base_func.match_template("Battlefinish_sign")
    attackFlag,Position = Base_func.match_template("Attack_button")
    while not(finFlag or attackFlag):
        finFlag,Position = Base_func.match_template("Battlefinish_sign")
        attackFlag,Position = Base_func.match_template("Attack_button")
    if finFlag:
        pass
    elif attackFlag:
        print(" 翻车，进入补刀程序")          #翻车检测
        bf.budao()
    print(" Battle finished")
    time.sleep(1)
    rainbowFlag,Position = Base_func.match_template("Rainbow_box")  #检测是否掉礼装，若掉落则短信提醒  
    if rainbowFlag:
        gc.num_Craft += 1
    Serial.touch(936,545,6)    
    
    Serial.touch(235,525,2)                #拒绝好友申请
    Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    print(" Quit success")
    time.sleep(1)

