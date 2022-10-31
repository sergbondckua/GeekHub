"""
Програма-світлофор.
"""
from time import sleep


def traffic_lights(red_time=3, green_time=3):
    """Traffic lights emulator"""
    switchover = dict(Red="Green", Yellow="Red", Green="Red")

    red = ["Red" for _ in range(red_time)]
    yellow = ["Yellow" for _ in range(2)]
    green = ["Green" for _ in range(green_time)]

    while True:
        for color in red + yellow + green:
            print(color, switchover[color].rjust(10))
            sleep(1)


traffic_lights()
