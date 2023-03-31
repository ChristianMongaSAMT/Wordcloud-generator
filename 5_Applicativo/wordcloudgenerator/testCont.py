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
import panel as pn
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import colorchooser
from kivy.lang import Builder

imageWidth = 0
img = 0
BORDI = -1
GERARCHIA = -2

Builder.load_string('''
<ConterGUI>:
    BoxLayout:
        size: self.size
        Image:
            id: image
            source: app.path
            size: self.size
''')

    
class ConterGUI(BoxLayout):
    pass
    def on_touch_down(self, touch):
        path = './pictures/provaEdo.png'
        img = cv2.imread(path)
        x = math.trunc(touch.pos[0])
        
        y = math.trunc(touch.pos[1])

        screenDim = self.ids.image.size
        self.imageDim = self.ids.image.norm_image_size
        self.popList = []

        if(y > screenDim[1]/2):
            d = y - screenDim[1]/2
            y = screenDim[1]/2 - d
        else:
            d = screenDim[1]/2 - y
            y = screenDim[1]/2 + d
        
        print("pos", touch.pos)
        print("img", self.imageDim)
        print("dim", screenDim)
        
        pxY = int(y-(screenDim[1] - self.imageDim[1])/2)
        pxX = int(x-(screenDim[0] - self.imageDim[0])/2)
        if(self.isInArea(pxX,pxY)):
            
            print("rpo",pxX, pxY, "\n")
            #img[pxX,pxY] = [255,255,0]
            x = pxX - 5
            y = pxY - 5
            """while(x < pxX + 5):
                while(y < pxY + 5):
                    if(self.isInArea(y,x, imageDim)):
                        img[y, x] = [255,255,0]
                    y+=1                
                x += 1
                y = pxY - 5"""
           
            #print("Pura curiosità ", BORDI[4][1][0][1]) #[bordo][pixel][0--> evitare il valore strano][coordinata]
            self.highlightArea(img, pxX, pxY)
            cv2.imwrite(path, img)
            self.ids.image.source = path
            self.ids.image.reload()

    def highlightArea(self, img, x, y):
        queue = []
        queue.append([x, y])
        # Color the pixel with the new color
        color = [0,255,0]
        img[y][x] = color

        while queue:
            
            currPixel = queue.pop()
            
            posX = currPixel[0]
            posY = currPixel[1]
            
            if(self.isInArea(posX + 1, posY) and not self.isHighlightedPixel(posX + 1, posY, img) and not self.isBorder(posX + 1, posY, img)):
                img[posY][posX + 1] = color
                queue.append([posX + 1, posY])

            if(self.isInArea(posX - 1, posY) and not self.isHighlightedPixel(posX - 1, posY, img) and not self.isBorder(posX - 1, posY, img)):
                img[posY][posX - 1] = color
                queue.append([posX - 1, posY])
            
            if(self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY + 1, img) and not self.isBorder(posX, posY + 1, img)):
                img[posY + 1][posX] = color
                queue.append([posX, posY + 1])
            
            if( self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY - 1, img) and not self.isBorder(posX, posY - 1, img)):
                img[posY - 1][posX] = color
                queue.append([posX, posY - 1])

    def isHighlightedPixel(self, x, y, img):
        test = np.array([0,255,0])
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == test[key])):
                    isEqual = False

        return isEqual

    def isBorder(self, x, y, img):
        test = np.array([0, 0, 150])
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == test[key])):
                    isEqual = False

        return isEqual

    def isInArea(self, x, y):
        if(x >= 0 and y >= 0 and x < self.imageDim[0] and y < self.imageDim[1]):
            #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: True')
            return True
        #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: False')
        return False

    
class ConterApp(App):
    path = './pictures/cerchio.png'
    def build(self):

        self.build_image()
        self.gui = ConterGUI()
        colorPicker = ColorPicker()
        self.gui.add_widget(colorPicker)
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
                bordo = cv2.drawContours(img, [cnt], -1, (0,0,150), 1)
                #self.gui.setBorder("ok")
                x1, y1 = cnt[0,0]

        #cv2.imshow("Image", img)
        
        #self.path = "./pictures/cerchio.png"
        pathTempImage = "./pictures/provaEdo.png"
        cv2.imwrite(pathTempImage, img)
        #self.root.ids.image.source = pathTempImage
        #self.root.ids.image.reload()
    
    

if __name__ == '__main__':
    ConterApp().run()
    
    