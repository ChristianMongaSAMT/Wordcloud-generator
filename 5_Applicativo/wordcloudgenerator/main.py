from wordcloud import WordCloud, ImageColorGenerator#, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image

#text = open('file.txt', 'r').read()
text = "ciao come stai"
excludedWords = "ciao"

#print(STOPWORDS)

python_mask = np.array(PIL.Image.open("./pictures/heart - Copia.png"))

colormap = ImageColorGenerator(python_mask)

wc = WordCloud(
                stopwords=excludedWords,    # Parole vietate
                mask=python_mask,           # Maschera su cui deve lavorare
                background_color="white",   # Colore del background
                contour_color="black",      # Colore del contorno
                contour_width=5,            # Size del contorno
                min_font_size=3,            # Size minima del font
                max_words=100               # Parole massime
            ).generate(text)    



plt.imshow(wc)
plt.axis("off")
plt.show()