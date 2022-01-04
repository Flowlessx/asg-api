from modules.User import User
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.toast import toast
from modules.DB_Connection import DB_Connection
from modules.Query_Creator import Query_Creator

# Login Screen
class Login(Screen):
    # define login button
    login_button = ObjectProperty(None)

    # Window bind on key down
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

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

    # check if login button is focussed and enter { keycode[] 40 } is pressed
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.login_button.focus and keycode == 40:
            # execute self.login
            self.login_process()
        elif keycode == 40:
            # execute self.login
            self.login_process()

    # checks login credentials from user input
    def login_process(self):
        user_name = self.ids.userfield.text
        user_password = self.ids.password.text

        # set current user and set username and password
        # from input value's to the User object
        current_user = User(user_name, user_password)

        # create new Database Object
        # db = DB("","","","")
        # create new Database Connection Object
        # db_conn = DB.connect_db(db)
        # use db conn to execute query
        # query = SELECT user_password WHERE user_name == $user_name
        # result = DB.execute_query(db_conn, query)

        # Execute check_login_details in user class with current_user/ User Object
        if User.check_login_details(current_user):
            # if check_login_details returns true set screen to workspace_GUI
            self.manager.current = "index"

        else:
            # if details are not correct let user know , log the event and return
            print('LOGIN >>> FAILED! User: ' + user_name)
            toast("Incorrect Login! Please Try Again.")
        return
