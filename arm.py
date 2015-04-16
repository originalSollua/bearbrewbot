import serial
import time
class Arm:
    def __init__(self):   
        self.CEN_VAL = 1250
        self.out = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            xonxoff=serial.XOFF,
            rtscts=False,
            dsrdtr=False,
        )
        
        self.out.open()
        self.out.isOpen()
        self.out.write("#0 P1500 S250 \r")
        self.out.write("#1 P1500 S250 \r")
        self.out.write("#2 P1500 S250 \r")
        self.out.write("#3 P1500 S250 \r")
        self.out.write("#4 P1500 S250\r")
    def terminate(self):
        esc = 27
        
        self.out.write("#0 P1500 S250"+str(esc))
        self.out.write("#1 P1500 S250"+str(esc))
        self.out.write("#2 P1500 S250"+str(esc))
        self.out.write("#3 P1500 S250"+str(esc))
        self.out.write("#4 P1500 S250"+str(esc))
        self.out.close()
    def center(self):

        self.out.write("#0 P1500 S250\r")
        self.out.write("#1 P1500 S250\r")
        self.out.write("#2 P1500 S250\r")
        self.out.write("#3 P1500 S250\r")
        self.out.write("#4 P1500 S250\r")
        
    def open(self):
        self.center()
        time.sleep(1)

        self.out.write("#0 P1900 S250 \r")
        time.sleep(3)
        self.out.write("#1 P1000 S250 \r")
        time.sleep(1) 
        self.out.write("#0 P1450 S250 \r")
        time.sleep(2)
        self.out.write("#1 P1400 S250 \r")
        time.sleep(2)
        self.out.write("#0 P1000 S250 \r")
        time.sleep(2)
        self.out.write("#0 P1600 S250 \r")
        time.sleep(2)
        self.center()

    def close(self):
        self.center()
        time.sleep(2)
        self.out.write("#1 P1700 S250 \r")
        time.sleep(2)    
        self.out.write("#0 P250 S250 \r")
        time.sleep(3)
        self.out.write("#1 P1360 S250 \r")
        time.sleep(2)
        self.out.write("#2 P1700 S250 \r")
        time.sleep(1)
        self.out.write("#0 P1250 S1000 \r")
        time.sleep(1)
        self.center()       

    def empty_basket(self):
        self.center()
        time.sleep(2)
        #initial grab positioning. problematic
        self.out.write("#0 P1300 S250 \r")
        time.sleep(3)
        self.out.write("#3 P600 S250 \r")
        time.sleep(4)
        self.out.write("#1 P1280 S250 \r")
        time.sleep(2)
        self.out.write("#2 P1570 S250 \r")
        time.sleep(2)
        self.out.write("#4 P2500 S500 \r")
        time.sleep(4)
        self.out.write("#2 P1410 S250 \r")
        time.sleep(2)
        self.out.write("#3 P500 S250 \r")
        time.sleep(2)
        self.out.write("#1 P1600 S250 \r")
        time.sleep(2)
        self.out.write("#0 P1875 S250 \r")
        time.sleep(2)
        self.out.write("#2 P1960 S250 \r")
        time.sleep(2)
        self.out.write("#3 P875 S250 \r")
        time.sleep(2)
        self.out.write("#1 P1010 S250 \r")
        time.sleep(3)
        self.out.write("#3 P1275 S250 \r")
        time.sleep(4)
        self.out.write("#4 P500 S500 \r")
        time.sleep(3)
        self.out.write("#1 P950 S250 \r")
        time.sleep(2)
        self.out.write("#1 P1500 S250 \r")
        time.sleep(2)
        self.out.write("#2 P1500 S250 \r")
        time.sleep(2)
        self.out.write("#3 P1500 S250 \r")
        time.sleep(2)
        self.out.write("#4 P1500 S250 \r")
        time.sleep(2)
        self.out.write("#0 P1500 S250 \r")
        time.sleep(2)

    def load_basket(self):
        self.center()
        time.sleep(2)
        self.out.write("#0 P2500 S250 \r")
        time.sleep(4)
        self.out.write("#1 P975 S250 \r")
        time.sleep(3)
        self.out.write("#2 P1750 S250 \r")
        time.sleep(2)
        self.out.write("#3 P950 S250 \r")
        time.sleep(3)
        self.out.write("#1 P905 S250 \r")
        time.sleep(2)
        self.out.write("#3 P1090 S250 \r")
        time.sleep(2)
        self.out.write("#4 P2500 S500 \r")
        time.sleep(4)
        self.out.write("#1 P1475 S250 \r")
        time.sleep(3)
        self.out.write("#3 P500 S250 \r")
        time.sleep(3)
        self.out.write("#0 P1675 S250 \r")
        time.sleep(3)
        self.out.write("#2 P1350 S250 \r")
        time.sleep(2)
        self.out.write("#0 P1300 S250 \r")
        time.sleep(3)
        self.out.write("#1 P1295 S250 \r")
        time.sleep(2)
        self.out.write("#2 P1580 S250 \r")
        time.sleep(2)
        self.out.write("#4 P500 S250 \r")
        time.sleep(4)
        self.center()



#arm testing entry point
#a = Arm()
#time.sleep(5)
#a.open()
#time.sleep(3)
#a.empty_basket()
#time.sleep(3)
#a.load_basket()
#time.sleep(3)
#a.close()
