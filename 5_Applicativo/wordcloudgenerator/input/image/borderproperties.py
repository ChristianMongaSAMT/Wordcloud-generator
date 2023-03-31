import cv2
from kivy.uix.boxlayout import BoxLayout
from input.image.imageselector import getPath
from kivy.properties import StringProperty

class Border(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(Border, self).__init__(**kwargs)
        self.txt = row

    def updateImage(self):
        tolerance = self.ids.tolerance_slider.value
        self.createBorderImage(tolerance)

        tolPer = int((self.ids.tolerance_slider.value / 2000) * 100)
        tolValue = f'Tolerance: {str(tolPer)}%'
        self.ids.tolerance_label.text = tolValue

    def createBorderImage(self, tolerance):
        #Logger.info(f'createBorderImage with: {tolerance} on image {self.imagepath}')

        # Legge l'immagine corrispondente alla path
        print(f'pathDaModificare: {getPath()}')
        img = cv2.imread(getPath())

        # Converte l'immagine ad una scala di grigi
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Applica il thresholding nell'immagine grigia per avere un'immagine binaria
        ret,thresh = cv2.threshold(gray,150,255,0)

        # Trova il contorno usando l'immagine binaria
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            # Per ogni contorno calcola area e perimetro
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)

            # Se l'area è maggiore ad un determinato numero la disegna sull'immagine
            if(area > tolerance):
                cv2.drawContours(img, [cnt], -1, (0,0,255), 2)

        # Crea una nuova immagine che conterrà i bordi
        pathTempImage = './pictures/imageMod.png'
        cv2.imwrite(pathTempImage, img)

        #self.printAllWords(img, font, pathTempImage, wordsOrderByEmphasis)

        # Imposta la path nell'Image
        #self.ids.imageMod.source = pathTempImage
        #Logger.info(f'imageMod: {self.ids.imageMod.source}')

        # Ricarice l'immagine
        #self.ids.imageMod.reload()
