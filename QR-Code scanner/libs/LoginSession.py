class LoginSession:
    # initialize login session
    def __init__(self, user_name, user_password):

        # class constructor
        self._user_name = user_name
        self._user_password = user_password
    
    # find user credentials based on user input
    def find_user_credentials(self):
        # create query that selects password where username equals the users input username
        query = " SELECT user_password FROM users WHERE user_name == " + self._user_name 
        print(query)
    
    # check login details after database
    def check_login_details(self, query_result):
        if self._user_name == 1 and self._user_password == 1:
            print("login succesfull")     

            
