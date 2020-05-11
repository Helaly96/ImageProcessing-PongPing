import numpy as np
import cv2
import math


def find_length(diff_x, diff_y):
    return math.sqrt(diff_y ** 2 + diff_x ** 2)


def contours_center(c):
    if c is not None:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return -1, -1


def find_nearest_contour(point, contours, trajectories):
    min = 100000
    index = 0
    correct_index = 0

    best_fit = ()
    # comparing to each contour point
    i = 0
    for c in contours:
        for p in c:
            x, y = p.ravel()
            diff_x = x - point[0]
            diff_y = y - point[1]
            dist = find_length(diff_x, diff_y)
            if dist < min:
                i = index
                min = dist
                best_fit = (x, y)
        index += 1

    diff_x = best_fit[0] - point[0]
    diff_y = best_fit[1] - point[1]
    dist = find_length(diff_x, diff_y)

    # the point we predicted is off
    if dist > 400:
        return point, contours[i]
        # predict
        # last_direction = tuple(map(sub, trajectories[-1], trajectories[-2]))
        # last_direction = tuple(map(floordiv, last_direction, (2, 2)))
        # best_fit = tuple(map(add, point, last_direction))
    return best_fit, contours[i]


def draw_on_screen(frame, pts0, pts1, pts2):
    # Draw boundaries
    cv2.polylines(frame, [pts0], True, (255, 255, 255))
    cv2.polylines(frame, [pts1], True, (255, 255, 255))
    cv2.polylines(frame, [pts2], True, (0, 255, 0))


def get_ball_coordinates(frame, previous, trajectories, points):
    # Parameters for the difference
    sensitivityValue = 60

    # Convert to grayscale
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcuate the difference between current and last frame
    differenceImage = cv2.subtract(grayImage, previous)
    # cv2.imshow('gray', grayImage)
    # cv2.imshow('pre', previous)
    # cv2.imshow('diff', differenceImage)

    # Cycle the
    previous = grayImage.copy()

    # Blur the difference to remove noise
    blur = cv2.GaussianBlur(differenceImage, (5, 5), cv2.BORDER_DEFAULT)

    # Threshold the blured frame
    _, thresholdImage = cv2.threshold(blur, sensitivityValue, 255, cv2.THRESH_BINARY)

    # Openning on the frame
    structuringElementSize = (7, 7)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, structuringElementSize)
    finalThresholdImage = cv2.morphologyEx(thresholdImage, cv2.MORPH_OPEN, structuringElement)

    # Blur the opened frame
    finalThresholdImage = cv2.GaussianBlur(finalThresholdImage, (5, 5), cv2.BORDER_DEFAULT)

    # Contour Detection
    # Contour Parameters
    perimeterMin = 25
    perimeterMax = 125

    # instead of getting a tree of contours (ie, each contour contain a child)
    # contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # we can get only top levels contours
    contours, hierarchy = cv2.findContours(finalThresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Select contours with specific arc length
    real_cnts = []

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeterMin < perimeter < perimeterMax:
            real_cnts.append(cnt)

    ''' --------------------/ Trajectory /------------------ '''

    # The ball is detected
    if len(real_cnts) > 0:
        # Get center of first contour
        center_x, center_y = contours_center(real_cnts[0])

        # Append it to the trajectories
        trajectories.append((center_x, center_y))

        # Skip first 15 frames
        if len(trajectories) > 15:
            # Calculate the distance between current point and last point
            diff_x = trajectories[-1][0] - trajectories[-2][0]
            diff_y = trajectories[-1][1] - trajectories[-2][1]
            dist = find_length(diff_y, diff_x)

            # The current point is very far
            if dist > 60:
                # Remove it from the trajectories
                trajectories.pop()

                # Get the nearest contour
                corrected_point, best_contour = find_nearest_contour(trajectories[-1], real_cnts, trajectories)

                # Append the correct contour to the trajectories
                trajectories.append(corrected_point)

            return trajectories[-1], previous
        else:
            return None, previous

    # No contours are found in the current frame
    else:
        return None, previous
