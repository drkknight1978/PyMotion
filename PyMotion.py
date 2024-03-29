'''PyMotion v0.1 - Written by C.Mclaren UK.
   date 4th October 2019'''

from io import BytesIO
from time import sleep, time
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
def display (inArray, total, pic = 0, count = 9999999):
    yDim, xDim = inArray.shape
    displayArray = inArray.tolist()
    dStr = ''
    for i in range(yDim - 1):
        for j in range(xDim - 1):
            dStr = dStr + str(displayArray[i][j]).zfill(3)
        dStr = dStr + '\n'
    dStr = dStr + '---------- ' + str(total) + ' -------- snaps taken - ' + str (pic) + ' cycles = ' +str(count)
    return (dStr)

'''displays the image using text symbols'''
def displayImgTxt (inArray):
    yDim, xDim = inArray.shape
    displayArray = inArray.tolist()
    _ = system('clear')
    dStr = ''
    for i in range(yDim - 1):
        for j in range(xDim - 1):
            dStr = dStr + numConv(displayArray[i][j])
        dStr = dStr + '\n'
    return dStr


'''converts a number that is less than 255 to a text symbol - used
for displaying the camera image'''
def numConv(num):
    if num > 255:
        num = 255
    #symbols =['.', ',', ';', ':', '~', '!', '|', '/', '=','}', '+' ,'*', '#','@']
    symbols = [' ','.', ',', '-', '"', '^', ';', ':', '_', '/', '+', '=', '*', '#', '@']
    nSymbol = len (symbols)
    step = 256 / nSymbol
    index = int(num / step)
    return symbols[index]


#set-up camera and stream
stream = BytesIO()
camera = PiCamera()


threshold = 10 #Threshold of the number of pixels to be moving before taking a shot.
pixelTot = 0 #total difference in pixel brightness between images

#check image resolution and long term photo resolution.
xSmall = 48
ySmall = 32

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
tStart = time()

try:
    while True:
        '''Will keep taking a shot and compare with last shot, if there's movement above a threshold
        the camera will take a picture and record the time it happend.  Shot to be taken at a low 
        resolution and compared if there is movement take another higher resolution shot'''
        stream.seek (0) #ensure  that we start at the begining of the stream.
        camera.capture(stream, format='bmp',use_video_port=False , resize =(xSmall, ySmall))
        stream.seek (0)
        snapShot = Image.open(stream).convert('L')
        snapArr = np.array(snapShot)

        diffArr, moveAmt = motionLevel(snapShot, oldSnapshot, 25)
        imDiff = Image.fromarray (diffArr)
        print ('Front ' + str(datetime.now()) + ' >>>>> ' +str(pic))
        disp = display(diffArr, moveAmt, pic, cnt)
        disp = disp + '\n'+ 'Actual View ' + '\n' +  displayImgTxt(snapArr)
        _ = system ('clear')
        print (disp)
        if moveAmt > threshold:
            f = open('moves.csv','a+')
            camera.capture('img' + str(pic).zfill(7) +'>' + str(datetime.now()).replace(' ','+') + '.jpg')
            csv = str(datetime.now()) + ',' + str(time()-tStart) + ',' + '1\n'
            f.write(csv)
            f.close()
            pic += 1
        cnt += 1
        oldSnapshot = snapShot
        #sleep(0.1)
except KeyboardInterrupt:
    print ('')
    print('exited, camera closed.')
    camera.close()

