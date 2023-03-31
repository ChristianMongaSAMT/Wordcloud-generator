import cv2
from kivy.uix.boxlayout import BoxLayout
from input.image.imageselector import getPath
from kivy.properties import StringProperty



BORDER_COLOR = (0,255,100)
FLOAD_COLOR = (0,0,0)
contours = -1

def getCountours():
    return contours

class Border(BoxLayout):
    txt = StringProperty()
    tolerance = 100
    borderSize = 1
    showBorder = True
    def __init__(self, row, **kwargs):
        super(Border, self).__init__(**kwargs)
        self.txt = row
    
    def on_color(self, instance, value):
        global BORDER_COLOR
        global FLOAD_COLOR

        # Colore del bordo
        BORDER_COLOR = (int(value[2] * 255), int(value[1] * 255), int(value[0] * 255))

        # Colore dell'area selezionata
        FLOAD_COLOR = (255 - BORDER_COLOR[0],255 -BORDER_COLOR[1],255 - BORDER_COLOR[2])

    def updateImage(self):
        self.tolerance = self.ids.tolerance_slider.value
        self.borderSize = self.ids.border_slider.value
        self.showBorder = self.ids.switch.active
        print(self.showBorder)
        self.createBorderImage()

        tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
        tolValue = f'Tolerance: {str(tolPer)}%'
        self.ids.tolerance_label.text = tolValue

    def createBorderImage(self):
        #Logger.info(f'createBorderImage with: {tolerance} on image {self.imagepath}')

        # Legge l'immagine corrispondente alla path
        print(f'pathDaModificare: {getPath()}')
        img = cv2.imread(getPath())

        # Converte l'immagine ad una scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applica il thresholding nell'immagine grigia per avere un'immagine binaria
        ret,thresh = cv2.threshold(gray,150,255,0)

        global contours
        # Trova il contorno usando l'immagine binaria
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



        ''' CONTROLLARE SE SI PUO TOGLIERE '''
        for cnt in contours:
            # Per ogni contorno calcola area e perimetro
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            # Se l'area è maggiore ad un determinato numero la disegna sull'immagine
            if(area > self.tolerance):
                # border size{ min:1 | max:10 } 
                cv2.drawContours(img, [cnt], -1, BORDER_COLOR, self.borderSize)

        # Crea una nuova immagine che conterrà i bordi
        pathTempImage = './pictures/imageMod.png'
        cv2.imwrite(pathTempImage, img)

        #self.printAllWords(img, font, pathTempImage, wordsOrderByEmphasis)

        # Imposta la path nell'Image
        #self.ids.imageMod.source = pathTempImage
        #Logger.info(f'imageMod: {self.ids.imageMod.source}')

        # Ricarice l'immagine
        #self.ids.imageMod.reload()
