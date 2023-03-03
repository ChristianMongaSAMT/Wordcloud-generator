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
BORDO = 10

class ConterGUI(BoxLayout):
    pass 
    def on_touch_down(self, touch):
        path = './pictures/provaEdo.png'
        img = cv2.imread(path)
        x = math.trunc(touch.pos[0])
        
        y = math.trunc(touch.pos[1])

        screenDim = self.ids.image.size
        imageDim = self.ids.image.norm_image_size

        

        if(y > screenDim[1]/2):
            d = y - screenDim[1]/2
            y = screenDim[1]/2 - d
        else:
            d = screenDim[1]/2 - y
            y = screenDim[1]/2 + d
        
        print("pos", touch.pos)
        print("img", imageDim)
        print("dim", screenDim, "\n")
        
        pxY = int(y-(screenDim[1] - imageDim[1])/2)
        pxX = int(x-(screenDim[0] - imageDim[0])/2)
        print("X --> ", pxX)
        #print(BORDO)
        if(self.isInArea(pxX,pxY,imageDim)):
            
            print("cpos",pxX, pxY, "????????????????????")
            img[pxX,pxY] = [255,255,0]
            x = pxX - 5
            y = pxY - 5
            while(x < pxX + 5):
                while(y < pxY + 5):
                    img[y, x] = [255,255,0]
                    y+=1                
                x += 1
                y = pxY - 5
            print("Pura curiosità ", BORDO[4][1][0][1])
            #self.highlightArea(img, pxX, pxY, imageDim)
            #path = "./pictures/provaEdo.png"
            cv2.imwrite(path, img)
            self.ids.image.source = path
            self.ids.image.reload()

    def highlightArea(self, img, x, y, imageDim):
        
        if(self.isInArea(x,y,imageDim)):
            img[y, x] = [255,255,0]
            if(self.isInBorder(x + 1, y)):
                self.highlightArea(img, x + 1, y, imageDim)
            if(self.isInBorder(x - 1, y)):
                self.highlightArea(img, x - 1, y, imageDim)
            if(self.isInBorder(x, y + 1)):
                self.highlightArea(img, x, y + 1, imageDim)
            if(self.isInBorder(x, y - 1)):
                self.highlightArea(img, x, y - 1, imageDim)
        
        """while(x < 10):
            while(y < 10):
                img[y, x] = [255,255,0]
                y+=1                
            x += 1
            y = 0"""
    
    def isInBorder(self, x, y):
        for bor in BORDO:
            for cell in b:
                if(BORDO[bor][cell][0] == x and BORDO[i, j, 1] == y):
                    return False
        return True

    def isInArea(self, x, y, imageDim):
        #print(x > 0, "x > 0")
        #print(y > 0, "y > 0")
        #print(x < imageDim[0], "x < 500 | x = ", x)
        #print(y < imageDim[1], "y < 500", "\n")
        if(x > 0 and y > 0 and x < imageDim[0] and y < imageDim[1]):
            return True
        return False
        
class ConterApp(App):
    path = './pictures/cerchio.png'
    def build(self):            
        self.build_image()
        self.gui = ConterGUI()
        return self.gui

    def build_image(self):
        global BORDO
        img = cv2.imread(self.path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,150,255,0)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours in image:",len(contours))
        BORDO = contours
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
    
    