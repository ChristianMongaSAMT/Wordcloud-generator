from input.text.inputselector import InputType
from input.text.importantwords import ImportantWords
from input.text.excludedwords import ExcludedWords
from input.text.fontselector import FontFamily
from input.image.imageselector import getQueue
from input.image.imageselector import ImageSelector
from input.image.borderproperties import Border

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

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
        Image:
            id: image
            source: './pictures/imageMod.png'
    BoxLayout:
        size_hint_x: 0.25
        padding: [10, 10, 10, 10]
        
        ImageOptions:
            orientation: "vertical"
            spacing: 50
            

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
        values: 'Cartoon','Borex','Krinkes','Theaters','Calibri','Roboto'
        id: fontSpinner
        on_text:
            root.font_changed()

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
                text: 'Border'
            Switch:
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Border Size'
            Slider:
                id: border_slider
                max: 50
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
        self.add_widget(InputType(importantWords, excludedWords, fontFamily, TEXT_OPTIONS[0]))
        self.add_widget(excludedWords)
        self.add_widget(importantWords)
        self.add_widget(fontFamily)

imageSelector = ImageSelector(IMAGE_OPTIONS[0])
border = Border(IMAGE_OPTIONS[1])

class ImageOptions(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageOptions, self).__init__(**kwargs)
        self.add_widget(imageSelector)
        #self.add_widget(ImageSelector(IMAGE_OPTIONS[0]).setQueue(q))
        self.add_widget(border)

class WordCloudGUI(BoxLayout):
    def getImagePath(self, deltatime):
        path = getQueue()
        # print(f'callback deltatime: {deltatime}, path: {path}')

        if path:
            border.savePath(path)
            self.ids.image.source = path
    def reloadImage(self, deltatime):
        border.updateImage()
        self.ids.image.reload()

class WordCloudApp(App):
    def build(self):
        wcg = WordCloudGUI()
        Clock.schedule_interval(wcg.reloadImage, 1 / 10.)
        return wcg
    
if __name__ == '__main__':
    WordCloudApp().run()