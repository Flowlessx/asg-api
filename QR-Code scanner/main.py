# import kivy builder
# import Kivy Config
# import kivy Config
from kivy.config import Config
# import kivy window
from kivy.core.window import Window
from kivy.lang import Builder
# import kivy properties
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import EventDispatcher, Screen, ScreenManager
#import kivymd
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

# import Database Modules
from modules.DB_Connection import DB_Connection
from modules.Query_Creator import Query_Creator
from screen_modules.Index import Index

# import screen classes {! Not unused imports}
from screen_modules.Login import Login


# Mouse config to remove red dot
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Keyboard config to track keyboard behavior
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

# set loader to none type 
Loader = None


class MyScreenManager(ScreenManager):
    shared_data = StringProperty("")
sm = MyScreenManager()
# workspace app and build screen_manager
class Airstar_Dashboard(MDApp):
    def build(self):

        # window to borderless
       # Window.borderless = True
        # window to fullscreen
        #Window.fullscreen = 'auto'

        # theme style
        self.theme_cls.theme_style = "Dark"

        # theme colours
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "DeepPurple"
        self.theme_cls.primary_hue = "A700"
       
        # Build kivy file
        return Builder.load_file('kivy/screen_manager.kv')


    # add rail open function for collapsing railbar
    def rail_open(self):
        if self.root.ids.rail.rail_state == "open":
            self.root.ids.rail.rail_state = "close"
        else:
            self.root.ids.rail.rail_state = "open"


# Create Content Navigation Drawer
class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()



# check if file is main file.
if __name__ == '__main__': 
    Airstar_Dashboard().run()
