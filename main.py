import os, sys
import utils
from datapack import Datapack
from collections import defaultdict

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.lang import Builder

EXE_DIRECTORY = os.path.dirname(sys.argv[0])

def is_empty(path: str) -> bool:
    files = os.listdir(path)
    return ( 
        'pack.mcmeta' not in files 
        and
        'data' not in files
    )

class MainWindow(Screen):
    datapack = Datapack(EXE_DIRECTORY)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.init, 1)

    def init(self, *args) -> None:
        if EXE_DIRECTORY.split(os.sep)[-2] != 'datapacks':
            self.manager.transition = NoTransition()
            self.manager.current = "path_invalid"
            return
        if is_empty(EXE_DIRECTORY):
            self.manager.transition = NoTransition()
            self.manager.current = "generate_datapack"
            return
        
class GenerateDatapack(Screen):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.optional_files = defaultdict(bool)

    def test(self) -> None:
        print(self.optional_files)

    def checkbox_click(self, instance, value: bool, dictonary: dict, key: str):
        dictonary[key] = value

class TestWindow(Screen):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_file(utils.resource_path("kivy", "main.kv"))

def main() -> None:
    MainApp().run()

if __name__ == "__main__":
    main()