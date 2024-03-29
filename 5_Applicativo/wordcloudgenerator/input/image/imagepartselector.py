import cv2
import math
import numpy as np

from input.image.borderproperties import getBorderColor
from input.image.borderproperties import getCountours
from input.image.imageselector import setIsResult
from generatecloud import generateCloud
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.logger import Logger

FLOAD_COLOR = (0,0,0)
DOWNLOAD = -1
BORDERWINDOW = 4
TEMP_PATH = "./pictures/imageMod.png"
MASK_PATH = "./pictures/.mask.png"
DELTA_PATH = "./pictures/.delta.png"

class ImageSelection(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageSelection, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        self.updateMask(touch)

    def highlightArea(self, img, imgDelta, mask, x, y):
        queue = []
        queue.append([x, y])
        # Color the pixel with the new color
        #color = [0,255,0]
        color = 0
        mask[y][x] = color

        while queue:
            currPixel = queue.pop()
            
            posX = currPixel[0]
            posY = currPixel[1]
            
            if(self.isInArea(posX + 1, posY) and not self.isHighlightedPixel(posX + 1, posY, mask) and not self.isBorder(posX + 1, posY, img)):
                mask[posY][posX + 1] = color
                imgDelta[posY][posX+1] = img[posY][posX+1]
                queue.append([posX + 1, posY])
            if(self.isInArea(posX - 1, posY) and not self.isHighlightedPixel(posX - 1, posY, mask) and not self.isBorder(posX - 1, posY, img)):
                mask[posY][posX - 1] = color
                imgDelta[posY][posX-1] = img[posY][posX-1]
                queue.append([posX - 1, posY])
            
            if(self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY + 1, mask) and not self.isBorder(posX, posY + 1, img)):
                mask[posY + 1][posX] = color
                imgDelta[posY+1][posX] = img[posY+1][posX]
                queue.append([posX, posY + 1])
            
            if( self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY - 1, mask) and not self.isBorder(posX, posY - 1, img)):
                mask[posY - 1][posX] = color
                imgDelta[posY-1][posX] = img[posY-1][posX]
                queue.append([posX, posY - 1])
            

    def isHighlightedPixel(self, x, y, img):
        color = 0
        return color == img[y][x]

    def isBorder(self, x, y, img):
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
    
                if(not (bgr == getBorderColor()[key])):
                    isEqual = False
        return isEqual

    def isInArea(self, x, y):
        if(x >= 0 and y >= 0 and x < self.imageDim[0] and y < self.imageDim[1]):
            return True
        return False


    def updateMask(self, touch):
    
        img = cv2.imread(TEMP_PATH)
        Logger.info(f'[imagepartselector.py] letta immagine da elaborare: {TEMP_PATH}')
        
        #dimensione immagine originale
        mask = np.ones((img.shape[0],img.shape[1],1), np.uint8)

        cv2.imwrite(MASK_PATH, mask, [cv2.IMWRITE_PNG_BILEVEL, 1])
        imgDelta = cv2.imread(MASK_PATH)

        
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
        x = x - (Window.size[0] - self.boxDim[0])/2 - BORDERWINDOW

        
        pxY = int(y-(self.boxDim[1] - self.imageDim[1])/2)
        pxX = int(x-(self.boxDim[0] - self.imageDim[0])/2)
        if(self.isInArea(pxX,pxY)):
            self.highlightArea(img, imgDelta, mask, pxX, pxY)
            cv2.imwrite(MASK_PATH, mask, [cv2.IMWRITE_PNG_BILEVEL, 1])
            cv2.imwrite(TEMP_PATH, img)
            cv2.imwrite(DELTA_PATH, imgDelta)
            generateCloud(img.shape)
            setIsResult(True)
            Logger.info(f'[imagepartselector.py] posizione valida :{pxX, pxY}')
        else:
            Logger.warning(f'[imagepartselector.py] posizione non valida:{pxX, pxY}')

        