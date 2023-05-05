import cv2
from kivy.uix.boxlayout import BoxLayout
from input.image.imageselector import getPath
from input.image.imageselector import getIsResult
from kivy.properties import StringProperty

from kivy.logger import Logger

BORDER_COLOR = [0,0,0]
FLOAD_COLOR = (0,0,0)
contours = -1
borderSize = 1
border = True

def getBorderColor():
    return BORDER_COLOR
def getCountours():
    return contours
def getBorderSize():
    if(border):
        return borderSize
    return 0
class Border(BoxLayout):
    txt = StringProperty()
    tolerance = 100
    showBorder = True
    def __init__(self, row, **kwargs):
        super(Border, self).__init__(**kwargs)
        self.txt = row
    
    def on_color(self, instance, value):
        global BORDER_COLOR
        global FLOAD_COLOR

        # Colore del bordo
        BORDER_COLOR = [int(value[2] * 255), int(value[1] * 255), int(value[0] * 255)]

        # Colore dell'area selezionata
        FLOAD_COLOR = (255 - BORDER_COLOR[0],255 -BORDER_COLOR[1],255 - BORDER_COLOR[2])

    def updateImage(self):
        if(not getIsResult()):
            global borderSize
            global border
            self.tolerance = self.ids.tolerance_slider.value
            border = self.ids.switch.active
            borderSize = self.ids.border_slider.value
            self.showBorder = self.ids.switch.active
            #print(self.showBorder)
            self.createBorderImage()

            tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
            tolValue = f'Tolerance: {str(tolPer)}%'
            self.ids.tolerance_label.text = tolValue

    def createBorderImage(self):
        # Legge l'immagine corrispondente alla path
        #print(f'pathDaModificare: {getPath()}')
        img = cv2.imread(getPath())

        # Converte l'immagine ad una scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applica il thresholding nell'immagine grigia per avere un'immagine binaria
        ret,thresh = cv2.threshold(gray,150,255,0)

        global contours
        # Trova il contorno usando l'immagine binaria
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # Per ogni contorno calcola area e perimetro
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            # Se l'area è maggiore ad un determinato numero la disegna sull'immagine
            if(area > self.tolerance):
                # border size{ min:1 | max:10 } 
                global borderSize
                cv2.drawContours(img, [cnt], -1, BORDER_COLOR, borderSize)

        # Crea una nuova immagine che conterrà i bordi
        pathTempImage = './pictures/imageMod.png'
        cv2.imwrite(pathTempImage, img)
        
