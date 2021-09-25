



import Base_func_wormhole as Base_func
import FGO_func as mainOperations
import Serial_wormhole as Serial 

Base_func.init_wormhole()


def FGO_process(times=1,servant="Caster_Altria"):
    for i in range(times):
        times-=1
        mainOperations.enter_battle()
        mainOperations.apple_feed()
        mainOperations.find_friend(servant)
        
        mainOperations.battle()        
        mainOperations.quit_battle()                
        print(" ")
        print(" {} times of battles remain.".format(times))
        print(" Currently {} Gold Apples used, {} Silver Apples used, {} Crafts droped.".format(gc.num_GoldApple_used,gc.num_SilverApple_used,gc.num_Craft))
      
 

def main():
    Base_func.init_wormhole()
    Serial.mouse_set_zero()
    # mainOperations.FGO_process(2,"Caster_Altria")
    mainOperations.battle()
    print(" All done!") 
        
if __name__=="__main__":
	main()


