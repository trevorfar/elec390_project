from robot_hat import Pin
import time

rightPin = Pin('D1')
leftPin = Pin('D0')
#val = pin.value
# rightPin.value(0)
# leftPin.value(0)
# 
# 
# rightPin.value(1)
# leftPin.value(1)
# time.sleep(1)
# 
# leftPin.value(0)
# 
# rightPin.value(0)
# time.sleep(0.1)
# rightPin.value(1)
# time.sleep(0.1)
# rightPin.value(0)
# time.sleep(0.1)
# rightPin.value(1)
# time.sleep(0.1)
# rightPin.value(0)
# 
# leftPin.value(1)
# time.sleep(0.1)
# leftPin.value(0)
# time.sleep(0.1)
# leftPin.value(1)
# time.sleep(0.1)
# leftPin.value(0)
# 

def turnSignal(direction, num):
    for i in range(num):
        direction.value(1)
        time.sleep(0.1)
        direction.value(0)
        time.sleep(0.1)
        
turnSignal(leftPin, 4)

 #pin = Pin('D0')
#val = pin.value
# pin.value(1)
# time.sleep(0.1)
# pin.value(0)
# time.sleep(0.1)
# pin.value(1)
# time.sleep(0.1)
# pin.value(0)

#def turn_signal(direction):
    #