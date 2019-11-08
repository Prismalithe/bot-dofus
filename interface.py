import pyautogui
import time
from lecture import lecture
import numpy as np
import keyboard
import matplotlib.pyplot as plt

POSITION_ITEM_FIRST = [283, 204]

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

print(screenWidth, screenHeight)
print(currentMouseX, currentMouseY)


# Fonction d'achat avec l'item déjà sélectionné
def achat(prix):
    if prix == 1:
        position_prix = POSITION_P1
    elif prix == 2:
        position_prix = POSITION_P10
    elif prix == 3:
        position_prix = POSITION_P100
    pyautogui.moveTo(position_prix)
    # time.sleep(1)
    pyautogui.click()
    # time.sleep(1)
    pyautogui.moveTo(POSITION_ACHAT)
    # time.sleep(1)
    pyautogui.click()
    # time.sleep(1)
    pyautogui.moveTo(POSITION_CONFIRM_YES)
    # time.sleep(1)
    pyautogui.click()


def is_item(positionX, positionY):
    pix = pyautogui.pixel(positionX, positionY)
    if pix == (180, 172, 141) or pix == (201, 191, 157):
        return [False, [positionX, positionY]]
    elif pix == (147, 134, 108):
        if pyautogui.pixel(587, 487) == (81, 74, 60):
            pyautogui.moveTo(283, 480)
            pyautogui.scroll(-500)
            NewPositionX = 535
            NewPositionY = 484
            if pyautogui.pixel(NewPositionX, NewPositionY) == (255, 153, 17):
                return [False, [284, NewPositionY]]
            while pyautogui.pixel(NewPositionX, NewPositionY) != (255, 153, 17):
                if NewPositionY > 220:
                    NewPositionY -= 25
                else:
                    break
                print(NewPositionX, NewPositionY)
            return [True, [284, NewPositionY]]
        else:
            return [False, [positionX, positionY]]
    else:
        return [True, [positionX, positionY + 25]]


def full():
    data = []
    position = POSITION_ITEM_FIRST
    pyautogui.moveTo(position)
    pyautogui.click()
    time.sleep(1)
    item = is_item(position[0], position[1])
    while item[0]:
        position = item[1]
        pyautogui.moveTo(position)
        pyautogui.click()
        prix = lecture()
        print([prix[0], prix[1], prix[2], time.time()])
        data.append([prix[0], prix[1], prix[2], time.time()])
        item = is_item(position[0], position[1])
    return len(data), data


count = 0
while True:
    if keyboard.is_pressed("q"):
        break
    number_item, data = full()
    pyautogui.scroll(100000)
    count += 1
    data.append(["end_line", number_item, count, "hey"])
    nb_item = data[-1][1]
    with open('hdv5.data', 'ab') as f2:
        np.savetxt(f2, data, fmt='%s')
    for i in range(nb_item):
        if not data[i][0] == None:
            plt.plot(data[i][3], data[i][0], 'xb-')
        if not data[i][1] == None:
            plt.plot(data[i][3], data[i][1], 'xr-')
        if not data[i][2] == None:
            plt.plot(data[i][3], data[i][2], 'xg-')
        plt.draw()
        plt.pause(0.1)

plt.show()
