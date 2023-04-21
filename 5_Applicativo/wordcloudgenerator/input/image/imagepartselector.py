import cv2
import math
import numpy as np

from input.image.imageselector import getPath
from input.image.borderproperties import getCountours
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

BORDER_COLOR = (100,100,100)
FLOAD_COLOR = (0,0,0)
DOWNLOAD = -1
BORDERWINDOW = 4;
TEMP_PATH = "./pictures/imageMod.png"
MASK_PATH = "./pictures/.mask.png"

class ImageSelection(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageSelection, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        img = cv2.imread(TEMP_PATH)
        mask = cv2.imread(TEMP_PATH, cv2.IMREAD_UNCHANGED)
        countours = getCountours()
        #print(countours)

        ''' CONTROLLARE '''
        for cnt in countours:
            area = cv2.contourArea(cnt)
            if(area > 1000):
                cv2.drawContours(img, [cnt], -1, BORDER_COLOR, 1)

        x = math.trunc(touch.pos[0])

        y = math.trunc(touch.pos[1])
        self.boxDim = self.ids.image.size
        self.imageDim = self.ids.image.norm_image_size

        if(y > self.boxDim[1]/2):
            d = y - self.boxDim[1]/2
            y = self.boxDim[1]/2 - d
        else:
            d = self.boxDim[1]/2 - y
            y = self.boxDim[1]/2 + d
        print("window size", Window.size[0])
        print("Start", (Window.size[0] - self.boxDim[0])/2)
        x = x - (Window.size[0] - self.boxDim[0])/2 - BORDERWINDOW

        
        print("pos", touch.pos)
        print("img", self.imageDim)
        print("dim", self.boxDim)
        
        pxY = int(y-(self.boxDim[1] - self.imageDim[1])/2)
        pxX = int(x-(self.boxDim[0] - self.imageDim[0])/2)
        if(self.isInArea(pxX,pxY)):
            print("rpo",pxX, pxY, "\n")
            self.highlightArea(img, mask, pxX, pxY)
            cv2.imwrite(MASK_PATH, mask, [cv2.IMWRITE_PNG_BILEVEL, 1])
            cv2.imwrite(TEMP_PATH, img)
            self.ids.image.source = TEMP_PATH 
            self.ids.image.reload()

    def highlightArea(self, img, mask, x, y):
        queue = []
        queue.append([x, y])
        # Color the pixel with the new color
        #color = [0,255,0]
        color = 1
        mask[y][x] = color
        img[y][x] = FLOAD_COLOR

        while queue:
            currPixel = queue.pop()
            print(currPixel)
            
            posX = currPixel[0]
            posY = currPixel[1]
            if(self.isInArea(posX + 1, posY)):
                print("isInArea")
            """
            if(self.isInArea(posX + 1, posY) and not self.isHighlightedPixel(posX + 1, posY, mask) and not self.isBorder(posX + 1, posY, img)):
                mask[posY][posX + 1] = color
                img[posY][posX + 1] = FLOAD_COLOR
                queue.append([posX + 1, posY])
            if(self.isInArea(posX - 1, posY) and not self.isHighlightedPixel(posX - 1, posY, mask) and not self.isBorder(posX - 1, posY, img)):
                mask[posY][posX - 1] = color
                img[posY][posX - 1] = FLOAD_COLOR
                queue.append([posX - 1, posY])
            
            if(self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY + 1, mask) and not self.isBorder(posX, posY + 1, img)):
                mask[posY + 1][posX] = color
                img[posY + 1][posX] = FLOAD_COLOR
                queue.append([posX, posY + 1])
            
            if( self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY - 1, mask) and not self.isBorder(posX, posY - 1, img)):
                mask[posY - 1][posX] = color
                img[posY - 1][posX] = FLOAD_COLOR
                queue.append([posX, posY - 1])
            """

    def isHighlightedPixel(self, x, y, img):
        color = 1
        return color == img[y][x]

    def isBorder(self, x, y, img):
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == BORDER_COLOR[key])):
                    isEqual = False
        return isEqual

    def isInArea(self, x, y):
        '''if(x - (self.boxDim[0] - self.imageDim[0])/2 >= 0 and y - (self.boxDim[1] - self.imageDim[1])/2 >= 0 and x < self.imageDim[0] - (self.boxDim[0] - self.imageDim[0])/2 and y < self.imageDim[1] - (self.boxDim[1] - self.imageDim[1])/2):
            print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: True')
            return True
            #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: False')
        return False'''


        if(x >= 0 and y >= 0 and x < self.imageDim[0] and y < self.imageDim[1]):
            #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: True')
            return True
        #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: False')
        return False
    #def generateMask