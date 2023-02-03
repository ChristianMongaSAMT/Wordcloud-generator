
import logging
import logmanager
import kivy
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from pathlib import Path
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

logmanager.get_configured_logger()

class Test():   
    folder = ""

    def __init__(self, path):
        self.folder = Path(path)

    def printData(self):
        logging.debug(f'{self.folder.read_text()}')
        
class DragLabel(DragBehavior, Label):
    pass
########################DragBehavior############################
class TestApp(App):

    def build(self):
        self.title = 'ztest'
########################TestPath############################
#def run():
#    test = Test('E:\\306\\Worldcloud-generatorData\\testingPath.txt')
#    test.printData()

########################DragNDrop############################
class DraggableBoxLayout(DraggableLayoutBehavior, BoxLayout):

    def compare_pos_to_widget(self, widget, pos):
        if self.orientation == 'vertical':
            return 'before' if pos[1] >= widget.center_y else 'after'
        return 'before' if pos[0] < widget.center_x else 'after'

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)

class DragLabel(DraggableObjectBehavior, Label):

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)
####################################################################
#if __name__ == '__main__':
    #TestApp().run()