
import logging
import kivy

from kivy.app import App
from kivy.lang import Builder

downloadScreen = Builder.load_file("./download.kv")

class DownloadApp(App):
    def build(self):
        return downloadScreen
    
    def downloadImage(self):
        print('download!!!!')

if __name__ == '__main__':
    DownloadApp().run()
