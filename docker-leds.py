#encoding:utf-8
import docker
import json
import time
import random
from neopixel import *

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

docker_client = docker.from_env()
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()
strip.show()
led = [None for _ in range(32)]

print("Starting program")
print("Listenning for events")

for event in docker_client.events():
    
    docker_event = json.loads(event)

    if "status" in docker_event:

        # creating
        if docker_event['status']=='create':
            print("creating %s", docker_event['id'])
            for i in range(0,len(led)):
                if led[i] == None:
                    led[i] = docker_event['id']
                    strip.setPixelColor(i, Color(255,255,0)) # yellow
                    strip.show()
                    break

        # starting
        if docker_event['status']=='start': 
            print("startig %s", docker_event['id'])
            for i in range(0,len(led)):
                if led[i] == docker_event['id']:
                    strip.setPixelColor(i, Color(255,255,255)) # white
                    strip.show()
                    break
        
        # dying
        if docker_event['status']=='die': 
            print("dying %s", docker_event['id'])
            for i in range(0,len(led)):
                if led[i] == docker_event['id']:
                    strip.setPixelColor(i, Color(255,0,0)) # red
                    strip.show()
                    break
        
        # killing
        if docker_event['status']=='kill': 
            print("killing %s", docker_event['id'])
            for i in range(0,len(led)):
                if led[i] == docker_event['id']:
                    strip.setPixelColor(i, Color(255,0,0)) # red
                    strip.show()
                    break
            
        # destroyed
        if docker_event['status']=='destroy': 
            print("destroying %s", docker_event['id'])
            for i in range(0,len(led)):
                if led[i] == docker_event['id']:
                    led[i] = None
                    strip.setPixelColor(i, Color(0,0,0)) # off
                    strip.show()
                    break



# while 1:
#     qtde = len(docker_client.containers.list())
#     print (qtde)
#     for i in range(0,qtde):
#         strip.setPixelColor(i, Color(255,255,255))
#         strip.show()