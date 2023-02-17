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

imageWidth = 0

class ConterGUI(BoxLayout):
    pass 
    def on_touch_down(self, touch):
        print(touch.pos)
        
        imageWidth = self.ids.image.size
        print(imageWidth)
        #if super(testerApp, self).on_touch_down(touch):
        #    print("true")
        #touch.grab(self)
        #self.points.append(touch.pos)

class ConterApp(App):
    def build(self):
        return ConterGUI()
    path = './pictures/cerchios.png'
    def build(self):            
        self.build_image()
        return ConterGUI()

    def build_image(self):
        
        img = cv2.imread(self.path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(gray,150,255,0)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours in image:",len(contours))
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            if(area > 1000):
                print('Area:', area)
                print('Perimeter:', perimeter)
                cv2.drawContours(img, [cnt], -1, (0,0,255), 3)
                x1, y1 = cnt[0,0]

        #cv2.imshow("Image", img)
        #self.path = "./pictures/cerchio.png"
        #pathTempImage = self.path + '.png'
        #cv2.imwrite(pathTempImage, img)


    #def on_touch_down(self, touch):
    #    print("Mouse Down", touch)
    
    

if __name__ == '__main__':
    ConterApp().run()
    
    