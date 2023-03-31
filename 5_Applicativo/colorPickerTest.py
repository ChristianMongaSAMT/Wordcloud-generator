import os
import cv2
import validators
import tkinter as tk
from tkinter import filedialog
import numpy as np

from urllib.request import urlopen
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.splitter import Splitter

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

from kivy.uix.colorpicker import ColorPicker
from PIL import Image
import getpass
import os.path

import math

BORDER_COLOR = (100,100,100)
DOWNLOAD = -1

Builder.load_string('''
<MongaGUI>:
    BoxLayout:
        
        canvas.before:
            Color:
                rgba: 1, 0, 0, 0.5
            Rectangle:
                size: self.size
                pos: self.pos
        size: self.size
        
        ImageBox:

<ImageSelection>:
    Image:
        id: image
        source: root.startPath
        size: self.size
        canvas.before:
            Color:
                rgba: 0, 1, 0, 0.5
            Rectangle:
                size: self.size
                pos: self.pos
<Download>:
    BoxLayout:
        padding: [50,50,50,50]
        Button:
            text:"Conferma"
            id: download_button
            on_release: app.download()        
        Spinner:
            size_hint: None, None
            size: 100, 44
            text: 'png'
            values:'png','jpg','webp'
            id: formatSpinner
            on_text:
                app.format_changed()           

''')

class ImageBox(BoxLayout):
    def __init__(self, **kwargs):
        global DOWNLOAD
        super(ImageBox, self).__init__(**kwargs)
        self.add_widget(ImageSelection())

        self.add_widget(Splitter())
        colorPicker = ColorPicker()
        colorPicker.bind(color=self.on_color)
        self.add_widget(colorPicker)
        DOWNLOAD = Download()
        self.add_widget(DOWNLOAD)

    def on_color(self, instance, value):
        global BORDER_COLOR
        #print("RGBA = ", str(value))  #  or instance.color
        #print("HSV = ", str(instance.hsv))
        #print("HEX = ", str(instance.hex_color))
        BORDER_COLOR = (int(value[2] * 255), int(value[1] * 255), int(value[0] * 255))

class Download(BoxLayout):
     def __init__(self, **kwargs):
        super(Download, self).__init__(**kwargs)


class ImageSelection(BoxLayout):
    startPath = './pictures/cerchio.png'
    contours = -1

    def __init__(self, **kwargs):
        super(ImageSelection, self).__init__(**kwargs)
        self.buildImage()
    
    def buildImage(self):
        img = cv2.imread(self.startPath)
        print(img.shape,"albatros")
        mask = np.zeros((img.shape[0],img.shape[1],1), np.uint8)

        cv2.imwrite("./pictures/provaEdoBN.png", mask, [cv2.IMWRITE_PNG_BILEVEL, 1])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,150,255,0)
        #countour[4][1][0][1]) #[bordo][pixel][0--> evitare il valore strano][coordinata]
        self.contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #BORDERS = contours
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 3)

            if(area > 1000):
                cv2.drawContours(img, [cnt], -1, BORDER_COLOR, 1)
                x1, y1 = cnt[0,0]
        pathTempImage = "./pictures/provaEdo.png"
        cv2.imwrite(pathTempImage, img)
    
    def on_touch_down(self, touch):
        path = './pictures/provaEdo.png'
        img = cv2.imread(path)
        mask = cv2.imread('./pictures/provaEdoBN.png', cv2.IMREAD_UNCHANGED)
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 3)

            if(area > 1000):
                cv2.drawContours(img, [cnt], -1, BORDER_COLOR, 1)
                x1, y1 = cnt[0,0]
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
            self.highlightArea(img, mask, pxX, pxY)
            cv2.imwrite('./pictures/provaEdoBN.png', mask, [cv2.IMWRITE_PNG_BILEVEL, 1])
            self.ids.image.source = path
            self.ids.image.reload()

    def highlightArea(self, img, mask, x, y):
        queue = []
        queue.append([x, y])
        # Color the pixel with the new color
        #color = [0,255,0]
        color = 1
        #color = BORDER_COLOR

        mask[y][x] = color

        while queue:
            
            currPixel = queue.pop()
            
            posX = currPixel[0]
            posY = currPixel[1]
            if(self.isInArea(posX + 1, posY) and not self.isHighlightedPixel(posX + 1, posY, mask) and not self.isBorder(posX + 1, posY, img)):
                mask[posY][posX + 1] = color
                queue.append([posX + 1, posY])

            if(self.isInArea(posX - 1, posY) and not self.isHighlightedPixel(posX - 1, posY, mask) and not self.isBorder(posX - 1, posY, img)):
                mask[posY][posX - 1] = color
                queue.append([posX - 1, posY])
            
            if(self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY + 1, mask) and not self.isBorder(posX, posY + 1, img)):
                mask[posY + 1][posX] = color
                queue.append([posX, posY + 1])
            
            if( self.isInArea(posX, posY + 1) and not self.isHighlightedPixel(posX, posY - 1, mask) and not self.isBorder(posX, posY - 1, img)):
                mask[posY - 1][posX] = color
                queue.append([posX, posY - 1])

    def isHighlightedPixel(self, x, y, img):
        color = 1
        return color == img[y,x]
        """isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == color[key])):
                    isEqual = False"""

        return isEqual

    def isBorder(self, x, y, img):
        isEqual = True
        for key, bgr in enumerate(img[y,x]):
            if(isEqual):
                if(not (bgr == BORDER_COLOR[key])):
                    isEqual = False
        return isEqual

    def isInArea(self, x, y):
        if(x >= 0 and y >= 0 and x < self.imageDim[0] and y < self.imageDim[1]):
            #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: True')
            return True
        #print(f'x: {x}, y: {y}, w: {self.imageDim[0]}, h: {self.imageDim[1]}, in: False')
        return False

class MongaGUI(BoxLayout):
    pass

class MongaApp(App):
    def download(self):
        font = DOWNLOAD.ids.formatSpinner.text
        homedir = os.path.expanduser("~")
        homedir = homedir.replace("\\", "/")
        path = f"{homedir}/Downloads/bellagianda.{font}"# da qui ho capitò che non usero mai piu python

        image = Image.open("./pictures/provaEdoBN.png")
        image.save(path)
       
        print(homedir)

    def format_changed(self):
        global DOWNLOAD
        font = DOWNLOAD.ids.formatSpinner.text
        #print(font)
        #self.root.ids.fontLabel.font_name = font

    def build(self):
        mongaGUI = MongaGUI()
        return mongaGUI
    
    

if __name__ == '__main__':
    MongaApp().run()