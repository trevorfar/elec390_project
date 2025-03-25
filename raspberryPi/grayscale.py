from picarx import Picarx
from speed import Speed

px = Picarx()
car = Speed(px)

def adjust_direction():
    """Adjust the car's direction based on grayscale sensor values."""
    sensor_values = px.get_grayscale_data()

    left_sensor = sensor_values[0]
    right_sensor = sensor_values[2]

    if left_sensor > 200:
        print("Left sensor detected high value! Turning right.")
        px.set_dir_servo_angle(30)  # Adjust the angle as needed
    elif right_sensor > 200:
        print("Right sensor detected high value! Turning left.")
        px.set_dir_servo_angle(-30)  # Adjust the angle as needed
    else:
        px.set_dir_servo_angle(0)

while True:
    car.set_speed(10)
    adjust_direction()
