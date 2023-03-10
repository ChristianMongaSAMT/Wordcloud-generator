from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.properties import StringProperty
import logging
import kivy
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from pathlib import Path
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import _default_font_paths
from kivy.graphics import *
from kivy.uix.recycleview import RecycleView
import cv2
import numpy as np
import math
from kivy.config import Config

imageWidth = 0
img = 0
BORDI = -1
GERARCHIA = -2

class ConterGUI(BoxLayout):
    pass 
    def on_touch_down(self, touch):
        path = './pictures/provaEdo.png'
        img = cv2.imread(path)
        x = math.trunc(touch.pos[0])
        
        y = math.trunc(touch.pos[1])

        screenDim = self.ids.image.size
        self.imageDim = self.ids.image.norm_image_size

        

        if(y > screenDim[1]/2):
            d = y - screenDim[1]/2
            y = screenDim[1]/2 - d
        else:
            d = screenDim[1]/2 - y
            y = screenDim[1]/2 + d
        
        print("pos", touch.pos)
        print("img", self.imageDim)
        print("dim", screenDim, "\n")
        
        pxY = int(y-(screenDim[1] - self.imageDim[1])/2)
        pxX = int(x-(screenDim[0] - self.imageDim[0])/2)
        print("X --> ", pxX)
        #print(BORDI)
        if(self.isInArea(pxX,pxY)):
            
            print("cpos",pxX, pxY, "????????????????????")
            img[pxX,pxY] = [255,255,0]
            x = pxX - 5
            y = pxY - 5
            """while(x < pxX + 5):
                while(y < pxY + 5):
                    if(self.isInArea(y,x, imageDim)):
                        img[y, x] = [255,255,0]
                    y+=1                
                x += 1
                y = pxY - 5"""
            print("Pura curiosità ", BORDI[4][1][0][1]) #[bordo][pixel][0--> evitare il valore strano][coordinata]
            #print("atisoiruc aruP ", "\n",GERARCHIA)
            self.highlightArea(img, pxX, pxY)
            #path = "./pictures/provaEdo.png"
            cv2.imwrite(path, img)
            self.ids.image.source = path
            self.ids.image.reload()

    def highlightArea(self, img, x, y):
        if(self.isInArea(x, y)):
            popList = []
            img[y, x] = [0,255,0]
            if(self.isInArea(x + 1,y)):
                pixel = [x + 1, y, False]
                popList.append(pixel)
            if(self.isInArea(x - 1,y)):
                pixel = [x - 1, y, False]
                popList.append(pixel)
            if(self.isInArea(x,y + 1)):
                pixel = [x, y + 1, False]
                popList.append(pixel)
            if(self.isInArea(x,y - 1)):
                pixel = [x, y - 1, False]
                popList.append(pixel) 
            while(False in popList):
                if(self.isInArea(x + 1,y)):
                    pixel = [x + 1, y, False]
                    popList.append(pixel)
                if(self.isInArea(x - 1,y)):
                    pixel = [x - 1, y, False]
                    popList.append(pixel)
                if(self.isInArea(x,y + 1)):
                    pixel = [x, y + 1, False]
                    popList.append(pixel)
                if(self.isInArea(x,y - 1)):
                    pixel = [x, y - 1, False]
                    popList.append(pixel) 

        """if(self.isInArea(x,y) and  not self.isHighlightedPixel(x,y, img)):
            img[y, x] = [0,255,0]
            if(self.isInArea(x + 1,y)):
                self.highlightArea(img, x + 1, y)
            if(self.isInArea(x - 1,y)):
                self.highlightArea(img, x - 1, y)
            if(self.isInArea(x,y + 1)):
                self.highlightArea(img, x, y + 1)
            if(self.isInArea(x,y - 1)):
                self.highlightArea(img, x, y - 1)

            if(self.isInBorder(x + 1, y)):
                self.highlightArea(img, x + 1, y, imageDim)
            if(self.isInBorder(x - 1, y)):
                self.highlightArea(img, x - 1, y, imageDim)
            if(self.isInBorder(x, y + 1)):
                self.highlightArea(img, x, y + 1, imageDim)
            if(self.isInBorder(x, y - 1)):
                self.highlightArea(img, x, y - 1, imageDim)"""

    def popNewPixels(self, x, y):
        if(self.isInArea(x + 1,y)):
            pixel = [x + 1, y]
            popList.append(pixel)
            popCheckList.append(False)
        if(self.isInArea(x - 1,y)):
            pixel = [x - 1, y]
            popList.append(pixel)
            popCheckList.append(False)
        if(self.isInArea(x,y + 1)):
            pixel = [x, y + 1]
            popList.append(pixel)
            popCheckList.append(False)
        if(self.isInArea(x,y - 1)):
            pixel = [x, y - 1]
            popList.append(pixel) 
            popCheckList.append(False)
    def isHighlightedPixel(self, x, y, img):
        test = np.array([0,255,0])
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == test[key])):
                    isEqual = False
        return isEqual

    def isInBorder(self, x, y):
        #[bordo][pixel][0--> evitare il valore strano][coordinata]
        for bordo in BORDI:
            for pixel in bordo:
                if(pixel[0][0] == x  and pixel[0][1] == y):
                    return False
        return True

    def isInArea(self, x, y):
        #print(x > 0, "x > 0")
        #print(y > 0, "y > 0")
        #print(x < imageDim[0], "x < 500 | x = ", x)
        #print(y < imageDim[1], "y < 500", "\n")
        if(x > 0 and y > 0 and x < self.imageDim[0] and y < self.imageDim[1]):
            print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: True')
            return True
        print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: False')
        return False
        
class ConterApp(App):
    path = './pictures/cerchio.png'
    def build(self):            
        self.build_image()
        self.gui = ConterGUI()
        return self.gui

    def build_image(self):
        global BORDI
        global GERARCHIA
        img = cv2.imread(self.path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,150,255,0)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours in image:",len(contours))
        BORDI = contours
        GERARCHIA = hierarchy
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 3)

            if(area > 1000):
                #print('Area:', area)
                #print('Perimeter:', perimeter)
                bordo = cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
                #self.gui.setBorder("ok")
                x1, y1 = cnt[0,0]

        #cv2.imshow("Image", img)
        
        #self.path = "./pictures/cerchio.png"
        pathTempImage = "./pictures/provaEdo.png"
        cv2.imwrite(pathTempImage, img)
        #self.root.ids.image.source = pathTempImage
        #self.root.ids.image.reload()

    #def on_touch_down(self, touch):
    #    print("Mouse Down", touch)
    
    

if __name__ == '__main__':
    ConterApp().run()
    
    