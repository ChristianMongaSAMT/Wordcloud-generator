from wordcloud import WordCloud, ImageColorGenerator#, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image

#text = open('file.txt', 'r').read()
text = "ciao come stai EDOARDO GAY LI PIACE IL CAZZO soono bello ok brutto ad sef saf4d as f a sdjbd  dfgb dg  da dq qwe qe"
excludedWords = "ciao"

#print(STOPWORDS)

python_mask = np.array(PIL.Image.open("./pictures/.delta.png"))

colormap = ImageColorGenerator(python_mask)

wc = WordCloud(
                stopwords=excludedWords,    # Parole vietate
                mask=python_mask,           # Maschera su cui deve lavorare
                background_color="white",   # Colore del background
                contour_color="yellow",      # Colore del contorno
                contour_width=5,            # Size del contorno
                min_font_size=3,            # Size minima del font
                max_words=100               # Parole massime
            ).generate(text)    

WordCloud.to_file(wc, "prova.png")
plt.savefig("prova.png")
plt.imshow(wc)
plt.axis("off")
plt.show()