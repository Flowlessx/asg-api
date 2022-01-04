from kivymd.toast import toast



class User:
    def __init__(self, user_name, user_password):

        # constructor
        self._username = user_name
        self._password = user_password

    def check_login_details(self):

        # check if input equals db ouput
        if self._username == "Admin" and self._password == "test123":
            return True
        # details not correct? return false
        else:
            return False
