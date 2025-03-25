from robot_hat import Pin
import time

forwardLights = Pin('D0')
stopLights = Pin('D1')
# leftTurn = Pin('P8')
# rightTurn = Pin('P9')
forwardLights.value(1)
time.sleep(1)
forwardLights.value(0)