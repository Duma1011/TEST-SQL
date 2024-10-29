import sqlite3


class DB:
    def __init__(self):
        self.DBConnection = None
        self.DBCursor = None
        self.establish_connection("test1.db")

    def establish_connection(self, databaseFile):
        # Initialize the connection and cursor
        self.DBConnection = sqlite3.connect(databaseFile)
        self.DBCursor = self.DBConnection.cursor()

    def commit(self):
        self.DBConnection.commit()

    def fetch(self, tableName:str): # this method is used when you want to acquire data for specific table.
        self.DBCursor.execute("SELECT * FROM " + tableName)
        return self.DBCursor.fetchall()
        
    def insert(self, tableName:str, values:list): # this method is used to insert data into the Database
        if tableName.lower()=="assignment":
            data = (values[0],values[1],values[2],values[3],values[4],values[5])
            self.DBCursor.execute("INSERT INTO Assignment (id,reldate,enddate,easy,medium,hard) VALUES (?, ?, ?, ?, ?, ?)",data)
        elif tableName.lower()=="user":
            data = (values[0],values[1],values[2],values[3],values[4])
            self.DBCursor.execute("INSERT INTO User(id,fname,sname,password,type) VALUES (?, ?, ?, ?, ?)",data)
        elif tableName.lower()=="question":
            data = (values[0],values[1],values[2],values[3])
            self.DBCursor.execute("INSERT INTO Question (id,level,question,answer) VALUES (?, ?, ?, ?)",data)
        elif tableName.lower()=="studentassignmentquestion":
            data = (values[0],values[1],values[2],values[3])
            self.DBCursor.execute("INSERT INTO StudentAssignmentQuestion (assignment_id, student_id, question_id, question_level) VALUES (?, ?, ?, ?)",data)
        elif tableName.lower()=="studentanswers":
            data = (values[0],values[1],values[2],values[3],values[4])
            self.DBCursor.execute("INSERT INTO StudentAnswers (assignment_id, student_id, question_id, question_level, answer) VALUES (?, ?, ?, ?, ?)",data)
        elif tableName.lower()=="mark":
            data = (values[0],values[1],values[2])
            self.DBCursor.execute("INSERT INTO Mark (assignment_id, student_id, mark) VALUES (?, ?, ?)",data);    
        self.commit()

    def executeStatment(self,sqlStatement:str): # this will be used to excecute a student sql statement and return a query.
        # connect to new database here (the classicmodel one)
        self.establish_connection("classicModels2022.db")

        try:
            self.DBCursor.execute(sqlStatement.lower())
        except:
            print('error in SQL statement')
            # connect to old database here (the test.db one)
            self.establish_connection("test1.db")
            return 'error'
        
        result=self.DBCursor.fetchall()

        # connect to old database here (the test.db one)
        self.establish_connection("test1.db")

        # return results of executed statement
        if len(result)==1 and len(result[0])==1:
            print([result[0][0]])
            return [[result[0][0]]]
        else:
            return result
        
    # get the id number of the last question with the specified level
    def getLastQ(self, level:int):
        self.establish_connection("test1.db")
        self.DBCursor.execute("SELECT * FROM question WHERE level = "+str(level)+" ORDER BY id DESC LIMIT 1")
        return self.DBCursor.fetchall()
    
    # function to get all the column names in each table
    def getTable(self, tablename:str):
        self.establish_connection("classicModels2022.db")
        data=self.DBCursor.execute("SELECT * FROM " + tablename)
        # Re-establish connection to main database 
        self.establish_connection("test1.db")
        return data
    
    # method to get the names of all the tables in the database
    def get_tables(self):
        self.establish_connection("classicModels2022.db")
        sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
        self.DBCursor.execute(sql_query)
        tabs=self.DBCursor.fetchall()
        # Re-establish connection to main database 
        self.establish_connection("test1.db")
        return tabs
        
        