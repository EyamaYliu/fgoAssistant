



import Base_func_wormhole as Base_func
import FGO_func as main
import Serial_wormhole as Serial 
import Battle_Funcs as bf
import Global_Config as gc
import draw 
import sys

Base_func.init_wormhole()


def FGO_process(times=1,servant="Caster_Altria",scriptName = "Continues"):
    for i in range(times):
        times-=1
        main.enter_battle()
        main.apple_feed()
        main.find_friend(servant)
        
        main.battle(scriptName)       
        main.quit_battle()                
        print(" ")
        print(" {} times of battles remain.".format(times))
        print(" Currently {} Gold Apples used, {} Silver Apples used, {} Crafts droped.".format(gc.num_GoldApple_used,gc.num_SilverApple_used,gc.num_Craft))
      
 

def main():
    arg = sys.argv[1]
    Base_func.init_wormhole()
    Serial.mouse_set_zero()
    if arg == "Con":
        FGO_process(10,"Caster_Altria","Continues")
    elif arg == "Once":
        turn = int(sys.argv[2])
        bf.battle_script("Once",turn)
    elif arg == "draw":
        draw.draw_pool()
    print(" All done!") 
        
if __name__=="__main__":
	main()
