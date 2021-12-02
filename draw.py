
import time
import Serial_wormhole as Serial 
import Base_func_wormhole as Base_func
import FGO_func as main
import Mystic_Codes
import Global_Config as gc

def draw_pool():   
    empty_pool = False
    while True:
            
        while not empty_pool:
            empty_pool, emptyPos = Base_func.match_template("pool_done")
            Serial.touch(gc.draw10GiftsBtn,interval=0.1)
        if empty_pool:
            reset, resetPos = Base_func.match_template("reset_pool")
            Serial.touch(gc.resetBtn)
            Serial.touch(gc.confirmResetBtn)
            pass
        time.sleep(3)  # Wait for reset finish
        Serial.touch(gc.closeResetDialogBtn)
        empty_pool = False