from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class ImageSelector(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(ImageSelector, self).__init__(**kwargs)
        self.txt = row