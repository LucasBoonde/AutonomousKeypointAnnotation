import cv2 as cv
import numpy as np
import math

def ParseCoordinates(line):
    keypointExstraction = line.strip().split()[1:]
    cx, cy, w, h = map(float,keypointExstraction[:4])
    keypoints = list(map(float, keypointExstraction[4:]))
    return cx, cy, w, h, keypoints


def Keypoints(imagePath, cx, cy, w, h, keypoints):
    image = cv.imread(imagePath)

    imageH, imageW, c = image.shape

    minX, minY = (int(imageW*(cx-(w/2))), int(imageH*(cy-(h/2))))
    maxX, maxY = (int(imageW*(cx+(w/2))), int(imageH*(cy+(h/2))))

    #Tegner BBOX
    cv.rectangle(image,(int(minX) ,int(minY) ), (int(maxX) ,int(maxY) ), (0,0,255), 3)

    #Tegner Alle Keypoints
    for i in range(0, len(keypoints), 2):
        kpX = int(keypoints[i] * imageW)
        kpY = int(keypoints[i+1]* imageH)
        cv.circle(image, (kpX, kpY), 10, (0,0,255), -1)
    
    cv.imshow("BBOX and Keypoints", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def main(filePath, imagePath):
    with open(filePath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            cx, cy, w, h, keypoints = ParseCoordinates(line)
            Keypoints(imagePath, cx, cy, w, h, keypoints)

if __name__ == "__main__":
    filePath ="data/labels/aircraft_0019.txt"
    imagePath ="data/images/aircraft_0019.jpg"
    main(filePath, imagePath)