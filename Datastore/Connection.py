import sqlite3
from sqlite3 import Error

def create_connection(path):
    """This function can be used to access a connection to the database. This function should not be used outside of this module.
    pre-condition:The path argument should specify the location for the db to be store/is stored
    post-condition:A sql lite connection is returned"""
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        raise e

    return connection

class dbConnection:
    """This class provides an interface for database access that is independent of the technology used"""
    def __init__(self,sqlLiteConnetcion):
        self.connection = sqlLiteConnetcion

    def execute_query(self,query):
        """This function will execute sql queries
        pre-condition:The SQL query to execute should be passed as an argument
        post-condition:If the query was a select a result list is returned.
        If the query was an insert then the newly inserted row id is returned."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            isSelectQuery = query.strip().lower().startswith("select")
            if isSelectQuery:
                result = cursor.fetchall()
                return result
            else:
                return cursor.lastrowid
        except Error as e:
            raise e

class Connection:
    """This class keeps a reference the main dbConnection object that can be reused"""
    connection = dbConnection(create_connection("database.db"))
    def useTestDatabase(self):
        Connection.connection = dbConnection(create_connection("test_database.db"))
    def usePrimaryDatabase(self):
        Connection.connection = dbConnection(create_connection("database.db"))




