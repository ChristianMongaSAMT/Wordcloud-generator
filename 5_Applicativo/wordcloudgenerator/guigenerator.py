import os
os.environ['KIVY_HOME'] = "./config/.kivy"


from input.text.inputselector import InputType
from input.text.importantwords import ImportantWords
from input.text.excludedwords import ExcludedWords
from input.text.fontselector import FontFamily
from input.image.imageselector import ImageSelector
from input.image.borderproperties import Border
from input.image.imagepartselector import ImageSelection
from output.download import Download

from kivy.uix.colorpicker import ColorPicker
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder

from kivy.core.window import Window



import logging
from kivy.config import Config
from kivy.logger import Logger, ColoredFormatter
# Add timestamp to log file
Logger.handlers[1].setFormatter(
    logging.Formatter('%(asctime)s %(message)s'))
# Add timestampt to console output
Logger.handlers[2].setFormatter(
    ColoredFormatter('[%(levelname)-18s] %(asctime)s %(message)s'))

config_path = os.path.join( os.environ.get('KIVY_HOME'), "config.ini")

Logger.info(f'config path: {config_path}')
Config.read("config.ini")

TEXT_OPTIONS = ["Input Type", "Important Words", "Excluded Words", "Font Family"]
IMAGE_OPTIONS = ["Image Path", "Border"]

Builder.load_string("""
<WordCloudGUI>:
    BoxLayout:
        size_hint_x: 0.25
        padding: [10, 10, 10, 10]
        ScrollView:
            TextOptions:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: 50
    BoxLayout:
        size_hint_x: 0.5
        padding: [10, 0, 0, 10]
        ImageSelected:
            orientation: "vertical"
            spacing: 50
    BoxLayout:
        size_hint_x: 0.25
        padding: [10, 10, 10, 10]
        
        ImageOptions:
            orientation: "vertical"
            spacing: 50
            
<ImageSelection>:
    BoxLayout:
        Image:
            id: image
            source: './pictures/imageMod.png'


<InputType>:
    size_hint_y: None
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.txt
            Spinner:
                id: inputType
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                text: 'LIST'
                values: 'FILE', 'LIST', 'URL'
                on_text: root.generateListWord()
            Button:
                text: "Send"
                on_release: root.generateListWord()
        ScrollView:
            id: scrlv
            TextInput:
                id: pathWords
                hint_text: "Text"
                size_hint: 1, None
                height: max(self.minimum_height, scrlv.height)

        
        
<ExcludedWords>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: root.txt
    TextInput:
        id: excludedWords
        hint_text: root.txt
        
<ImportantWords>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: root.txt
    TextInput:
        id: importantWords
        hint_text: root.txt

<FontFamily>:
    size_hint_y: None
    size_hint_x: 1
    height: 100
    Label:
        text: 'Font Family'
        id: fontLabel
    Spinner:
        text: 'Font'
        values: 'Calibri','Cartoon','Christmas','Guilty','Love','Keisya','Resgold'
        id: fontSpinner
        on_text:
            root.font_changed()

<Download>:
    size_hint_y: None
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: "Download"
            on_release: root.downloadFormat()

<ImageSelector>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Path'
        TextInput:
            id: path
            hint_text:'Enter text'
            on_text: root.visualizer()
<Border>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Border ON' if switch.active else 'Border OFF'
            Switch:
                id: switch
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Border Size'
            Slider:
                id: border_slider
                step: 1
                max: 10
                min: 1
                value: 1
                on_touch_up: root.updateImage()
        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: tolerance_label
                text: "Select Tolerance"
            Slider:
                id: tolerance_slider
                step: 10
                max: 2000
                min: 100
                value: 100
                on_touch_up: root.updateImage()

""")
class TextOptions(BoxLayout):
    def __init__(self, **kwargs):
        super(TextOptions, self).__init__(**kwargs)
        # Necessita che ogni widget sia BoxLayout
        importantWords = ImportantWords(TEXT_OPTIONS[1])
        excludedWords = ExcludedWords(TEXT_OPTIONS[2])
        fontFamily = FontFamily(TEXT_OPTIONS[3])
        download = Download()
        self.add_widget(InputType(importantWords, excludedWords, fontFamily, TEXT_OPTIONS[0]))
        Logger.info(f'[guigenerator.py] Aggiunta sezione text InputType')
        self.add_widget(excludedWords)
        Logger.info(f'[guigenerator.py] Aggiunti elementi excludedWords con successo')
        self.add_widget(importantWords)
        Logger.info(f'[guigenerator.py] Aggiunti elementi importantWords con successo')
        self.add_widget(fontFamily)
        Logger.info(f'[guigenerator.py] Aggiunti elementi fontFamily con successo')
        self.add_widget(download)
        Logger.info(f'[guigenerator.py] Aggiunti elementi download con successo')

imageSelector = ImageSelector(IMAGE_OPTIONS[0])
border = Border(IMAGE_OPTIONS[1])
imageSelection = ImageSelection()

class ImageOptions(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageOptions, self).__init__(**kwargs)
        self.add_widget(imageSelector)
        Logger.info(f'[guigenerator.py] Aggiunta sezione image options con successo')
        self.add_widget(border)
        Logger.info(f'[guigenerator.py] Aggiunti elementi border con successo')
        colorPicker = ColorPicker()
        colorPicker.bind(color=border.on_color)
        self.add_widget(colorPicker)
        Logger.info(f'[guigenerator.py] Aggiunto elemento color picker con successo')
    
class ImageSelected(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageSelected, self).__init__(**kwargs)
        self.add_widget(imageSelection)
        Logger.info(f'[guigenerator.py] Aggiunta sezione image con successo')

class WordCloudGUI(BoxLayout):
    def reloadImage(self, deltatime):
        border.updateImage()
        imageSelection.ids.image.reload()
    
    

class WordCloudApp(App):
    def build(self):
        wcg = WordCloudGUI()
        Clock.schedule_interval(wcg.reloadImage, 1 / 10.)
        return wcg
    
if __name__ == '__main__':
    open('./text/.userwords.txt', 'w').write("")
    WordCloudApp().run()