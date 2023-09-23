import cv2
import numpy as np

# videocapture from 192.168.88.228 login admin password maser000

# cap = cv2.VideoCapture("rtsp://admin:master000@192.168.88.229:554")
cap = cv2.VideoCapture(0)


def find_buoy(img, lower, upper, label, iterations, quant, kernel_size=(9, 9)):
    """
    Find a circle in the image and draw contours with label if found.

    :param kernel_size:
    :param numpy.array lower: lower bound of color to search for (HSV).
    :param numpy.array upper: upper bound of color to search for (HSV).
    :param str label: label to draw near circle.
    :param int iterations: numbers of dilate
    :param int quant: quantity of objects
    :return int x: x-coords on frame
    """
    blur_img = cv2.GaussianBlur(img, (15, 15), 5)
    negative = np.array([255, 255, 255]) - (lower + upper) / 2
    hsv = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow('mask', mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    eroded = cv2.erode(mask, kernel)
    dilated = cv2.dilate(eroded, kernel, iterations=iterations)

    cv2.imshow('dilated', dilated)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (test_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contours = contours[:quant]
    contours_coordinates = []

    for contour in largest_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), negative, 2)
        cv2.putText(img, label, (int(x + (w - text_height * len(label)) / 2), int(y + h / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, negative, 2)
        contours_coordinates.append((x + w / 2, y + h / 2))

    #
    # if len(contours) > 0:
    #     c = max(contours, key=cv2.contourArea)
    #     for cnt in contours:
    #         if cv2.contourArea(cnt) > 100:
    #             x, y, w, h = cv2.boundingRect(c)
    #             cv2.rectangle(img, (x, y), (x + w, y + h), negative, 2)
    #             cv2.putText(img, label, (int(x + (w - text_height * len(label)) / 2), int(y + h / 2)),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1, negative, 2)
    # cv2.imshow('mask', mask)
    # cv2.imshow('dilated', dilated)
    cv2.imshow('frame', img)
    return contours_coordinates


def find_gates(img, lower, upper, label, iterations, kernel_size=(9, 9)):
    blur_img = cv2.GaussianBlur(img, (15, 15), 5)
    negative = np.array([255, 255, 255]) - (lower + upper) / 2
    hsv = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow('mask', mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    eroded = cv2.erode(mask, kernel)
    dilated = cv2.dilate(eroded, kernel, iterations=iterations)

    cv2.imshow('dilated', dilated)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (test_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contours = contours[:2]
    if len(largest_contours) == 2:
        x1, y1, w1, h1 = cv2.boundingRect(largest_contours[0])
        x2, y2, w2, h2 = cv2.boundingRect(largest_contours[1])
        xc1 = int(x1 + w1 / 2)
        xc2 = int(x2 + w2 / 2)
        yc1 = int(y1 + h1 / 2)
        yc2 = int(y2 + h2 / 2)
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), negative, 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), negative, 2)
        x = int((xc1 + xc2) / 2)
        y = int((yc1 + yc2) / 2)
        cv2.putText(img, label, (int(x - text_height * len(label) / 2), int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, negative, 2)
        cv2.line(img, (xc1, yc1), (xc2, yc2), negative, thickness=3)
        cv2.circle(img, (x, y), radius=3, color=(0, 0, 255), thickness=3)
        cv2.imshow('frame', img)
        return x, y
    cv2.imshow('frame', img)
    return None


def find_dock(img, lower, upper, label, iterations, kernel_size=(9, 9)):
    return find_buoy(img, lower, upper, label, iterations, 1, kernel_size)


# while True:
#     ret, frame = cap.read()
#     # coordinates = find_buoy(frame, np.array([5, 141, 101]), np.array([33, 215, 149]), "Warning", 4, 6)
#     # print(coordinates)
#     coordinates = find_gates(frame, np.array([5, 141, 101]), np.array([33, 215, 149]), "Gate", 4)
#     print(coordinates)
#
#     cv2.imshow('frame', frame)
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break
# cv2.destroyAllWindows()
