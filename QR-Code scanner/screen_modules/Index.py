
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.toast import toast
from modules.DB_Connection import DB_Connection
from modules.Query_Creator import Query_Creator
from kivy_garden.zbarcam import ZBarCam

# User_Overview Screen
class Index(Screen):
    pass
    #  create db connection
    def create_db_conn(self):
        """
        Create Database Connection object with credentials
        """
      
        # start Database connection with specified value's
        db_conn = DB_Connection("root", "AirStar", "localhost", "3306", "deliverme")

        # connect to db
        open_db_conn = db_conn.connect_db()

        # create cursor
        cursor = open_db_conn.cursor()

        # open database connection
        query = Query_Creator(db_conn, cursor)
