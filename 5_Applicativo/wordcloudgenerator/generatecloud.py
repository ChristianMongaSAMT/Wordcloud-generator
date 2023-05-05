from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image 
from input.image.borderproperties import getBorderColor
from input.image.borderproperties import getBorderSize
from input.text.fontselector import getFont

from kivy.logger import Logger

wc = ""
def getWC():
    return wc
def generateCloud(size):
    text = open('./text/.userwords.txt', 'r').read()
    if(not text.strip()):
        text = open('./text/.example.txt', 'r').read()
    open('./text/.userwords.txt', 'w').write("")


    python_mask = np.array(PIL.Image.open("./pictures/.delta.png"))

    colormap = ImageColorGenerator(python_mask)

    borderColor = (getBorderColor()[2], getBorderColor()[1], getBorderColor()[0])
    global wc 
    try:
        wc = WordCloud(
                    width=size[1],
                    height=size[0],
                    font_path=getFont(),  
                    stopwords=STOPWORDS,    # Parole vietate
                    mask=python_mask,           # Maschera su cui deve lavorare
                    background_color="white",   # Colore del background
                    contour_color=borderColor,      # Colore del contorno
                    contour_width=getBorderSize()           # Size del contorno
                ).generate(text)    
        wc.recolor(color_func=colormap)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig("./pictures/imageMod.png", format="png", metadata=None,
            transparent=True, pil_kwargs=None)
        Logger.info(f'[generateclud.py] sovrascritta immagine visualizzata')
    except Exception as exc:
        Logger.error(f'{exc}')
    