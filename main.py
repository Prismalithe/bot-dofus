from interface import refresh
from lecture import lecture
import numpy as np
import time
import keyboard



def main():
    data = []
    while True:
        refresh()
        prix = lecture()
        print([prix[0], prix[1], prix[2], time.time()])
        data.append([prix[0], prix[1], prix[2], time.time()])
        if keyboard.is_pressed("q"):
            break

main()
