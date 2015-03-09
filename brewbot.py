#The Bear Brew Bot. 
# A tweeting coffee brewing solution
# by Edward Pryor
# using Tweepy twitter API wrapper for python.
import time
import RPi.GPIO as GPIO
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

#this class controls handling the incoming text
# on_status will parse the tweet
#call the apropriate functions if deemed good

class StdOutListener(StreamListener):
    def on_status(self, status):
        print("got status")
        self.parse(status.text)
    def on_error(self, status_code):
        print("got error with code"+str(status_code))
        return
    def on_timeout(self):
        print("timeout....")
        return True

    def parse(self, statusText):
        red = 0
        blue = 0
        green = 0
        quit = 0
        red = statusText.count("red")
        blue = statusText.count("blue")
        green = statusText.count("green")
        quit = statusText.count("quit")
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

    pin_ready = 6
    pin_red = 25
    pin_green = 24
    pin_blue = 26

    def __init__(self):

        with open("token") as f:
            for line in f:
                self.tokenBuffer.append(line.strip())
        print('Tokens got')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_ready, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_red, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_blue, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_green, GPIO.OUT, initial=GPIO.LOW);
        print("Pins Set")
        auth = tweepy.OAuthHandler(self.tokenBuffer[0], self.tokenBuffer[1])
        auth.secure = True
        auth.set_access_token(self.tokenBuffer[2], self.tokenBuffer[3])
        self.api = tweepy.API(auth)
        print(self.api.me().name)
        #set up stream
        
        folList = self.api.followers()
        usrString = str(folList[0].id)
        print("ledTest")
        GPIO.output(self.pin_ready, GPIO.HIGH)
        listener = StdOutListener()
        stream = Stream(auth, listener)
        stream.filter(follow=[usrString], track=['#brew'])
        #end constructor
    #other fucntion defs at this level

#code entry point
mainBot = brewBot()
time.sleep(20)
print("Shutting down")

GPIO.cleanup(6)
GPIO.cleanup(24)
GPIO.cleanup(25)
GPIO.cleanup(26)
