from abc import ABC, abstractmethod
import random
import Database
from datetime import datetime


# Database connection
database = Database.DB()


class User(ABC):
    # Constructor
    def __init__(self, ID, fname, sname, password):
        self.ID = ID
        self.fname = fname
        self.sname = sname
        self.password = password

    # Accesors
    def getID(self):
        return self.ID
    
    def getFname(self):
        return self.fname
    
    def getSname(self):
        return self.sname
    
    def getPassword(self):
        return self.password

    # Methods
    @abstractmethod
    def validateUser(userNo, password):
        pass



class Lecturer(User):
    # Constructor
    def __init__(self, ID, fname, sname, password):
        super().__init__(ID, fname, sname, password) # call constructor on parent class user

    # Methods
    def validateUser(userNo, password):
        for user in database.fetch('user'):
            print(user[0])
            if user[4].lower() == 'lecturer':   # if database entry is a lecturer, not a student
                if user[0] == userNo:   # if lecturer number exists
                    if user[3] == password:   # if password matches
                        return True, user[1], user[2] # return True (credentials valid), first name, surname
                    break
        return False, '', ''



class Student(User):
    # Constructor
    def __init__(self, ID, fname, sname, password):
        super().__init__(ID,fname, sname, password) # call constructor on parent class user

    # Methods
    def validateUser(userNo, password):
        for user in database.fetch('user'):
            if user[4].lower() == 'student': # if database entry is a student, not a lecturer
                if user[0] == userNo: # if student number exists
                    if user[3] == password: # if password matches
                        return True, user[1], user[2] # return True (credentials valid), first name, surname
                    break
        return False, '', ''



class Question:
    # Constructor
    def __init__(self, ID, level, question, answer):
        self.ID = ID
        self.level = level
        self.question = question
        self.answer = answer

    # Accesors
    def getID(self):
        return self.ID

    def getQuestion(self):
        return self.question
    
    def getDifficulty(self):
        return self.level
    
    def getAnswer(self):
        return self.answer



class Assignment:  
    # Constructor
    def __init__(self, ID, releaseDate, endDate, easy:int, medium:int, hard:int):
        self.ID = ID # to get this ID we need a method that looks at the database to see what the next ID should be
        self.releaseDate = releaseDate
        self.endDate = endDate
        self.easy = easy
        self.medium = medium
        self.hard = hard

    # Accessors
    def getID(self):
        return self.ID
    
    def getReleaseDate(self):
        return self.releaseDate
    
    def getEndDate(self):
        return self.endDate
    
    def getEasy(self):
        return self.easy
    
    def getMedium(self):
        return self.medium
    
    def getHard(self):
        return self.hard



