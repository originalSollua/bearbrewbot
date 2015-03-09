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
        #parse status
        #based on parsing do stuff

        return True
    def on_error(self, status_code):
        print("got error with code"+str(status_code))

    def on_timeout(self):
        print("timeout....")
        return True

    #def parse


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
    pin_green = 26
    pin_blue = 24

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

        #listener = StdOutListener()
        #stream = Stream(auth, listener)
        #stream.filter(follow=[usrString], track=['#brew'])
        print("ledTest")
        GPIO.output(self.pin_ready, GPIO.HIGH)

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
