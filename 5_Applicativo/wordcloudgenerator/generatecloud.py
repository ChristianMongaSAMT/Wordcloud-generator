from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image 
from input.image.borderproperties import getBorderColor
from input.image.borderproperties import getBorderSize

#text = open('file.txt', 'r').read()
def generateCloud():
    #text = ["ciao", "come", "va"]
    text = open('./text/.userwords.txt', 'r').read()
    excludedWords = "ciao"

    #print(STOPWORDS)

    python_mask = np.array(PIL.Image.open("./pictures/.delta.png"))

    colormap = ImageColorGenerator(python_mask)

    borderColor = (getBorderColor()[2], getBorderColor()[1], getBorderColor()[0])
    wc = WordCloud(
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