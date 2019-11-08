import cv2
import numpy as np
from PIL import ImageGrab


def process_img(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (2, 2))
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh


def lecture():

    # Les coordonnées à modifiés : ils doivent représenter la ligne d'achat des ressources
    screen = np.array(ImageGrab.grab(bbox=(650, 360, 980, 390)))

    #######   training part    ###############
    samples = np.loadtxt('generalsamples.data', np.float32)
    responses = np.loadtxt('generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    ############################# testing part  #########################

    out = np.zeros(screen.shape, np.uint8)
    thresh = process_img(screen)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    p1 = []
    p10 = []
    p100 = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 28 and cv2.contourArea(cnt) < 300:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 10 & h < 20:
                cv2.rectangle(screen, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi = thresh[y:y+h, x:x+w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(
                    roismall, k=1)
                string = str(int((results[0][0])))
                # print(int(results[0][0]), x, y, h, w)

                if x < 110 and x > 40:
                    p1.append([int(results[0][0]), x])
                elif x < 210 and x > 150:
                    p10.append([int(results[0][0]), x])
                elif x < 320 and x > 250:
                    p100.append([int(results[0][0]), x])

    sorted_p1 = sorted(p1, key=lambda x: x[1])
    sorted_p10 = sorted(p10, key=lambda x: x[1])
    sorted_p100 = sorted(p100, key=lambda x: x[1])

    # cv2.imshow('im', screen)
    # cv2.imshow('out', thresh)
    # cv2.waitKey(0)

    prix = [sorted_p1, sorted_p10, sorted_p100]

    prix_1 = ''
    prix_10 = ''
    prix_100 = ''

    # print(prix)

    for i, p in enumerate(prix):
        if i == 0:
            for unite in p:
                prix_1 += str(unite[0])
        if i == 1:
            for unite in p:
                prix_10 += str(unite[0])
        if i == 2:
            for unite in p:
                prix_100 += str(unite[0])

    prix_tot_str = [prix_1, prix_10, prix_100]

    prix_tot = []

    for p in prix_tot_str:
        if p == '':
            p = None
        else:
            p = int(p)
        prix_tot.append(p)

    return prix_tot


# lecture()
