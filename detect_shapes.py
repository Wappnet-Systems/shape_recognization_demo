# import the necessary packages
import argparse

import cv2
import imutils

from pyimagesearch.shapedetector import ShapeDetector

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the threshold image and initialize the
# shape detector
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
sd = ShapeDetector()

# loop over the contours
for contour in contours:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(contour)
    contour_X = int((M["m10"] / M["m00"]) * ratio)
    contour_Y = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(contour)

    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    contour = contour.astype("float")
    contour *= ratio
    contour = contour.astype("int")
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (contour_X, contour_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
