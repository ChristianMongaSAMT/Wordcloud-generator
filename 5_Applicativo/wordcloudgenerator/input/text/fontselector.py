from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.text import LabelBase

from kivy.logger import Logger


FONT_MAPPING = {}
FONT_MAPPING['Calibri'] = './fonts/calibri/Calibri.ttf'
FONT_MAPPING['Cartoon'] = './fonts/from-cartoon-blocks/From Cartoon Blocks.ttf'
FONT_MAPPING['Christmas'] = './fonts/christmas-sundaylab/Christmas Sundaylab.otf'
FONT_MAPPING['Guilty'] = './fonts/guilty-chaos/Guilty Chaos.otf'
FONT_MAPPING['Love'] = './fonts/love-sunday/Love Sunday.ttf'
FONT_MAPPING['Keisya'] = './fonts/baby-keisya/Baby Keisya.ttf'
FONT_MAPPING['Resgold'] = './fonts/resgold-willgets/Resgold Willgets Serif OTF.otf'

font = "./fonts/baby-keisya/Baby Keisya.ttf"
def getFont():
    return font
for font_name, font_path in FONT_MAPPING.items():
    LabelBase.register(name=font_name, fn_regular=font_path)  

class FontFamily(BoxLayout):
    txt = StringProperty()
    
    def __init__(self, row, **kwargs):
        super(FontFamily, self).__init__(**kwargs)
        self.txt = row
    
    def font_changed(self):
        # Memorizza il nuovo font
        global font
        font = self.ids.fontSpinner.text
        font = FONT_MAPPING[font]
        Logger.info(f'[fontselector.py] selezionato font: {font}')
        # (Test) Applica il font al label
        self.ids.fontLabel.font_name = font