from picarx import Picarx
#from speed import Speed
import time
px = Picarx()
#car = Speed(px)
aaaa
currState = 0

def move():
    px.set_motor_speed(1, 100)
    px.set_motor_speed(2, -100)
def checkStop():
    sensor_values = px.get_grayscale_data()
    currGray = sensor_values
    move()
    time.sleep(1)
    currState =0;
    if ((currGray[0]>200 and currGray[1]>200 and currGray[2]>200) and currState == 0):
            px.forward(0)
            print("stopped")
            time.sleep(3)
            currState = 1
def adjust_direction():
    """Adjust the car's direction based on grayscale sensor values."""
    sensor_values = px.get_grayscale_data()
    move()
    currState =0;
    left_sensor = sensor_values[0]
    right_sensor = sensor_values[2]
    
    if left_sensor > 200:
        print("Left sensor detected high value! Turning right.")
        px.set_dir_servo_angle(30)  
    elif right_sensor > 200:
        print("Right sensor detected high value! Turning left.")
        px.set_dir_servo_angle(-30)  
    
    else:
        px.set_dir_servo_angle(-2)
        
while True:
    move()
    checkStop()
    adjust_direction()
    
    


