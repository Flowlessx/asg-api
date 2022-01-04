import mysql.connector as mysql_connector

class DB_Connection:
    # initialize login session
    def __init__(self, db_user_name, db_user_password,  db_host, db_port, db_name):

        # class constructor
        self._db_user_name = db_user_name
        self._db_user_password = db_user_password

        self._db_host = db_host
        self._db_port = db_port

        self._db_name = db_name

    # connect db with db object return db connection
    def connect_db(self):
        """
        This method will connect to the database
        If succesfull return db_conn
        """
        try:
            db_conn = mysql_connector.connect(user=self._db_user_name, password=self._db_user_password, host=self._db_host, port=self._db_port,
                                              database=self._db_name)
            print("Database connection ok")
        except mysql_connector.Error as e:
            print(f"Error connecting to Database: {e}")

        # return db connection
        return db_conn
