import tkinter as tk
import cv2
from tkinter import filedialog
from kivy.uix.boxlayout import BoxLayout
from generatecloud import getWC
import matplotlib.pyplot as plt

from kivy.logger import Logger
class Download(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Download, self).__init__(**kwargs)
    @staticmethod
    def downloadFormat():
        root = tk.Tk()
        root.withdraw()
        file = filedialog.asksaveasfile(
                initialfile="wordcloud",
                title="Save the wordcloud",
                defaultextension=".png",
                filetypes=(
                    ("Image files", "*.webp"),
                    ("Image files", "*.jpg"),
                    ("Image files", "*.jpeg"),
                    ("Image files", "*.png")
                )
            )
        img = cv2.imread("./pictures/imageMod.png")
        if (file is None):
            Logger.info(f'[download.py] annullato scaricamento')
        else:
            Logger.info(f'[download.py] Immagine scaricata in: {file.name}')
            return cv2.imwrite(file.name, img)