class StudentAssignment:
    # Constructor
    def __init__(self, assignment:Assignment, student:Student):
        self.assignment = assignment
        self.student = student

        self.questions = [] # of type Question - Assignment is just a list of questions
        self.studentAnswers = [] # of type String - only set once student takes and submits test (hence set method)
        self.marks = [] # of type Boolean - only set once student submits test (in markAssignment method)
        self.mark = 0
        
        self.loadAssignment() # Fills questions list, and student Answers and marks if completed. 


    # Accesors
    def getQuestions(self):
        return self.questions
    
    def setStudentAnswers(self, studentAnswers):
        self.studentAnswers = studentAnswers


    # Methods - Load up an assignment that has been created for a student
    def loadAssignment(self):
        # Fill question list
        for stuAssQuest in database.fetch('studentassignmentquestion'):
            # If this is the right assignment and student
            if (stuAssQuest[0] == self.assignment.getID() and stuAssQuest[1] == self.student.getID()):
                for question in database.fetch('question'): # find the question in the table
                    if (question[0] == stuAssQuest[2] and question[1] == stuAssQuest[3]): # if question ID and level are the same (composite key)
                        self.questions.append(Question(question[0],question[1],question[2],question[3])) # add question to students list of questions
                        break # you've found this specific question, now look for another one of this student's questions

        if StudentAssignment.assignmentTaken(self): # if assignment already, then already been marked and has student answers
            # Fill student answers list and marks list
            for question in self.questions:
                for studentAnswer in database.fetch('studentanswers'):
                    # If this is the right assignment and student and question
                    if (studentAnswer[0] == self.assignment.getID() and studentAnswer[1] == self.student.getID() and studentAnswer[2] == question.getID() and studentAnswer[3] == question.getDifficulty()):
                        self.studentAnswers.append(studentAnswer[4]) # add student answer to list of student answers
                        questionMark = QuestionsUtility.markQuestion(question.getAnswer(), studentAnswer[4])
                        self.marks.append(questionMark)
                        if questionMark:
                            self.mark += 1
                        break # you've found this specific student answer to the specific question, now look for another one
    
    # Mark the assignment question by question, given the student answers
    def markAssignment(self):
        questionNo = 0
        # Mark each question by comparing student answer to real answer, and store mark in marks list
        for question in self.questions:
            questionMark = QuestionsUtility.markQuestion(question.getAnswer(), self.studentAnswers[questionNo])
            self.marks.append(questionMark)
            if (questionMark):
                self.mark += 1
            # Add student answer to database
            database.insert("StudentAnswers", [self.assignment.getID(), self.student.getID(), question.getID(), question.getDifficulty(), self.studentAnswers[questionNo]]) 
            questionNo += 1
        # Add student total mark to database
        database.insert("Mark", [self.assignment.getID(), self.student.getID(), self.mark])

    # Check if assignment has been taken by the student yet
    def assignmentTaken(self):
        for mark in database.fetch('mark'):
            # if the student has a mark for the assignment, they've taken the assignment
            if mark[0] == self.assignment.getID() and mark[1] == self.student.getID(): 
                print("Found it. This student has taken the assignment")
                return True
        return False
    


class StudentPracticeAssignment:
    # Constructor
    def __init__(self, easy, medium, hard):
        self.easy = easy
        self.medium = medium
        self.hard = hard

        self.questions = [] # of type Question - Assignment is just a list of questions
        self.studentAnswers = [] # of type String - only set once student takes and submits test (hence set method)
        self.marks = [] # of type Boolean - only set once student submits test (in markAssignment method)
        self.mark = 0

        self.createPracticeAssignment() # fills questions list


    # Accessors
    def getQuestions(self):
        return self.questions
    
    def setStudentAnswers(self, studentAnswers):
        self.studentAnswers = studentAnswers        


    # Methods - Create a once-off practice assignment with the desired number of easy, medium and hard random questions
    def createPracticeAssignment(self):
        noTotalEasyQuestions = AssignmentUtility.noTotalQuestions(1)
        noTotalMediumQuestions = AssignmentUtility.noTotalQuestions(2)
        noTotalHardQuestions = AssignmentUtility.noTotalQuestions(3)

        easyQuestions = []
        mediumQuestions = []
        hardQuestions = []

        for question in database.fetch('question'):
            # check what the question level is
            if question[1] == 1: 
                easyQuestions.append(question)
            elif question[1] == 2:
                mediumQuestions.append(question)
            else:
                hardQuestions.append(question)

        randomListEasy = []
        # randomly pick the IDs of the desired number of easy questions
        r=random.randint(0,noTotalEasyQuestions-1) # need to get noTotalEasyQuestions from DBQuestions
        for i in range(self.easy):
            while (r in randomListEasy): # continue until this number is new 
                r=random.randint(0,noTotalEasyQuestions-1)
            randomListEasy.append(r) # keep track of the questions already used
            aQuestion = easyQuestions[r]
            # Add question to the questions list
            self.questions.append(Question(aQuestion[0],aQuestion[1],aQuestion[2],aQuestion[3]))

        randomListMedium = []
        # randomly pick the IDs of the desired number of easy questions
        r=random.randint(0,noTotalMediumQuestions-1) # need to get noTotalMediumQuestions from DBQuestions
        for i in range(self.medium):
            while (r in randomListMedium): # continue until this number is new 
                r=random.randint(0,noTotalMediumQuestions-1)
            randomListMedium.append(r) # keep track of the questions already used
            aQuestion = mediumQuestions[r]
            # Add question to the questions list
            self.questions.append(Question(aQuestion[0],aQuestion[1],aQuestion[2],aQuestion[3]))
        
        randomListHard = []
        # randomly pick the IDs of the desired number of easy questions
        r=random.randint(0,noTotalHardQuestions-1) # need to get noTotalHardQuestions from DBQuestions
        for i in range(self.hard):
            while (r in randomListHard): # continue until this number is new 
                r=random.randint(0,noTotalHardQuestions-1)
            randomListHard.append(r) # keep track of the questions already used
            aQuestion = hardQuestions[r]
            # Add question to the questions list
            self.questions.append(Question(aQuestion[0],aQuestion[1],aQuestion[2],aQuestion[3]))

    # Mark the assignment question by question, given the student answers
    def markAssignment(self):
        questionNo = 0
        # Mark each question by comparing student answer to real answer, and store mark in marks list
        for question in self.questions:
            questionMark = QuestionsUtility.markQuestion(question.getAnswer(), self.studentAnswers[questionNo])
            self.marks.append(questionMark)
            if (questionMark):
                self.mark += 1 # correct answer
            questionNo += 1



