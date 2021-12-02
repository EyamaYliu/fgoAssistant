
import Serial_wormhole as Serial 
import Base_func_wormhole as Base_func


def main():

    condition = True    
    i=0

    while condition:
        location = [650,1400]
        Serial.touch(location,interval = 0)
        i+=1
        print(i)
        if i == 10000:  
            condition = False
        
if __name__=="__main__":
	main()
