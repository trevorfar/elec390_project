from robot_hat import Pin
import time

pin = Pin('D0')
#val = pin.value
pin.value(0)


 #pin = Pin('D0')
#val = pin.value
pin.value(1)
time.sleep(1)
pin.value(0)
