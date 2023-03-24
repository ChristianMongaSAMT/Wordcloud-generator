from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.text import LabelBase

FONT_MAPPING = {}
FONT_MAPPING['Cartoon'] = './fonts/from-cartoon-blocks/From Cartoon Blocks.ttf'
FONT_MAPPING['Borex'] = './fonts/borex/BOREX-Regular.otf'
FONT_MAPPING['Krinkes'] = './fonts/krinkes/KrinkesRegularPERSONAL.ttf'
FONT_MAPPING['Theaters'] = './fonts/theaters/THEATERS DEMO REGULAR.ttf'

for font_name, font_path in FONT_MAPPING.items():
    LabelBase.register(name=font_name, fn_regular=font_path)  

class FontFamily(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(FontFamily, self).__init__(**kwargs)
        self.txt = row
    
    def font_changed(self):
        # Memorizza il nuovo font
        self.font = self.ids.fontSpinner.text

        # (Test) Applica il font al label
        print(self.font)
        self.ids.fontLabel.font_name = self.font