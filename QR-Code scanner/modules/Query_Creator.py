import mysql.connector as mysql_connector


class Query_Creator:

    def __init__(self, db_alive_connection):
        self.conn = db_alive_connection[0]
        self.cursor = db_alive_connection[1]

    def execute_query(self, query, query_type):
        """
        This method execute query and sets the query_type
        if succesfull return True
        """

        # print statement + values
        print("Executing Query ", query)

        # try to execute query with cursor
        try:
            print(query)
            # check if cursor is able to execute query
            self.cursor.execute(query)
            print("query ok")

        # statement not successful? set db error to value e
        except mysql_connector.Error as e:
            print(f"Error executing query to Database: {e}")

        # if query type is equal to 1 (insert & commit)
        # commit cursor to db
        if query_type == 1:
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) successfully added")
            return True

        # if query type = 2 (fetch & print result)
        # fetch all result from cursor
        elif query_type == 2:
            return self.cursor.fetchall()

        # if query type is equal to 3 (delete & commit)
        # commit cursor to db
        elif query_type == 3:
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) deleted")
            return True

        # if query type is equal to 3 (update & commit)
        # commit cursor to db
        elif query_type == 4:
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) updated")
            return True

    # try to create the specified database
    # Catch and display any error
    # Draft

    def create_db(self, db_name):
        """
        This method will create a database
        If succesfull return True
        """
        try:
            # check if cursor is able to create databse
            if self.cursor.execute("CREATE DATABASE ", db_name, ""):
                print("Database created ok")
                return True
            else:
                return False
        except self.cursor.Error as e:
            print(f"Error creating Database ", db_name, " : {e}")

    # try to create the specified table
    # Catch and display any error.
    # Draft

    def create_servers_table(self):
        """
        This method creates a table
        If succesfull return True
        """
        try:
            # execute create table command
            if self.cursor.execute("CREATE TABLE Connected_Servers(ServerID int NOT NULL " +
                                   "AUTO_INCREMENT,ServerName varchar(255),ServerIP varchar(255),CONSTRAINT UC_Server " +
                                   "PRIMARY KEY (ServerID,ServerName))"):
                print("Table created ok")
                return True
            else:
                return False
        # trow exceptionss
        except self.cursor.Error as e:
            print(f"Error creating Table : {e}")

    def insert(self, table, columns, data_val):
        """
        This method will create an insert_query
        if executing query is succesfull return true
        """
        # set statement value's
        # value of table should be in single quotes
        _syntax_query = "INSERT INTO "
        _table = table  # "users"
        _columns = columns  # "(first_name, lastname)"
        _values = " VALUES " + str(data_val)

        # merge  value's to create query
        query = str(_syntax_query) + str(_table) + str(_columns) + str(_values)

        # set query type to 1 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 1

        # execute query with current query value's
        if self.execute_query(query, query_type):
            return True
        else:
            return False

    def insert_child(self, table, columns, data_val):
        """
        This method will create an insert_query
        if executing query is succesfull return true
        """
        # set statement value's
        # value of table should be in single quotes
        _syntax_query = "INSERT INTO "
        _table = table  # "users"
        _columns = columns  # "(first_name, lastname)"
        _values = " VALUES " + str(data_val )
        # merge  value's to create query
        query = str(_syntax_query) + str(_table) + str(_columns) + str(_values ) 
        
        # set query type to 1 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 1

        # execute query with current query value's
        if self.execute_query(query, query_type):
            return True
        else:
            print("failed")
            return False

    def select_where(self, table, data_val, where_val):
        """
        This method will create a select query 
        If executing query is succesfull return rows
        """
        # set statement value's
        # value of table should be in single quotes

        query = "Select " + str(data_val) + " from " + str(table) + "WHERE" + where_val + ";"

        # set query type to 2 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 2

        # execute query with current query value's
        rows = self.execute_query(query, query_type)
        return rows

    def select(self, table, data_val):
        """
        This method will create a select query 
        If executing query is succesfull return rows
        """
        # set statement value's
        # value of table should be in single quotes

        query = "Select " + str(data_val) + " from " + str(table) + ";"

        # set query type to 2 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 2

        # execute query with current query value's
        rows = self.execute_query(query, query_type)

        return rows

    def delete(self, table_name, columns, data_val):
        """
        This method will create a delete query
        if executing query is  succesfull return True
        """

        # set statement value's
        # value of table should be in single quotes
        _syntax_query = "DELETE FROM ", table_name, \
            " WHERE ", columns, " = ", data_val

        # merge to create statement
        query = _syntax_query

        # set query type to 2 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 3

        # execute query with current query value's
        if self.execute_query(query, query_type):
            return True

    # updates
    def update(self, table_name, columns, where_val, data_val):
        """ 
        This method will create an update method
        If executing query is succesfull return True
        """
        # set statement value's
        # value of table should be in single quotes
        update_list = []
        data_index = 0 
        for c in columns:
            print(c)
            print(data_val[data_index])
            update_list.append(str(c) + " = '" + str(data_val[data_index])+ "'" )
            if data_index > len(update_list):
                break
            else:
                data_index = data_index + 1
        target = {34:None, 91:None , 93:None} 
        translated_update_list=(str(update_list).translate(target))


        query = "UPDATE " + str(table_name) + " SET "+ translated_update_list  + " WHERE " + str(where_val)
        
        # set query type to 2 for execute query
        # This so execute query() understands what type of query we are trying to execute
        query_type = 4

        # execute query with current query value's
        if self.execute_query(query, query_type):
            print("qc-s")
            return True
        else:
            return False
