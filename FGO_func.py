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
#from Notice import sent_message


sys.path.append(gc.default_dir) 
fuse = Base_func.Fuse()

def enter_battle():
    print("Lets enter battle ! \n")
    menuFlag,menuPos = Base_func.match_template("Menu_button")

    # print(menuFlag)
    reenterFlag,reEnterPos = Base_func.match_template("reenter_battle")
    #print('Flag now: ', menu, "Position now: ", Position )   
    
    while not(menuFlag or reenterFlag):
        time.sleep(1)       #Original value is 1
        menuFlag,Position1 = Base_func.match_template("full_menu")
        reenterFlag,Position2 = Base_func.match_template("reenter_battle")
        fuse.increase()
        fuse.alarm()        
    fuse.reset()
    
    if menuFlag:
        LastOrderFlag,Position3 = Base_func.match_template("LastOrder_sign")
        print("enter lastOrder")
        if LastOrderFlag:
            Serial.touch(Position3[0]+230,Position3[1]+50)
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
    recoverFlag,Position = Base_func.match_template("AP_recover")
    if not(recoverFlag):
        print(" No need to feed apple")
        return
    
    goldFlag,goldPosition = Base_func.match_template("Gold_apple")
    if goldFlag:
        Serial.touch(goldPosition[0],goldPosition[1])
        time.sleep(0.5)                
        Serial.touch(goldPosition[0]+300,goldPosition[1]+170) #决定
        gc.num_GoldApple_used += 1
        print(" Feed gold apple success")
        return
    
    silverFlag,silverPosition = Base_func.match_template("Silver_apple")          #check similarity between highlight and normal icon   
    if silverFlag:
        Serial.touch(709,silverPosition[1])
        time.sleep(1.5)            
        Serial.touch(710,470)   #决定
        gc.num_SilverApple_used += 1
        print(" Feed silver apple success")
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

     
def budao():   
    print("补刀啦")
    finFlag,Position = Base_func.match_template("Battlefinish_sign")
    attackFlag = False
    while not(finFlag):
        Serial.touch(960,510)   #点击attack按钮 
        time.sleep(1)       
        Card_index = random.sample(range(0,4),3) #随机三张牌   
        Serial.touch(115+(Card_index[0])*215,430)          
        Serial.touch(115+(Card_index[1])*215,430)  
        Serial.touch(115+(Card_index[2])*215,430)
        print(" Card has pressed")
        while not(finFlag or attackFlag):
            finFlag,Position = Base_func.match_template("Battlefinish_sign")
            attackFlag,Position = Base_func.match_template("Attack_button")
 
        
def quit_battle():
    time.sleep(15)
    finFlag,Position = Base_func.match_template("Battlefinish_sign")
    attackFlag,Position = Base_func.match_template("Attack_button")
    while not(finFlag or attackFlag):
        finFlag,Position = Base_func.match_template("Battlefinish_sign")
        attackFlag,Position = Base_func.match_template("Attack_button")
    if finFlag:
        pass
    elif attackFlag:
        print(" 翻车，进入补刀程序")          #翻车检测
        budao()
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


#improve        
def Master_skill(func = Mystic_Codes.Chaldea_Combat_Uniform, *args):
    # mstSkill,mstSkillPos = Base_func.match_template("master_skill")
    # Serial.touch(mstSkillPos[0],mstSkillPos[1]) #御主技能按键
    Serial.touch(976, 325)
    func(*args)
    # time.sleep(1)    
    WaitForBattleStart()
    # print(" Master skill{} has pressed".format(args[0]))
    time.sleep(1)

    
def character_skill(character_no,skill_no,para=None):   #角色编号，技能编号，选人（可选）
    charPos = (70+(character_no-1)*230+(skill_no-1)*60,488)
    time.sleep(0.2)         #等待技能动画时间  
    Serial.touch(charPos[0],charPos[1])    
    if para != None:
        targetPos = (280+(para-1)*250,350)  #技能选人
        Serial.touch(targetPos[0],targetPos[1])     
    WaitForBattleStart()
    time.sleep(1)         #等待技能动画时间  
    print(" Character{}'s skill{} has pressed".format(character_no,skill_no))

    
def card(NoblePhantasm_no=1):    
    
    attack,attackBtnPos = Base_func.match_template("Attack_button")
    Serial.touch(attackBtnPos[0],attackBtnPos[1])   #点击attack按钮 
    time.sleep(2)       
    Serial.touch(350+(NoblePhantasm_no-1)*200,200)   #打手宝具,参数可选1-3号宝具位
    Card_index = random.sample(range(0,4),2) #随机两张牌   

    card1Pos = (125+(Card_index[0])*210,430)
    card2Pos = (125+(Card_index[1])*210,430)

    Serial.touch(card1Pos[0],card1Pos[1])  
    Serial.touch(card2Pos[0],card2Pos[1])    
    print(" Card has pressed")
    
def battle(): 
    # #判断是否进入战斗界面
    Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)                          #等待战斗开始
    WaitForBattleStart()    
    print("battle started")
    """
    #Turn1
    character_skill(3,1,1)
    character_skill(2,1,1)
    character_skill(1,2)  
    card()
    
    #Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)                          #等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    #Turn2
    character_skill(3,3,1)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3,3,2)
    character_skill(3,3)
    character_skill(3,2)
    card()    
    
    #Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)                          #等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    #Turn3
    character_skill(3,1,1)
    character_skill(2,3,1)
    card()
    """
    # Turn 1
    character_skill(2,1)
    character_skill(3,3,2)
    card(2)
    time.sleep(10)                          #等待战斗动画播放完成
    WaitForBattleStart()    
    
    # Turn 2
    character_skill(3,1)
    character_skill(3,2,1)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3,3,4)
    character_skill(3,1)
    character_skill(3,2,2)
    character_skill(3,3,2)
    card(2)
    time.sleep(10)                          #等待战斗动画播放完成
    WaitForBattleStart()    

    # Turn 3
    character_skill(1,1)
    character_skill(1,3)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 1)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 2)
    card()
    time.sleep(10)                          #等待战斗动画播放完成
    WaitForBattleStart()    

    budao()
