#The Bear Brew Bot. 
# A tweeting coffee brewing solution
# by Edward Pryor
# using Tweepy twitter API wrapper for python.

import time
import os
import RPi.GPIO as GPIO
#import tweepy
#from tweepy.streaming import StreamListener
#from tweepy import Stream
import socket
import arm


# parse reads the tweet
# this is a simple parse
# counts the occurence of key words in the tweet
# start = start brewing
# red, green, blue = change status collor light
# quit = shut down the pi. sloppy


# brew bot class
# primary action is to construct the stream listener
# authenticate the application
# respond to the tweet, using ticket file to make each tweet unique

class brewBot:
    readytoBrew = True
    pin_ready = 6
    pin_red = 25
    pin_green = 24
    pin_blue = 26
    pin_coffee = 23
    def __init__(self):

        self.a = arm.Arm()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_ready, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_red, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_blue, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_green, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_blue, GPIO.OUT, initial=GPIO.LOW);
        GPIO.setup(self.pin_coffee, GPIO.OUT, initial=GPIO.HIGH);
        print("Pins Set")

        #set up socket. this is erver code
        self.brewSocket = socket.socket()
        host = socket.gethostname()
        port = 8945
        self.brewSocket.bind((host, port))
        
        print("ledTest")
        GPIO.output(self.pin_ready, GPIO.HIGH)
        GPIO.output(brewBot.pin_green, GPIO.HIGH)


    #other fucntion defs at this level
    def brewDone(self):
        f = open("/home/pi/project/ticket", 'r')
        self.r = int(f.readline())
        f.close()
        self.r = self.r+1;
        f = open("/home/pi/project/ticket", 'w')
        f.write(str(self.r))
        self.readytoBrew = True
        GPIO.output(self.pin_green, GPIO.HIGH)
    def isBusy(self):
        print "coffee pot not ready"
        # add something here to send messages along the main socket


    # makeCoffee
    # this method controls the making of coffee
    # called when parse returns that the tweet contained the start sequence
    # first, make the arm run through its sequence
    # then run the brew.
    
    def makeCoffee(self):
        if(self.readytoBrew):
            self.readytoBrew = False
            GPIO.output(brewBot.pin_green, GPIO.LOW)
            GPIO.output(brewBot.pin_blue, GPIO.HIGH)
            
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
            GPIO.output(brewBot.pin_blue, GPIO.LOW)
            GPIO.output(brewBot.pin_red, GPIO.HIGH)
            GPIO.output(brewBot.pin_coffee, GPIO.LOW)
            #coffee is brewing, wait till done
            print "brew start"
            time.sleep(800)
            print "brew done"
            #leaves the pot running for 6 minutes
            GPIO.output(brewBot.pin_coffee, GPIO.HIGH)
            GPIO.output(brewBot.pin_red, GPIO.LOW)
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
            return False
        else:
            print("too many choices")
            self.client.send("error:01:bad_command")
            return True 

#end stream listener
#now define the initialization
# set up the gpio
# read in the four tokens
# authenticate
# once all that done, turn on led #6

#code entry point
mainBot = brewBot()
running = True
while(running):
    self.client = mainBot.brewSocket.accept()
    self.client.send("connected")
    # next up, expect a request for something
    # the argument for recieve is the buffer size
    s = mainBot.brewSocket.recv(1024)
    running = mainBot.parse(s)
    self.client.send("finished")
    self.client.close()
print("coffee bot shutting down")
GPIO.cleanup(6)
GPIO.cleanup(24)
GPIO.cleanup(25)
GPIO.cleanup(26)
GPIO.cleanup(23)
os.system("sudo shutdown -h now")