# Static methods that assist and provide functionality for generation and manipulation of assignments
class AssignmentUtility:

    # Create an assignment and add it permanently to the database
    @staticmethod
    def createAssignment(releaseDate, endDate, easy, medium, hard):
        assignment = Assignment(AssignmentUtility.getNextAssignmentID(), releaseDate, endDate, easy, medium, hard)
        database.insert("Assignment", [assignment.getID(), releaseDate, endDate, easy, medium, hard]) # add assignment to database
        AssignmentUtility.generateStudentAssignments(assignment) # generate unique assignments for each student

    # Generate unique assignments for each student with the desired number random questions, and add to the database
    @staticmethod
    def generateStudentAssignments(assignment:Assignment):
        noTotalEasyQuestions = AssignmentUtility.noTotalQuestions(1)
        noTotalMediumQuestions = AssignmentUtility.noTotalQuestions(2)
        noTotalHardQuestions = AssignmentUtility.noTotalQuestions(3)

        # Generate an assignment for each student
        for student in database.fetch('user'):
            if student[4].lower() == 'student': # must be a student

                randomListEasy = []
                # randomly pick the IDs of the desired number of easy questions
                r=random.randint(0,noTotalEasyQuestions-1) # need to get noTotalEasyQuestions from DBQuestions
                for i in range(assignment.getEasy()):
                    while (r in randomListEasy): # continue until this number is new 
                        r=random.randint(0,noTotalEasyQuestions-1)
                    randomListEasy.append(r) # keep track of the questions already used
                    # Add question to the database
                    database.insert("StudentAssignmentQuestion", [assignment.getID(), student[0], r, 1]) # columns in the table are assignment ID, student ID, question ID, question level


                randomListMedium = []
                # randomly pick the IDs of the desired number of medium questions
                r=random.randint(0,noTotalMediumQuestions-1)
                for i in range(assignment.getMedium()):
                    while (r in randomListMedium): # continue until this number is new 
                        r=random.randint(0,noTotalMediumQuestions-1)
                    randomListMedium.append(r) # keep track of the questions already used
                    # Add question to the database
                    database.insert("StudentAssignmentQuestion", [assignment.getID(), student[0], r, 2]) # columns in the table are assignment ID, student ID, question ID, question level
        

                randomListHard = []
                # randomly pick the IDs of the desired number of hard questions
                r=random.randint(0,noTotalHardQuestions-1)
                for i in range(assignment.getHard()):
                    while (r in randomListHard): # continue until this number is new 
                        r=random.randint(0,noTotalHardQuestions-1)
                    randomListHard.append(r) # keep track of the questions already used
                    # Add question to the database
                    database.insert("StudentAssignmentQuestion", [assignment.getID(), student[0], r, 3]) # columns in the table are assignment ID, student ID, question ID, question level

    # Get the total number of existing questions at a given level 
    @staticmethod
    def noTotalQuestions(level):
        count = 0
        for questions in database.fetch('question'):
            if questions[1] == level:
                count += 1
        return count
    
    # Get the next available assignment ID from the database 
    @staticmethod
    def getNextAssignmentID():
        latestAssignmentID = -1
        for assignment in database.fetch('assignment'):
            if assignment[0] > latestAssignmentID:
                latestAssignmentID = assignment[0]
        
        return latestAssignmentID + 1
    
    # Return whether an assignment exists or is open, and information on the open/existing assignment  
    @staticmethod
    def assignmentExistsAndOpen(): # Check to see if any assignment exists and if still open to be taken 
        # If no assignments exists
        if len(database.fetch('assignment')) == 0: 
            print ('no assignments exist')
            return False, False, '', '', '', '', '', '' # return False (no assignment found), False (no assignment open)

        # If an assignment exists and is still open
        newestAssignment = database.fetch('assignment')[0]
        for assignment in database.fetch('assignment'):
            if newestAssignment[2] < assignment[2]:
                newestAssignment = assignment
            # if an assignment is still open (current date is between release and end date)
            print(assignment[1], datetime.now().strftime("%Y-%m-%d %H:%M"), "\n", assignment[2], datetime.now().strftime("%Y-%m-%d %H:%M"))
            if (assignment[1] <= datetime.now().strftime("%Y-%m-%d %H:%M")) and (assignment[2] > datetime.now().strftime("%Y-%m-%d %H:%M")): 
                return True, True, assignment[0], assignment[1], assignment[2], assignment[3], assignment[4], assignment[5] # return True (assignment found), True (assignment still open), assignment ID, rel Date, end Date, Easy, Med, Hard 
                
        # If an assignment exists but is closed
        print ('assignment exists but not open')
        return True, False, newestAssignment[0], newestAssignment[1], newestAssignment[2], newestAssignment[3], newestAssignment[4], newestAssignment[5] # return True (assignment found), False (assignment closed), assignment, rel Date, end Date, Easy, Med, Hard 

        

