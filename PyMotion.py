'''PyMotion v0.1 - Written by C.Mclaren UK.
   date 4th October 2019'''

from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
import numpy as np
from os import system
from datetime import datetime

'''Differentiates the two images and the ensure that the image
has no negative numbers'''
def motionLevel(image1, image2, T = 0):
    arr1 = np.array (image1)
    arr2 = np.array (image2)
    arr3 = np.absolute (np.subtract(arr1, arr2, dtype = 'int8'))
    arr3 = (arr3 > T) * arr3
    return arr3, arr3.sum()

'''Displays the difference array on a screen,  more for debugging 
and testing'''
def display (inArray, total, pic = '0'):
    yDim, xDim = inArray.shape
    displayArray = inArray.tolist()
    _ = system('clear')
    for i in range(yDim - 1):
        for j in range(xDim - 1):
            print (displayArray[i][j], ' , ', end ='')
        print ('')
    print('---------- ', total, ' -------- snaps taken - ', pic)

'''displays the image using text symbols'''
def displayImgTxt (inArray):
    yDim, xDim = inArray.shape
    displayArray = inArray.tolist()
    _ = system('clear')
    for i in range(yDim - 1):
        for j in range(xDim - 1):
            print (numConv(displayArray[i][j]), end ='')
        print ('')


'''converts a number that is less than 255 to a text symbol - used
for displaying the camera image'''
def numConv(num):
    if num > 255:
        num = 255
    symbols =['.', ',', '-', '_', '~', '|', '/', '+' ,'*', '#','@']
    nSymbol = len (symbols)
    step = 256 / nSymbol
    index = int(num / step)
    return symbols[index]


#set-up camera and stream
stream = BytesIO()
camera = PiCamera()

#Number of seconds between camera shots
nSec = 1
#pixel value difference between images
threshold = 10
pixelTot = 0 #total differemonce in pixels between images

#check image resolution and long term photo resolution.
xSmall = 32
ySmall = 24

xBig = 2592
yBig = 1944

#warm up camera
camera.resolution = (xBig, yBig)
camera.start_preview()
sleep(2)
#capture and initial comparison image
camera.capture(stream, format='bmp',use_video_port=False  ,resize =(xSmall, ySmall))
oldSnapshot = Image.open(stream).convert('L')

pic = 0
cnt = 0

try:
    while True:
        '''Will take a shot every n seconds.  Shot to be taken at a low resolution and compared
        if there is movement take another higher resolution shot'''
        stream.seek (0) #ensure  that we start at the begining of the stream.
        camera.capture(stream, format='bmp',use_video_port=False , resize =(xSmall, ySmall))
        stream.seek (0)
        snapShot = Image.open(stream).convert('L')
        snapArr = np.array(snapShot)

        diffArr, moveAmt = motionLevel(snapShot, oldSnapshot, 25)
        imDiff = Image.fromarray (diffArr)

        #_ = display(diffArr, moveAmt, str(pic))
        _ = displayImgTxt(snapArr)
        if moveAmt > threshold:
            camera.capture(str(datetime.now()).replace(' ','+') + '.jpg')
            pic += 1
        cnt += 1
        oldSnapshot = snapShot
        sleep (0.1)
except KeyboardInterrupt:
    print ('')
    print('exited, camera closed.')
    camera.close()

