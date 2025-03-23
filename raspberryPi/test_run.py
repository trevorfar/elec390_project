from picarx import Picarx
import time

def slow_forward(speed=10, duration=2):
    """Move the PiCar-X forward at a slow speed."""
    px = Picarx()  # Initialize the PiCar-X
    
    # Set left and right motors to move forward at low speed
    px.set_motor_speed(1, speed)
    px.set_motor_speed(2, speed)

    time.sleep(duration)  # Move for the given duration
    
    px.stop()  # Stop the car

slow_forward(speed=0.5, duration=3)