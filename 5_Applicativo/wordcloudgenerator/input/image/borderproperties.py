from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class Border(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(Border, self).__init__(**kwargs)
        self.txt = row

class Tolerance(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(Tolerance, self).__init__(**kwargs)
        self.txt = row
    
    def editTolerance(self):
        print("prova tasto")