import tkinter as tk
import cv2
from tkinter import filedialog
from kivy.uix.boxlayout import BoxLayout
from generatecloud import getWC
import matplotlib.pyplot as plt
class Download(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Download, self).__init__(**kwargs)
    def downloadFile(self):
        print("ECCO")
    @staticmethod
    def downloadFormat():
        print("DIO NON VA")
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
        return cv2.imwrite(file.name, img)