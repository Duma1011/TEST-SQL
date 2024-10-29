#The following is my python code to connect to, insert into, and fetch from an SQLITE3 database. Insertion works because the information is reflected in the SQLiteStudio app. However, when i access the database with fetch(), this new value that I inserted is not there. Do I need to refresh the connection somehow? If so, how do I do that?


import sqlite3
import Logic


class DBTest:

    def __init__(self):
        self.DBConnection = None
        self.DBCursor = None
        self.establish_connection()

    def establish_connection(self):
        # Initialize the connection and cursor
        self.DBConnection = sqlite3.connect("D:/27636/University/3rd Year/Second Semester/CSC3003S/Capstone Project/Capstone Project Code/test1.db")
        self.DBCursor = self.DBConnection.cursor()

    def refresh_connection(self):
        # Close the existing connection and cursor
        self.DBConnection.close()
        # Reopen a new connection and cursor
        self.establish_connection()

    
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
        elif tableName.lower()=="marks":
            data = (values[0],values[1],values[2])
            self.DBCursor.execute("INSERT INTO Marks (assignment_id, student_id, mark) VALUES (?, ?, ?)",data);    
        self.commit()

        # refresh/get updated information
        #self.refresh_connection()


# I have added the commit() function as reccommended, but it still does not work. The following is the code of the actual program I use that accesses the DBTest class. Could it be a problem here?

class TestProgram:
    def Testing():
        database = DBTest()
        tblAssignment = database.fetch('assignment')

        assignmentsBefore = []
        assignmentsAfter = []

        # Check what assignments exist in the table
        print("Existing assignments before insertion:")
        for assignment in tblAssignment:
            assignmentsBefore.append(assignment[0])
            print(assignment[0]) # print the IDs of all the assignments

        
        # insert the new assignment
        database.insert("Assignment", [Logic.GenerateAssignment.getNextAssignmentID(), '2023-09-12', '2023-09-12', 3, 3, 3])
        database.DBConnection.commit()
        tblAssignment = database.fetch('assignment')

        # Check what assignments exist in the table again to see if new assignment registered
        print("Assignments after insertion:")
        for assignment in tblAssignment:
            assignmentsAfter.append(assignment[0])
            print(assignment[0]) # print the IDs of all the assignments 

        # Was the insertion noticed/registered
        for assignmentAfter in assignmentsAfter:
            if (assignmentAfter not in assignmentsBefore):
                print("They're Different!!!!")
                return
        print("They're the same :(. Still not registering") 


    Testing()  