# Static methods that assist and provide functionality for generation and manipulation of questions
class QuestionsUtility:

    # Mark a question given the correct answer and the students answer to the question
    @staticmethod
    def markQuestion(correctAnswer:str, studentAnswer:str):
        # If no answer given
        if (studentAnswer == ""):
            return False
        
        # If the statement is an insert or delete question, the answers must be identical        
        if (studentAnswer[:6].lower() == 'insert' or studentAnswer[:6].lower() == 'delete'):
            if (correctAnswer.lower() == studentAnswer.lower()):
                return True
            else:
                return False

        # If answers are identical, immediately mark correct
        elif (correctAnswer.lower() == studentAnswer.lower()): 
            return True
        # If the student sql statement gives an sql error, immediately mark incorrect
        elif (database.executeStatment(studentAnswer) == "error"):
            return False
        else:
            # Compare actual outputs of sql statements
            if (database.executeStatment(studentAnswer) == database.executeStatment(correctAnswer)):
                return True
            return False

    # Get the next available question ID of a given level from the database  
    @staticmethod
    def getLastQuestion(level):
        return database.getLastQ(level)
    
    # Add the new questions to the table question
    @staticmethod
    def createQuestions(id,level,question,answer): 
        database.insert("question", [id, level, question, answer])
    
    # Get the column names in the variable tablename
    @staticmethod
    def getTableName(tablename):
        return database.getTable(tablename)
    
    # Get the names of tables in the database 
    @staticmethod
    def getTables(): 
        return database.get_tables() 