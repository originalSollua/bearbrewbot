#The Bear Brew Bot. 
# A tweeting coffee brewing solution
# by Edward Pryor
# using Tweepy twitter API wrapper for python.
import time
import os
import RPi.GPIO as GPIO
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import arm
#this class controls handling the incoming text
# on_status will parse the tweet
#call the apropriate functions if deemed good

class StdOutListener(StreamListener):
    def on_status(self, status):
        print(status.text)
        print(str(mainBot.readytoBrew))
        self.parse(status.text)
    def on_error(self, status_code):
        GPIO.output(brewBot.pin_ready, GPIO.LOW)
        GPIO.output(brewBot.pin_red, GPIO.HIGH)
        print("got error with code"+str(status_code))
        return
    def on_timeout(self):
        print("timeout....")
        return True

    def makeCoffee(self):
        print "chicken"
        if(mainBot.readytoBrew):
            brewBot.readytoBrew = False
            
            #call to arms haha
         
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_green, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.LOW)
            GPIO.output(brewBot.pin_blue, GPIO.HIGH)
            GPIO.output(brewBot.pin_coffee, GPIO.LOW)
            #coffee is brewing, wait till done
            time.sleep(800)
            #leaves the pot running for 6 minutes
            GPIO.output(brewBot.pin_coffee, GPIO.HIGH)
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.HIGH)
            mainBot.brewDone()
        else:
            mainBot.isBusy()
        return

    def parse(self, statusText):
        red = 0
        blue = 0
        green = 0
        quit = 0
        brew = 0
        red = statusText.count("red")
        blue = statusText.count("blue")
        green = statusText.count("green")
        quit = statusText.count("quit")
        brew = statusText.count("start")
        if brew >= 1:
            self.makeCoffee()
            return True
        if red >= 1 and green == 0 and blue == 0:
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_green, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.HIGH)
            return True
        elif blue >= 1 and green == 0 and red == 0:
            GPIO.output(brewBot.pin_blue, GPIO.HIGH)
            GPIO.output(brewBot.pin_green, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.LOW)
            return True
        elif green >= 1 and red ==0 and blue == 0:
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_green, GPIO.HIGH)
            GPIO.output(brewBot.pin_red, GPIO.LOW)
            return True
        elif quit >= 1:
            self.running = False
            os.system("sudo shutdown -h now")
            return False
        else:
            print("too many choices")
            return True
#end stream listener
#now define the initialization
# set up the gpio
# read in the four tokens
# authenticate
# once all that done, turn on led #6

class brewBot:
    tokenBuffer  = []
    readytoBrew = True
    pin_ready = 6
    pin_red = 25
    pin_green = 24
    pin_blue = 26
    pin_coffee = 23
    def __init__(self):

        self.a = arm.Arm()
        with open("/home/pi/project/token") as f:
            for line in f:
                self.tokenBuffer.append(line.strip())
        print('Tokens got')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_ready, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_red, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_blue, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_green, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_blue, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_coffee, GPIO.OUT, initial=GPIO.HIGH);
        print("Pins Set")
        self.auth = tweepy.OAuthHandler(self.tokenBuffer[0], self.tokenBuffer[1])
        self.auth.secure = True
        self.auth.set_access_token(self.tokenBuffer[2], self.tokenBuffer[3])
        self.api = tweepy.API(self.auth)
        print(self.api.me().name)
        #set up stream
        
        folList = self.api.followers()
        self.usrString = str(folList[0].id)
        print("ledTest")
        GPIO.output(self.pin_ready, GPIO.HIGH)

    def streamStart(self):
        listener = StdOutListener()
        stream = Stream(self.auth, listener)
        print "stream built"
        stream.filter(follow=[self.usrString], track=['potsdamCoffee'])
        #end constructor

    #other fucntion defs at this level
    def brewDone(self):
        f = open("/home/pi/project/ticket", r)
        self.r = int(f.readline())
        f.close()
        self.api.update_status(status="Coffee's done!"+str(self.r))
        self.r = self.r+1;
        f = open("/home/pi/project/ticket", w)
        f.write(self.r)

    def isBusy(self):
        self.api.update_status(status="Busy...")

#code entry point
mainBot = brewBot()
mainBot.streamStart()
time.sleep(20)
print("Shutting down")

GPIO.cleanup(6)
GPIO.cleanup(24)
GPIO.cleanup(25)
GPIO.cleanup(26)
GPIO.cleanup(23)
