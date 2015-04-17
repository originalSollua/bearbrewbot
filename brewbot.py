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
    # on_status
    # respond to recieving status
    # recieve message, pass it to parse

    def on_status(self, status):
        print(status.text)
        print(str(mainBot.readytoBrew))
        self.parse(status.text)

    # on_error
    # something broke
    # most common is the 420 error, stems from bad tokens
    # this seems to happen from rapid accesses to the api, 
    # also breaks around bad shut down of program

    def on_error(self, status_code):
        GPIO.output(brewBot.pin_ready, GPIO.LOW)
        GPIO.output(brewBot.pin_red, GPIO.HIGH)
        print("got error with code"+str(status_code))
        return
    # on_timeout
    def on_timeout(self):
        print("timeout....")
        return True
    
    # makeCoffee
    # this method controls the making of coffee
    # called when parse returns that the tweet contained the start sequence
    # first, make the arm run through its sequence
    # then run the brew.
    
    def makeCoffee(self):
        if(mainBot.readytoBrew):
            brewBot.readytoBrew = False
            
            #call to arms haha
            mainBot.a.open()
            time.sleep(4)
            mainBot.a.empty_basket()
            time.sleep(4)
            mainBot.a.load_basket()
            time.sleep(4)
            mainBot.a.close()
            time.sleep(4)
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_green, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.LOW)
            GPIO.output(brewBot.pin_blue, GPIO.HIGH)
            GPIO.output(brewBot.pin_coffee, GPIO.LOW)
            #coffee is brewing, wait till done
            print "brew start"
            time.sleep(800)
            print "brew done"
            #leaves the pot running for 6 minutes
            GPIO.output(brewBot.pin_coffee, GPIO.HIGH)
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.HIGH)
            mainBot.brewDone()
        else:
            mainBot.isBusy()
        return
# parse reads the tweet
# this is a simple parse
# counts the occurence of key words in the tweet
# start = start brewing
# red, green, blue = change status collor light
# quit = shut down the pi. sloppy

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

# brew bot class
# primary action is to construct the stream listener
# authenticate the application
# respond to the tweet, using ticket file to make each tweet unique

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
        f = open("/home/pi/project/ticket", 'r')
        self.r = int(f.readline())
        f.close()
        self.api.update_status(status="Coffee's done!"+str(self.r))
        self.r = self.r+1;
        f = open("/home/pi/project/ticket", 'w')
        f.write(str(self.r))
        self.readytoBrew = True

        GPIO.output(self.pin_red, GPIO.LOW)
        GPIO.output(self.pin_red, GPIO.HIGH)
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
