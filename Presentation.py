from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import Logic
import openpyxl
from datetime import datetime
from functools import partial
from tkinter.simpledialog import askstring



# Shared Variables
studentAssignment : Logic.StudentAssignment
user: Logic.User


class LoginForm:

    def main_screen():
        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Login Page")
        root.resizable(False,False)


        def signIn(): 
            # Take as input the username and password
            userNo = entUsername.get()
            password = entPassword.get()

            # Ensure both username and password entered
            if (userNo == '' or password == ''):
                messagebox.showinfo('Login Unsuccesful','Please enter a username and password')
            
            else:
                # Lecturer sign in
                if isLecturer.get(): # if lecturer checkbox is checked
                    isValid, fname, sname = Logic.Lecturer.validateUser(userNo, password)

                    if isValid: # if login credentials are valid
                        global user
                        user = Logic.Lecturer(userNo, fname, sname, password) # create a lecturer object
                        
                        messagebox.showinfo('Login Succesful','Welcome ' + fname)
                        root.destroy()
                        LecturerHomeForm.main_screen()

                    else: # if login credentials are invalid
                        messagebox.showinfo('Login Unsuccesful','Invalid Credentials')

                # Student sign in
                else:
                    isValid, fname, sname = Logic.Student.validateUser(userNo, password)
                    
                    if isValid: # if login credentials are valid
                        user = Logic.Student(userNo, fname, sname, password) # create a student object
                        messagebox.showinfo('Login Succesful','Welcome ' + fname)
                        root.destroy()
                        StudentHomeForm.main_screen()

                    else: # if login credentials are invalid
                        messagebox.showinfo('Login Unsuccesful','Invalid Credentials')
                    

        # Create frame for image
        frameImg = Frame(root, width=425, height=450, bg='white')
        frameImg.place(x=0, y=0,)
        img = ImageTk.PhotoImage(Image.open("Login.png").resize((420,450)))
        Label(frameImg, image= img).pack()   # Label Widget to display Image

        # Create a frame for all the widgets
        frame = Frame(root, width=425, height=450, bg='white')
        frame.place(relx=0.5, y=0)

        # Add widgets
        heading = Label(frame, text='Sign in', bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        heading.place(relx=0.5, y=100, anchor=CENTER)

        # Input Fields and Labels
        lblUsername = Label(frame, text='Username', fg='#899499', bg='white', font=('Arial',13))
        lblUsername.place(x=70, y=155)
        entUsername = Entry(frame, fg='black', border=2, bg='white', font=('Arial',15))
        entUsername.place(relx=0.5, y=200, width=280, height=28, anchor=CENTER)

        lblPassword = Label(frame, text='Password', fg='#899499', bg='white', font=('Arial',13))
        lblPassword.place(x=70, y=230)
        entPassword = Entry(frame, fg='black', border=2, bg='white', font=('Arial',15))
        entPassword.place(relx=0.5, y=275, width=280, height=28, anchor=CENTER)

        # Lecturer Checkbox
        isLecturer = IntVar()
        chkLecturer = Checkbutton(frame, text='Lecturer', variable=isLecturer, bg='white')
        chkLecturer.place(x=73, y=298)
        
        # Sign in button
        btnSignIn = Button(frame , text='Sign in', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=signIn)
        btnSignIn.place(relx=0.5, y=350, width=250, height=30, anchor=CENTER)

        root.mainloop()



class LecturerHomeForm:
    btnCreateAssignment: Button
    btnCreateAssignmentState = 'normal'

    def main_screen():
        # Whenever you open up LecturerHomeForm
        exists, open, id, rel, end, easy, med, hard = Logic.AssignmentUtility.assignmentExistsAndOpen()
        if open: # if an assignment is currently open, you cannot create another one
            LecturerHomeForm.btnCreateAssignmentState = 'disabled'
        else:
            LecturerHomeForm.btnCreateAssignmentState = 'normal'


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Home Page")
        root.resizable(False,False)


        # Log out and return to sign in
        def logOut():
            result = messagebox.askokcancel("Log out","Are you sure you want to log out of your profile")
            if (result):
                messagebox.showinfo('','Logged out')
                root.destroy()
                LoginForm.main_screen()
        
        # Go to Create an assignment form
        def createAssignment():
            root.destroy()
            CreateAssignmentForm.main_screen()
        
        # Go to View grades form
        def viewGrades():
            root.destroy()
            ViewGradesForm.main_screen()
            
        def auto_generate():
            root.destroy()
            Auto_Generation.main_screen()    
        
        def addQuestions():
            root.destroy()
            SingleAddition.main_screen()


        # Create frame for image
        frameImg = Frame(root, width=425, height=450, bg='white')
        frameImg.place(relx=0.5, y=0)
        img = ImageTk.PhotoImage(Image.open("LectureBackground.png").resize((420,450)))
        Label(frameImg, image= img).pack()   # Label Widget to display Image

        # Create a frame for left side
        frame = Frame(root, width=425, height=450, bg='white')
        frame.place(x=0, y=0)
        # Create a frame for the buttons
        frameButtons = Frame(frame, width=425, height=250, bg='white')
        frameButtons.place(relx=0.5, y=250, anchor=CENTER)

        # Add widgets
        heading = Label(frame, text='Welcome ' + user.getFname(), bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        heading.place(relx=0.5, y=100, anchor=CENTER)

        # View Grades, Create Assignment, Generate Questions, Single Question buttons        
        LecturerHomeForm.btnCreateAssignment = Button(frameButtons, text='Create Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), state=LecturerHomeForm.btnCreateAssignmentState, command=createAssignment)
        LecturerHomeForm.btnCreateAssignment.place(relx=0.5, y=40, width=250, height=35, anchor=CENTER)
        
        btnViewGrades = Button(frameButtons, text='View Grades', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), command=viewGrades)
        btnViewGrades.place(relx=0.5, y=90, width=250, height=35, anchor=CENTER)

        btnGenerate = Button(frameButtons, text='Auto Generate Questions', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), command=auto_generate)
        btnGenerate.place(relx=0.5, y=140, width=250, height=35, anchor=CENTER)
        
        btnSingleQuestion = Button(frameButtons, text='Add Individual Questions', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), command=addQuestions)
        btnSingleQuestion.place(relx=0.5, y=190, width=250, height=35, anchor=CENTER)

        # Creating a photoimage object to use image
        userIcon = PhotoImage(file = r"userIcon.png")
        userIcon = userIcon.subsample(12, 12) # Resizing image to fit on button
        # Log out button
        btnLogOut = Button(frame, text='Log Out', image=userIcon, compound=LEFT, bg='white', border=0, command=logOut)
        btnLogOut.place(x=10, y=410, height=35)

        root.mainloop()



class StudentHomeForm:
    btnTakeAssignmentState = 'normal'
    btnViewGradeState = 'normal'

    def main_screen():
        # Whenever you open StudentHomeForm page
        exists, open, id, rel, end, easy, med, hard = Logic.AssignmentUtility.assignmentExistsAndOpen()          
        if exists:
            assignment = Logic.Assignment(id, rel, end, easy, med, hard)
            global studentAssignment
            studentAssignment = Logic.StudentAssignment(assignment, user) # create a student assignment object

            if open: # if assignment is open
                StudentHomeForm.btnViewGradeState = 'disabled' # students can't see marks until assignment close date
                if studentAssignment.assignmentTaken(): # already been taken by student
                    StudentHomeForm.btnTakeAssignmentState = 'disabled'
                else: # not yet taken by student
                    StudentHomeForm.btnTakeAssignmentState = 'normal'
            else: # If assignment closed
                StudentHomeForm.btnTakeAssignmentState = 'disabled'
                StudentHomeForm.btnViewGradeState = 'normal'

        else: # if no assignments have ever been made yet
            StudentHomeForm.btnTakeAssignmentState = 'disabled'
            StudentHomeForm.btnViewGradeState = 'disabled'        


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Home Page")
        root.resizable(False,False)

    
        # Log out and return to sign in screen
        def logOut():
            result = messagebox.askokcancel("Log out","Are you sure you want to log out of your profile")
            if (result):
                messagebox.showinfo('','Logged out')
                root.destroy()
                LoginForm.main_screen()
        
        # Go to Create an assignment form
        def takeAssignment():
            root.destroy()
            TakeAssignmentForm.main_screen()
        
        # Go to View grades form
        def viewGrades():
            root.destroy()
            AssignmentFeedbackForm.main_screen()

        # Go to Practice assignment form
        def takePracticeAssignment():
            result = ""
            invalidInput = True
            while (invalidInput):
                result = askstring("Enter number of questions","Enter the number of easy, medium and hard questions (seperated by a space)")
                if result == None:
                    return
                try:
                    li = result.split(' ')
                    TakePracticeAssignmentForm.easy = int(li[0])
                    TakePracticeAssignmentForm.medium = int(li[1])
                    TakePracticeAssignmentForm.hard = int(li[2])
                except:
                    invalidInput = True  
                    messagebox.showinfo('Invalid input','Please enter the number of easy, medium and hard questions (seperated by a space)\nExample: 5 0 3')
                    continue
                if (TakePracticeAssignmentForm.easy <= Logic.AssignmentUtility.noTotalQuestions(1) and TakePracticeAssignmentForm.medium <= Logic.AssignmentUtility.noTotalQuestions(2) and TakePracticeAssignmentForm.hard <= Logic.AssignmentUtility.noTotalQuestions(3)):
                    invalidInput = False
                else:
                    invalidInput = True
                    messagebox.showinfo('Invalid input','There are a max of {0} easy, {1} medium\nand {2} hard questions'.format(Logic.AssignmentUtility.noTotalQuestions(1), Logic.AssignmentUtility.noTotalQuestions(2), Logic.AssignmentUtility.noTotalQuestions(3)))

            root.destroy()
            TakePracticeAssignmentForm.main_screen()


        # Create frame for image
        frameImg = Frame(root, width=425, height=450, bg='white')
        frameImg.place(relx=0.5, y=0)
        img = ImageTk.PhotoImage(Image.open("StudentBackground.png").resize((420,450)))
        Label(frameImg, image= img).pack()   # Label Widget to display Image

        # Create a frame for left side
        frame = Frame(root, width=425, height=450, bg='white')
        frame.place(x=0, y=0)
        
        # Create a frame for the buttons
        frameButtons = Frame(frame, width=425, height=200, bg='white')
        frameButtons.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Add widgets
        heading = Label(frame, text='Welcome ' + user.getFname(), bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        heading.place(relx=0.5, y=100, anchor=CENTER)

        # View Grades and Take Assignment buttons
        btnTakeAssignment = Button(frameButtons , text='Take Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), state=StudentHomeForm.btnTakeAssignmentState, command=takeAssignment)
        btnTakeAssignment.place(relx=0.5, y=40, width=250, height=35, anchor=CENTER)
        
        btnViewGrade = Button(frameButtons , text='View Grade', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), state=StudentHomeForm.btnViewGradeState, command=viewGrades)
        btnViewGrade.place(relx=0.5, y=100, width=250, height=35, anchor=CENTER)

        btnTakePracticeAssignment = Button(frameButtons , text='Take Practice Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',15), command=takePracticeAssignment)
        btnTakePracticeAssignment.place(relx=0.5, y=160, width=250, height=35, anchor=CENTER)

        # Creating a photoimage object for logout button
        userIcon = PhotoImage(file = r"userIcon.png")
        userIcon = userIcon.subsample(12, 12) # Resizing image to fit on button
        
        # Log out button
        btnLogOut = Button(frame, text='Log Out', image=userIcon, compound=LEFT, bg='white', border=0, command=logOut)
        btnLogOut.place(x=10, y=410, height=35)

        root.mainloop()



class CreateAssignmentForm:
    def main_screen():
        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Create Assignment")
        root.resizable(False,False)


        # Function to submit created assignment, generate assignments for students, then change screens 
        def submitAssignment():            
            # Ensure all fields are entered
            if (entRelDate.get() == '' or entEndDate.get() == '' or (spnBoxEasy.get() == '0' and spnBoxMed.get() == '0' and spnBoxHard.get() == '0')):
                messagebox.showinfo('Incomplete Information','Please enter all required information')
            else:
                # Ensure date is entered in correct format
                try:
                    dateObject = datetime.strptime(entRelDate.get(), "%Y-%m-%d %H:%M")
                    dateObject2 = datetime.strptime(entEndDate.get(), "%Y-%m-%d %H:%M")
                    print(dateObject, dateObject2)
                except ValueError:
                    messagebox.showinfo("Incorrect date format", "Date format should be YYYY-MM-DD HH:MM") # If the date validation goes wrong
                    return

                # Confirm submit        
                if (messagebox.askokcancel("Create Assignment","Are you sure you want to submit the assignment?")):
                    Logic.AssignmentUtility.createAssignment(entRelDate.get(), entEndDate.get(), int(spnBoxEasy.get()), int(spnBoxMed.get()), int(spnBoxHard.get())) # create this new assignment                
                    messagebox.showinfo('','Assignment succesfully created!')
                    # Change screens
                    root.destroy()
                    LecturerHomeForm.main_screen()

        # Go back to previous form function
        def Back():
            # Confirm submit        
            if (messagebox.askokcancel("Exit","Are you sure you want to cancel assignment creation?")):
                # Change screens
                root.destroy()
                LecturerHomeForm.main_screen()


        # Create a frame for left side
        frameLeft = Frame(root, width=425, height=450, bg='white')
        frameLeft.place(x=0, y=0)
        # Create a frame for right side
        frameRight = Frame(root, width=425, height=450, bg='#f9f9f9')
        frameRight.place(relx=0.5, y=0)

        # Heading
        headingRight = Label(frameRight, text='Create Assignment', bg='#f9f9f9', fg='#3BB9FF', font=('Arial',24,'bold'))
        headingRight.place(relx=0.5, rely=0.4, anchor=CENTER)
        headingLeft = Label(frameLeft, text='Enter assignment details', bg='white', fg='black', font=('Arial',15))
        headingLeft.place(relx=0.5, y=45, anchor=CENTER)

        # Widgets for Release and End Dates
        lblRelDate = Label(frameLeft, text='Release Date (YYYY-MM-DD HH:MM)', fg='#899499', bg='white', font=('Arial',13))
        lblRelDate.place(x=105, y=80)
        entRelDate = Entry(frameLeft)
        entRelDate.place(x=110, y=105, height=25)
        
        lblEndDate = Label(frameLeft, text='Close Date', fg='#899499', bg='white', font=('Arial',13))
        lblEndDate.place(x=105, y=135)
        entEndDate = Entry(frameLeft)
        entEndDate.place(x=110, y=160, height=25)

        # Widgets for Question Difficulties
        lblEasy = Label(frameLeft, text='Easy', fg='#899499', bg='white', font=('Arial',13))
        lblEasy.place(x=105, y=190)
        spnBoxEasy = Spinbox(frameLeft, from_= 0, to=Logic.AssignmentUtility.noTotalQuestions(1))
        spnBoxEasy.place(x=110, y=215, height=25)

        lblMed = Label(frameLeft, text='Medium', fg='#899499', bg='white', font=('Arial',13))
        lblMed.place(x=105, y=245)
        spnBoxMed = Spinbox(frameLeft, from_= 0, to=Logic.AssignmentUtility.noTotalQuestions(2))
        spnBoxMed.place(x=110, y=270, height=25)

        lblHard = Label(frameLeft, text='Hard', fg='#899499', bg='white', font=('Arial',13))
        lblHard.place(x=105, y=300)
        spnBoxHard = Spinbox(frameLeft, from_= 0, to=Logic.AssignmentUtility.noTotalQuestions(3))
        spnBoxHard.place(x=110, y=325, height=25)

        # Submit button
        btnSubmit = Button(frameLeft , text='Submit Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=submitAssignment)
        btnSubmit.place(relx=0.5, y=390, width=250, height=30, anchor=CENTER)

        # Create photoimage object for back button
        userIcon = PhotoImage(file = r"Back.png")
        userIcon = userIcon.subsample(25, 25) # Resizing image to fit on button
        
        # Back button
        btnBack = Button(frameLeft, text='Back', image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnBack.place(x=10, y=410, height=35)
 
        root.mainloop()



class ViewGradesForm:
    def main_screen():
        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Create Assignment")
        root.resizable(False,False)
        root.config(bg="white")


        # Go back to previous form function
        def Back():
            root.destroy()
            LecturerHomeForm.main_screen()

        # Show marks
        def show():
            # Clear output
            txtOutput.delete("1.0","end-1c")
            txtOutput.insert(END, "Student ID\tMark\n")

            minMark = 9999
            maxMark = -1
            totalMarksRecorded = 0
            markSum = 0
            # Fill the assignment marks in, calculating avg, min and max mark
            for mark in Logic.database.fetch("mark"):
                if (mark[0] == assignmentChosen.get()): # if assignment IDs match
                    if mark[2] > maxMark:
                        maxMark = mark[2]
                    if mark[2] < minMark:
                        minMark = mark[2]
                    markSum += mark[2]
                    totalMarksRecorded += 1
                    txtOutput.insert(END, mark[1] + "\t" + str(mark[2]) + "\n")
            
            # Fill in assignment stats
            if totalMarksRecorded != 0:
                lblAssignmentMin.config(text="Lowest Mark: " + str(minMark))
                lblAssignmentAverage.config(text="Average Mark: " + str(markSum / totalMarksRecorded))
                lblAssignmentMax.config(text="Highest Mark: " + str(maxMark))
            else:
                txtOutput.delete("1.0","end-1c")
                txtOutput.insert(END, "No student marks\nrecorded for this\nassignment")
                lblAssignmentMin.config(text="")
                lblAssignmentAverage.config(text="")
                lblAssignmentMax.config(text="")

        # Heading
        lblHeading = Label(root, text = "View Assignment Marks", bg='white', fg='#3BB9FF', font=('Arial',18,'bold'))
        lblHeading.place(relx=0.5, y=25, anchor=CENTER)
        lblSelectAssignment = Label(root, text = "Select assignment:", bg='white', fg='black', font=('Arial',11))
        lblSelectAssignment.place(x=230, y=70)

        # Load in information
        assignmentOptions = []
        for assignment in Logic.database.fetch('assignment'):
            assignmentOptions.append(assignment[0])
        
        assignmentChosen = IntVar() # Variable that stores selected drop down item 
        if len(assignmentOptions) != 0:
            assignmentChosen.set(assignmentOptions[-1]) # set this to the most recent assignment
        
        dropDown = OptionMenu(root, assignmentChosen, *assignmentOptions)
        dropDown.place(relx=0.5, y=80, height=35, width=50, anchor=CENTER)
        btnShowMarks = Button(root, text="Show Marks", bg='#3BB9FF', border=0, fg='white', font=('Arial',13), command=show)
        btnShowMarks.place(x=450, y=60, height=35, width=100)

        # Assignment marks
        lblAssignment = Label(root, text = "Assignment " + str(assignmentChosen.get()) + " marks", bg='white', fg='black', font=('Arial',14))
        lblAssignment.place(relx=0.5, y=150, anchor=CENTER)
        txtOutput = Text(root, fg='#3b3b3b', bg='white', border=1, font=('Arial',12))
        txtOutput.place(relx=0.5, y=230, width=150, height=100, anchor=CENTER)

        # Assignment stats
        statsFrame = Frame(root, bg='white')
        statsFrame.place(relx=0.5, y=360, anchor=CENTER, width=600, height=35)
        lblAssignmentMin = Label(statsFrame, bg='white', fg='#3BB9FF', font=('Arial',13))
        lblAssignmentMin.place(x=0)
        lblAssignmentAverage = Label(statsFrame, bg='white', fg='#3BB9FF', font=('Arial',13))
        lblAssignmentAverage.place(relx=0.5, y=9, anchor=CENTER)
        lblAssignmentMax = Label(statsFrame, bg='white', fg='#3BB9FF', font=('Arial',13))
        lblAssignmentMax.pack(anchor=E)
        
        # Create photoimage object for back button
        userIcon = PhotoImage(file = r"Back.png")
        userIcon = userIcon.subsample(25, 25) # Resizing image to fit on button
        # Back button
        btnBack = Button(root, text='Back', image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnBack.place(x=10, y=410, height=35)
       
        root.mainloop()



class TakeAssignmentForm:
    def main_screen():
        # Variables
        questionFormHeight = 290
        spaceBtwnQuestion = 20
        numQuestions = studentAssignment.assignment.getEasy() + studentAssignment.assignment.getMedium() + studentAssignment.assignment.getHard() # number of question for this specific assignment 
        arrEntries = [] # store the entry fields that students input answers into to access answers from each seperately
        arrSQLOutputs = [] # text widgets that sql outputs go into


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("SQL Assignment")
        root.resizable(False,False)
        root.configure(bg='white')


        # Functions - Submit and mark assignment function
        def submitAssignment():
            result = messagebox.askokcancel("Submit Assignment","Are you sure you want to submit your assignment answers?")
            if (result):
                messagebox.showinfo('','Assignment succesfully submitted!')
                # get the answers from all the entry fields
                arrAnswers = []
                for entry in arrEntries:
                    arrAnswers.append(entry.get())
                # then do all marking and stuff
                studentAssignment.setStudentAnswers(arrAnswers)
                studentAssignment.markAssignment()

                root.destroy()
                StudentHomeForm.main_screen()

        # Execute SQL Statement and display output
        def executeSQLStatement(questionNo):
            arrSQLOutputs[questionNo].delete("1.0","end")
            # If valid SQL statement entered
            if (Logic.database.executeStatment(arrEntries[questionNo].get()) != "error"):
                for line in Logic.database.executeStatment(arrEntries[questionNo].get()):
                    if len(line) != 1: # if it's not a calculation that gives a single answer
                        for cell in line:
                            try:
                                arrSQLOutputs[questionNo].insert(END, "{}, ".format(cell))
                            except:
                                arrSQLOutputs[questionNo].insert(END, ", ")
                        arrSQLOutputs[questionNo].insert(END, "\n")
                    else: # if it's a calculation that gives a single answer
                        arrSQLOutputs[questionNo].insert(END,"{}\n".format(line[0]))
            # If invalid SQL statement entered
            else:
                arrSQLOutputs[questionNo].insert(END, "Invalid SQL statement")


        # Layout Needed for Scrollbar
        main_frame = Frame(root) # create main frame
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas = Canvas(main_frame) # create a canvas
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)     # add scrollbar to canvas
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set) # configure canvas
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, bg='white', height=(questionFormHeight+spaceBtwnQuestion)*numQuestions + 240, width=800) #create another Frame inside canvas
        my_canvas.create_window(0,0, window=second_frame, anchor="nw")

        # Heading
        headingAssignment = Label(second_frame, text='SQL Assignment', bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        headingAssignment.place(relx=0.5, y=30, anchor=CENTER)
        subHeading = Label(second_frame, text=str(numQuestions) + ' Questions', bg='white', fg='#899499', font=('Arial',15,)) # make numQuestions rather assignment.questions.length() when we create assignment class
        subHeading.place(relx=0.5, y=70, anchor=CENTER)

        # Loading in Questions
        questionNo = 0 # keep track of question number
    
        for question in studentAssignment.getQuestions():  
            # Frame that holds the full question
            frameQuestion = Frame(second_frame, width=700, height=questionFormHeight, bg='#f9f9f9')
            frameQuestion.place(relx=0.5, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion), anchor=CENTER)
            
            # Display question number and question
            lblQuestionNumber = Label(frameQuestion, text='Question ' + str(questionNo+1), fg='#3BB9FF', bg='#f9f9f9', font=('Arial',15))
            lblQuestionNumber.place(x=20, y=15)
            lblQuestion = Text(frameQuestion, fg='black', bg='#f9f9f9', border=0, font=('Arial',12))
            lblQuestion.place(x=25, y=45, width=600, height=45)
            lblQuestion.insert(END, question.getQuestion())
            
            # Input fields
            entAnswer = Entry(frameQuestion, fg='black', border=2, bg='white', font=('Arial',10))
            entAnswer.place(x=25, y=95, width=560, height=35)
            arrEntries.append(entAnswer) # store the input fields in an array
            
            # Run button
            btnRun = Button(frameQuestion, text='Run', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=partial(executeSQLStatement, questionNo))
            btnRun.place(x=630, y=110, width=70, height=25, anchor=CENTER)

            # SQL output text field
            lblOuput = Label(frameQuestion, text='SQL statement output:', fg='#3b3b3b', bg='#f9f9f9', font=('Arial',10))
            lblOuput.place(x=25, y=145)
            txtOutput = Text(frameQuestion, fg='#3b3b3b', bg='white', border=1, font=('Arial',10))
            txtOutput.place(x=25, y=170, width=600, height=100)
            arrSQLOutputs.append(txtOutput) # store the ouput fields in an array

            # Increment question number 
            questionNo += 1

        # Submit button
        btnSubmit = Button(second_frame , text='Submit Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=submitAssignment)
        btnSubmit.place(relx=0.76, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion) - 100, width=250, height=30, anchor=CENTER)
        
        root.mainloop()



class AssignmentFeedbackForm:
    def main_screen():
        # Variables
        questionFormHeight = 350
        spaceBtwnQuestion = 20
        numQuestions = studentAssignment.assignment.getEasy() + studentAssignment.assignment.getMedium() + studentAssignment.assignment.getHard() # number of question for this specific assignment 


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Assignment Feedback")
        root.resizable(False,False)
        root.configure(bg='white')


        # Go back to previous form function
        def Back():
            root.destroy()
            StudentHomeForm.main_screen()


        # Layout Needed for Scrollbar
        main_frame = Frame(root) # create main frame
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas = Canvas(main_frame) # create a canvas
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)     # add scrollbar to canvas
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set) # configure canvas
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, bg='white', height=(questionFormHeight+spaceBtwnQuestion)*numQuestions + 180, width=800) #create another Frame inside canvas
        my_canvas.create_window(0,0, window=second_frame, anchor="nw")

        # Heading
        headingAssignment = Label(second_frame, text='Assignment Feedback', bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        headingAssignment.place(relx=0.5, y=30, anchor=CENTER)
        subHeading = Label(second_frame,text='Mark: ' + str(studentAssignment.mark), bg='white', fg='#899499', font=('Arial',15,)) # make numQuestions rather assignment.questions.length() when we create assignment class
        subHeading.place(relx=0.5, y=70, anchor=CENTER)

        # Loading in Questions
        questionNo = 0 # keep track of question number
        
            
        if len(studentAssignment.studentAnswers)!=0:    
            for question in studentAssignment.getQuestions(): 
                # Frame that holds the full question
                frameQuestion = Frame(second_frame, width=700, height=questionFormHeight, bg='#f9f9f9')
                if questionNo == 0:
                    frameQuestion.place(relx=0.5, y=300, anchor=CENTER)
                else:
                    frameQuestion.place(relx=0.5, y=(questionNo)*(questionFormHeight+spaceBtwnQuestion) + 300, anchor=CENTER)
                # Naswer correctness determines color
                if (studentAssignment.marks[questionNo]): # if correct answer
                    correctColor = '#F3FFF3'
                else:
                    correctColor = '#FFE7E7'

                frameQuestion.configure(bg=correctColor)
                
                # Display question number and question
                lblQuestionNumber = Label(frameQuestion, text='Question ' + str(questionNo+1), fg='#3BB9FF', bg=correctColor, font=('Arial',13))
                lblQuestionNumber.place(x=13, y=20)
                lblQuestion = Text(frameQuestion, fg='black', bg='#f9f9f9', border=0, font=('Arial',12), yscrollcommand=True)
                lblQuestion.place(x=25, y=45, width=600, height=45)
                lblQuestion.insert(END, question.getQuestion())
                
                # Input fields
                lblStudentAnswer = Label(frameQuestion, text='Your answer:', wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
                lblStudentAnswer.place(x=15, y=75, width=680, height=20)
                lblStudentAnswer = Label(frameQuestion, text=studentAssignment.studentAnswers[questionNo], wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13))
                lblStudentAnswer.place(x=15, y=95, width=680, height=45)
                lblCorrectAnswer = Label(frameQuestion, text='Correct answer:', wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
                lblCorrectAnswer.place(x=15, y=135, width=680, height=20)
                lblCorrectAnswer = Label(frameQuestion, text=question.getAnswer(), wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13))
                lblCorrectAnswer.place(x=15, y=155, width=680, height=45)

                # SQL output of student and correct statement
                lblStudentSQLOutput = Label(frameQuestion, text='Your SQL statement produced:', anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
                lblStudentSQLOutput.place(x=15, y=225, width=320, height=20)
                lblCorrectSQLOutput = Label(frameQuestion, text='The correct SQL statement produced:', anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
                lblCorrectSQLOutput.place(x=365, y=225, width=320, height=20)

                txtStudentSQLOutput = Text(frameQuestion, fg='#36454F', bg='#f9f9f9', border=0, font=('Arial',12))
                txtStudentSQLOutput.place(x=15, y=250, width=320, height=80)
                txtCorrectSQLOutput = Text(frameQuestion, fg='#36454F', bg='#f9f9f9', border=0, font=('Arial',12))
                txtCorrectSQLOutput.place(x=365, y=250, width=320, height=80)

                # Fill Text widget with outputs from student SQL statements
                if (studentAssignment.studentAnswers[questionNo] != ""):
                    studentSQLOutput = Logic.database.executeStatment(studentAssignment.studentAnswers[questionNo])
                    if (studentSQLOutput != "error"):
                        print(studentSQLOutput)
                        for line in studentSQLOutput:
                            if len(line) != 1: # if it's not a calculation that gives a single answer
                                for cell in line:
                                    try:
                                        txtStudentSQLOutput.insert(END, "{}, ".format(cell))
                                    except:
                                        txtStudentSQLOutput.insert(END, ", ")
                                txtStudentSQLOutput.insert(END, "\n")
                            else: # if it's a calculation that gives a single answer
                                txtStudentSQLOutput.insert(END,"{}\n".format(line[0]))
                    else:
                        txtStudentSQLOutput.insert(END, "Invalid SQL statement")
                txtStudentSQLOutput.config(state='disabled')

                # Fill Text widget with outputs from correct SQL statements
                if (question.getAnswer() != ""):
                    correctSQLOutput = Logic.database.executeStatment(question.getAnswer())
                    if (correctSQLOutput != "error"):
                        for line in correctSQLOutput:
                            print(line)
                            if len(line) != 1: # if it's not a calculation that gives a single answer
                                for cell in line:
                                    print(cell)
                                    try:
                                        txtCorrectSQLOutput.insert(END, "{}, ".format(cell))
                                    except:
                                        txtCorrectSQLOutput.insert(END, ", ")
                                txtCorrectSQLOutput.insert(END, "\n")
                            else: # if it's a calculation that gives a single answer
                                txtCorrectSQLOutput.insert(END,"{}\n".format(line[0]))
                    else:
                        txtCorrectSQLOutput.insert(END, "Invalid SQL statement")
                txtCorrectSQLOutput.config(state='disabled')


                # Increment question number 
                questionNo += 1
        else:
            userIcon = PhotoImage(file = r"Home.png")
            userIcon = userIcon.subsample(1, 1) # Resizing image to fit on button
            
            # Home button
            btnHome = Button(second_frame, image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
            btnHome.place(x=20, y=20)
            lblFeedback = Label(text="Feedback not available. No assignment submitted.", bg='white', fg='#899499', font=('Arial',12))
            lblFeedback.place(relx=0.5, y=100, anchor=CENTER)
            root.mainloop()
            return
            

        # Create photoimage for home button
        userIcon = PhotoImage(file = r"Home.png")
        userIcon = userIcon.subsample(1, 1) # Resizing image to fit on button
        
        # Home button
        btnHome = Button(second_frame, image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnHome.place(x=20, y=20)
        btnHome = Button(second_frame, text='Home', image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnHome.place(x=15, y=(questionNo)*(questionFormHeight+spaceBtwnQuestion) + 130)
        
        root.mainloop()



class TakePracticeAssignmentForm:
    easy = 0
    medium = 0
    hard = 0
    practiceAssignment : Logic.StudentPracticeAssignment
    numQuestions = 0
    
    def main_screen():
        # Variables
        TakePracticeAssignmentForm.practiceAssignment = Logic.StudentPracticeAssignment(TakePracticeAssignmentForm.easy, TakePracticeAssignmentForm.medium, TakePracticeAssignmentForm.hard)
        questionFormHeight = 290
        spaceBtwnQuestion = 20
        TakePracticeAssignmentForm.numQuestions = TakePracticeAssignmentForm.easy + TakePracticeAssignmentForm.medium + TakePracticeAssignmentForm.hard # number of question for this specific assignment 
        arrEntries = [] # store the entry fields that students input answers into to access answers from each seperately
        arrSQLOutputs = [] # text widgets that sql outputs go into


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Practice SQL Assignment")
        root.resizable(False,False)
        root.configure(bg='white')


        # Functions - Submit and mark assignment function
        def submitAssignment():
            result = messagebox.askokcancel("Submit Assignment","Are you sure you want to submit your practice assignment answers?")
            if (result):
                messagebox.showinfo('','Practice assignment succesfully submitted!')
                # get the answers from all the entry fields
                arrAnswers = []
                for entry in arrEntries:
                    arrAnswers.append(entry.get())
                
                # then do all marking and stuff
                TakePracticeAssignmentForm.practiceAssignment.setStudentAnswers(arrAnswers)
                TakePracticeAssignmentForm.practiceAssignment.markAssignment()
                PracticeAssignmentFeedbackForm.numQuestions = TakePracticeAssignmentForm.practiceAssignment.easy + TakePracticeAssignmentForm.practiceAssignment.medium + TakePracticeAssignmentForm.practiceAssignment.hard

                root.destroy()
                # Instead show a practice assignment feedback page
                PracticeAssignmentFeedbackForm.main_screen()

        # Execute SQL Statement and display output
        def executeSQLStatement(questionNo):
            arrSQLOutputs[questionNo].delete("1.0","end")
            # If valid SQL statement entered
            if (Logic.database.executeStatment(arrEntries[questionNo].get()) != "error"):
                for line in Logic.database.executeStatment(arrEntries[questionNo].get()):
                    if len(line) != 1: # if it's not a calculation that gives a single answer
                        for cell in line:
                            try:
                                arrSQLOutputs[questionNo].insert(END, "{}, ".format(cell))
                            except:
                                arrSQLOutputs[questionNo].insert(END, ", ")
                        arrSQLOutputs[questionNo].insert(END, "\n")
                    else: # if it's a calculation that gives a single answer
                        arrSQLOutputs[questionNo].insert(END,"{}\n".format(line[0]))    
            # If invalid SQL statement entered
            else:
                arrSQLOutputs[questionNo].insert(END, "Invalid SQL statement")

        # Go back to previous form function
        def Back():
            # Confirm submit        
            if (messagebox.askokcancel("Exit","Are you sure you want to end practice assignment?\nYou will lose all progress")):
                # Change screens
                root.destroy()
                StudentHomeForm.main_screen()


        # Layout Needed for Scrollbar
        main_frame = Frame(root) # create main frame
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas = Canvas(main_frame) # create a canvas
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview) # add scrollbar to canvas
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set) # configure canvas
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, bg='white', height=(questionFormHeight+spaceBtwnQuestion)*TakePracticeAssignmentForm.numQuestions + 240, width=800) #create another Frame inside canvas
        my_canvas.create_window(0,0, window=second_frame, anchor="nw")

        # Heading
        headingAssignment = Label(second_frame, text='SQL Practice Assignment', bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        headingAssignment.place(relx=0.5, y=30, anchor=CENTER)
        subHeading = Label(second_frame, text=str(TakePracticeAssignmentForm.numQuestions) + ' Questions', bg='white', fg='#899499', font=('Arial',15,)) # make numQuestions rather assignment.questions.length() when we create assignment class
        subHeading.place(relx=0.5, y=70, anchor=CENTER)

        # Loading in Questions
        questionNo = 0 # keep track of question number
    
        for question in TakePracticeAssignmentForm.practiceAssignment.getQuestions():  
            # Frame that holds the full question
            frameQuestion = Frame(second_frame, width=700, height=questionFormHeight, bg='#f9f9f9')
            frameQuestion.place(relx=0.5, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion), anchor=CENTER)
            
            # Display question number and question
            lblQuestionNumber = Label(frameQuestion, text='Question ' + str(questionNo+1), fg='#3BB9FF', bg='#f9f9f9', font=('Arial',15))
            lblQuestionNumber.place(x=20, y=15)
            lblQuestion = Text(frameQuestion, fg='black', bg='#f9f9f9', border=0, font=('Arial',12))
            lblQuestion.place(x=25, y=45, width=600, height=45)
            lblQuestion.insert(END, question.getQuestion())
            
            # Input fields
            entAnswer = Entry(frameQuestion, fg='black', border=2, bg='white', font=('Arial',10))
            entAnswer.place(x=25, y=95, width=560, height=35)
            arrEntries.append(entAnswer) # store the input fields in an array
            
            # Run button
            btnRun = Button(frameQuestion, text='Run', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=partial(executeSQLStatement, questionNo))
            btnRun.place(x=630, y=110, width=70, height=25, anchor=CENTER)

            # SQL output text field
            lblOuput = Label(frameQuestion, text='SQL statement output:', fg='#3b3b3b', bg='#f9f9f9', font=('Arial',10))
            lblOuput.place(x=25, y=145)
            txtOutput = Text(frameQuestion, fg='#3b3b3b', bg='white', border=1, font=('Arial',10))
            txtOutput.place(x=25, y=170, width=600, height=100)
            arrSQLOutputs.append(txtOutput) # store the ouput fields in an array

            # Increment question number 
            questionNo += 1

        # Submit button
        btnSubmit = Button(second_frame , text='Submit Assignment', bg='#3BB9FF', fg='white', border=0, font=('Arial',13,'bold'), command=submitAssignment)
        btnSubmit.place(relx=0.76, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion) - 100, width=250, height=30, anchor=CENTER)
        
        # Create photoimage object for back button
        userIcon = PhotoImage(file = r"Back.png")
        userIcon = userIcon.subsample(25, 25) # Resizing image to fit on button
        
        # Back button
        btnBack = Button(second_frame, text='Back', image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnBack.place(x=15, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion) - 110, height=35)

        root.mainloop()



class PracticeAssignmentFeedbackForm:
    def main_screen():
        # Variables
        questionFormHeight = 350
        spaceBtwnQuestion = 20


        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Assignment Feedback")
        root.resizable(False,False)
        root.configure(bg='white')


        # Go back to previous form function
        def Back():
            root.destroy()
            StudentHomeForm.main_screen()
            

        # Layout Needed for Scrollbar
        main_frame = Frame(root) # create main frame
        main_frame.pack(fill=BOTH, expand=1)

        my_canvas = Canvas(main_frame) # create a canvas
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview) # add scrollbar to canvas
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set) # configure canvas
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, bg='white', height=(questionFormHeight+spaceBtwnQuestion)*TakePracticeAssignmentForm.numQuestions + 160, width=800) #create another Frame inside canvas
        my_canvas.create_window(0,0, window=second_frame, anchor="nw")


        # Heading
        headingAssignment = Label(second_frame, text='Practice Assignment Feedback', bg='white', fg='#3BB9FF', font=('Arial',24,'bold'))
        headingAssignment.place(relx=0.5, y=30, anchor=CENTER)
        subHeading = Label(second_frame,text='Mark: ' + str(TakePracticeAssignmentForm.practiceAssignment.mark), bg='white', fg='#899499', font=('Arial',15,)) # make numQuestions rather assignment.questions.length() when we create assignment class
        subHeading.place(relx=0.5, y=70, anchor=CENTER)


        # Loading in Questions
        questionNo = 0 # keep track of question number
    
        for question in TakePracticeAssignmentForm.practiceAssignment.getQuestions(): 
            # Frame that holds the full question
            frameQuestion = Frame(second_frame, width=700, height=questionFormHeight, bg='#f9f9f9')
            if questionNo == 0:
                frameQuestion.place(relx=0.5, y=300, anchor=CENTER)
            else:
                frameQuestion.place(relx=0.5, y=(questionNo)*(questionFormHeight+spaceBtwnQuestion) + 300, anchor=CENTER)
            # Answer correctness determines color
            if (TakePracticeAssignmentForm.practiceAssignment.marks[questionNo]): # if correct answer
                correctColor = '#F3FFF3'
            else:
                correctColor = '#FFE7E7'

            frameQuestion.configure(bg=correctColor)
            
            # Display question number and question
            lblQuestionNumber = Label(frameQuestion, text='Question ' + str(questionNo+1), fg='#3BB9FF', bg=correctColor, font=('Arial',13))
            lblQuestionNumber.place(x=13, y=20)
            lblQuestion = Text(frameQuestion, fg='black', bg='#f9f9f9', border=0, font=('Arial',12))
            lblQuestion.place(x=25, y=45, width=600, height=30)
            lblQuestion.insert(END, question.getQuestion())
            
            # Input fields
            lblStudentAnswerHeading = Label(frameQuestion, text='Your answer:', wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
            lblStudentAnswerHeading.place(x=15, y=75, width=680, height=20)
            lblStudentAnswer = Text(frameQuestion, fg='black', bg=correctColor, border=0, font=('Arial',13))
            lblStudentAnswer.place(x=15, y=95, width=680, height=40)
            lblStudentAnswer.insert(END, TakePracticeAssignmentForm.practiceAssignment.studentAnswers[questionNo])
            lblCorrectAnswerHeading = Label(frameQuestion, text='Correct answer:', wraplength=680, anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
            lblCorrectAnswerHeading.place(x=15, y=135, width=680, height=20)
            lblCorrectAnswer = Text(frameQuestion, fg='black', bg=correctColor, border=0, font=('Arial',13))
            lblCorrectAnswer.place(x=15, y=155, width=680, height=40)
            lblCorrectAnswer.insert(END, question.getAnswer())

            # SQL output of student and correct statement
            lblStudentSQLOutput = Label(frameQuestion, text='Your SQL statement produced:', anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
            lblStudentSQLOutput.place(x=15, y=225, width=320, height=20)
            lblCorrectSQLOutput = Label(frameQuestion, text='The correct SQL statement produced:', anchor='nw', justify=LEFT, fg='black', bg=correctColor, font=('Arial',13,'bold'))
            lblCorrectSQLOutput.place(x=365, y=225, width=320, height=20)

            txtStudentSQLOutput = Text(frameQuestion, fg='#36454F', bg='#f9f9f9', border=0, font=('Arial',12))
            txtStudentSQLOutput.place(x=15, y=250, width=320, height=80)
            txtCorrectSQLOutput = Text(frameQuestion, fg='#36454F', bg='#f9f9f9', border=0, font=('Arial',12))
            txtCorrectSQLOutput.place(x=365, y=250, width=320, height=80)

            # Fill Text widget with outputs from student SQL statements
            if (TakePracticeAssignmentForm.practiceAssignment.studentAnswers[questionNo] != ""):
                studentSQLOutput = Logic.database.executeStatment(TakePracticeAssignmentForm.practiceAssignment.studentAnswers[questionNo])
                if (studentSQLOutput != "error"):
                    print(studentSQLOutput)
                    for line in studentSQLOutput:
                        if len(line) != 1: # if it's not a calculation that gives a single answer
                            for cell in line:
                                try:
                                    txtStudentSQLOutput.insert(END, "{}, ".format(cell))
                                except:
                                    txtStudentSQLOutput.insert(END, ", ")
                            txtStudentSQLOutput.insert(END, "\n")
                        else: # if it's a calculation that gives a single answer
                            txtStudentSQLOutput.insert(END,"{}\n".format(line[0]))
                else:
                    txtStudentSQLOutput.insert(END, "Invalid SQL statement")
            txtStudentSQLOutput.config(state='disabled')

            # Fill Text widget with outputs from correct SQL statements
            if (question.getAnswer() != ""):
                correctSQLOutput = Logic.database.executeStatment(question.getAnswer())
                if (correctSQLOutput != "error"):
                    for line in correctSQLOutput:
                        print(line)
                        if len(line) != 1: # if it's not a calculation that gives a single answer
                            for cell in line:
                                print(cell)
                                try:
                                    txtCorrectSQLOutput.insert(END, "{}, ".format(cell))
                                except:
                                    print("Must be a missing entry or weird datatype")
                                    txtCorrectSQLOutput.insert(END, ", ")
                            txtCorrectSQLOutput.insert(END, "\n")
                        else: # if it's a calculation that gives a single answer
                            txtCorrectSQLOutput.insert(END,"{}\n".format(line[0]))
                else:
                    txtCorrectSQLOutput.insert(END, "Invalid SQL statement")
            txtCorrectSQLOutput.config(state='disabled')

            # Increment question number 
            questionNo += 1


        # Create photoimage for home button
        userIcon = PhotoImage(file = r"Home.png")
        userIcon = userIcon.subsample(1, 1) # Resizing image to fit on button
        
        # Home button
        btnHome = Button(second_frame, image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnHome.place(x=20, y=20)
        btnHome = Button(second_frame, text='Home', image=userIcon, compound=LEFT, bg='white', border=0, command=Back)
        btnHome.place(x=15, y=(questionNo+1)*(questionFormHeight+spaceBtwnQuestion) - 100)
        
        root.mainloop()



class Auto_Generation:
    def main_screen():
        # Main root window
        root = Tk() # create GUI window 
        root.geometry("800x450") # configuration of window 
        root.title("Question Generation")
        root.resizable(TRUE,TRUE)
        root.configure(bg='white')


        # Variables
        arrtables=[]
        arrcolumns=[]
        exclamation_replacements=[] 
        # Define arrays for replacement strings       
        combo1=[]
        combinations=[] # Initialize an empty list to store combinations
        underscore_replacements=[]
        exclamation_replacements=arrcolumns # Initialize a set to keep track of used exclamation replacements


        # Functions
        def replace_characters(input_str, index, current_str, combinations, used_exclamation):
            # If we've processed the entire string, add the current_str to combinations            
            if index==len(input_str):
                combinations.append(current_str)
                return   
                     
            # If the current character is '_', replace it with each replacement
            if input_str[index]=='_':                
                for replacement in underscore_replacements:
                    replace_characters(input_str,index+1,current_str+replacement,combinations,used_exclamation)
            # If the current character is '!', replace it with unused replacements
            elif input_str[index]=='!':
                for replacement in exclamation_replacements:
                    if replacement not in used_exclamation:
                        used_exclamation.add(replacement) #markk as used
                        replace_characters(input_str,index+1,current_str+replacement,combinations,used_exclamation)
                        used_exclamation.remove(replacement)           # Unmark the replacement when backtracking             
            else:# If it's any other character, keep it as is
                replace_characters(input_str,index+1,current_str+input_str[index],combinations,used_exclamation)
            
        def get_tables():
            tabs=Logic.QuestionsUtility.getTables()
            #arrtables=[tabs.__sizeof__]
            for i in tabs:
                i=str(i)
                i=i[:-3]
                i=i[2:]
                arrtables.append(i)
                # print(i)
            
        def get_cols(tablename):            
            data=Logic.QuestionsUtility.getTableName(tablename)
            for column in data.description:
            #print(column[0])
            #arrcolumns*=0
                arrcolumns.append(column[0])

        def Take_input():            
            if questiontxt.get("1.0","end-1c")=="" or answertxt.get("1.0","end-1c")=="":
                messagebox.showinfo('','Please fill in both your answer and question.')
                return
            
            btnDisplay['state'] = DISABLED
            spnBoxLevel['state'] = DISABLED
            questiontxt['state'] = DISABLED
            answertxt['state'] = DISABLED
            btnDelete['state'] = NORMAL
            print(Logic.QuestionsUtility.getTables())
            get_tables()
            #print(arrcolumns)
            user_input = questiontxt.get("1.0", "end-1c")
            answer_input=answertxt.get("1.0","end-1c")
            #combo1=[]                
            print(arrtables)   
            # Initialize an empty list to store combinations
            #combinations = []
            # Initialize a set to keep track of used exclamation replacements
            used_exclamation = set()
            i=-1
            for y in arrtables:
                #print(y)
                i+=1
                del arrcolumns[:]
                del underscore_replacements[:]
                get_cols(y)
                underscore_replacements.append(arrtables[i])
                #global exclamation_replacements
                #exclamation_replacements=arrcolumns
                #global exclamation_replacements
                #exclamation_replacements=arrcolumns
                replace_characters(user_input, 0, "", combinations, used_exclamation)
                replace_characters(answer_input,0, "", combo1, used_exclamation)
                #Output.insert(END, combinations)
                #sOut=""
                #print("Hello")
                #print(combinations)
                #print(combo1)
            for i in range(0,len(combinations), 1):
                Output.insert(END,f"Combination {i}: Question: {combinations[i]} Answer: {combo1[i]} \n")
                print(f"Combination {i}: Question: {combinations[i]} Answer: {combo1[i]}")
        
        #Output.insert(END,sOut)
        def delete_list():            
            user_input = cList.get("1.0","end-1c")
            # Split the input string into a list of integers
            input_list = [int(x.strip()) for x in user_input.split(',')]
            # Create an array (list) with some initial values
            # original_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            input_list.sort(reverse=True)
            # original_array=combinations
            # Delete elements from the original array at specified positions
            for position in input_list:
                if 0 <= position < len(combinations):
                #del original_array[position]
                    del combinations[position]
                    del combo1[position]
            # Print the modified array
            #print("Modified Array:", original_array)
            Output.delete("1.0","end-1c")
            for i in range(0,len(combinations), 1):
               Output.insert(END,f"Combination {i}: Question: {combinations[i]} Answer: {combo1[i]} \n")

        def submit_questions():
            print(spnBoxLevel.get())
            id=Logic.QuestionsUtility.getLastQuestion(int(spnBoxLevel.get()))
            print(id)
            x=(id[0])
            s=str(x)        
            s=s[1:-1]   
            y = [(b.strip()) for b in s.split(',')]
            iid=int(y[0])
            if (messagebox.askokcancel("Generate Questions","Are you sure you want to submit these combinations?")):                
                for i in range(0,len(combinations),1):
                    iid+=1
                    Logic.QuestionsUtility.createQuestions(iid,int(spnBoxLevel.get()),combinations[i],combo1[i]) # add this new question to the database              
                    
                # Change screens
                messagebox.showinfo('','Questions succesfully added!')
                root.destroy()
                LecturerHomeForm.main_screen()
            
        def exitBack():
            if (messagebox.askokcancel("Generate Questions","Are you sure you want to exit? None of the combinations will be saved.")):
                root.destroy()
                LecturerHomeForm.main_screen()
        

        # Heading
        lblHeading = Label(root, text = "Assignment Question Generation", bg='white', fg='#3BB9FF', font=('Arial',18,'bold'))
        lblHeading.place(relx=0.5, y=25, anchor= CENTER)

        # Statement generation input
        q1 = Label(root, text = "Question:", bg='white', fg='black', font=('Arial', 11))
        q1.place(x=15, y=50)
        q2 = Label(root, text = "Input the question, where '!' denotes the column name and '_' denotes the table name", anchor='w', bg='white', fg='#899499', font=('Arial', 11))
        q2.place(x=15, height=25, width=600, y=70)
        questiontxt = Text(root, bg = "light yellow")
        questiontxt.place(x=15, height=25, width = 600, y=95)
        
        a1 = Label(root, text = "Answer:", bg='white', fg='black', font=('Arial', 11))
        a1.place(x=15, y=125)
        a2 = Label(root, text="Input the SQL answer, where '!' denotes the column name and '_' denotes the table name", anchor='w', bg='white', fg='#899499', font=('Arial', 11))
        a2.place(x=15, height=25, width=600, y=145)
        answertxt = Text(root, bg = "light yellow")
        answertxt.place(x=15, height=25, width=600, y=170)

        lblLevel = Label(text="Select question difficulty:", bg='white', fg='#899499', font=('Arial',10), wraplength=150)
        lblLevel.place(x=630, y=90, width=150)
        spnBoxLevel = Spinbox(root, from_= 1, to=3) 
        spnBoxLevel.place(x=630, y=120, width=30)
        btnDisplay = Button(root, text ="Generate", bg='#3BB9FF', border=0, fg='white', font=('Arial',13), command = lambda:Take_input())
        btnDisplay.place(x=630, y=160, width=100, height=35)

        # Statement generation output
        lblOutput = Label(root, text="Generated combinations:", bg='white', fg='#3BB9FF', font=('Arial',12))
        lblOutput.place(x=15, y=200)   
        Output = Text(root, bg = "light cyan")
        Output.place(x=15, y=230, width=700, height=130)

        # Delete specific generations
        lblDelete = Label(text="Enter a comma separated list to delete any of the generated combinations:", bg='white', fg='#899499', font=('Arial',12))
        lblDelete.place(x=15,y=370)
        cList = Text(root, bg = "light cyan")
        cList.place(x=15, y=400, height=25, width = 400)  
        btnDelete = Button(root, text="Delete Questions", bg='#3BB9FF', fg='white', border=0, font=('Arial',9), state=DISABLED, command=lambda:delete_list())
        btnDelete.place(x=430, y=400, width=100, height=25)

        # Save combinations and exit
        lblCreateExit = Label(text="Click to add questions to the database", bg='white', fg='#3BB9FF', wraplength=130, font=('Arial',9))
        lblCreateExit.place(x=660, y=365, width=130)
        btnCreateExit = Button(root, text="Create and Exit", bg='#3BB9FF', fg='white', border=0, font=('Arial',11), command=lambda:submit_questions())
        btnCreateExit.place(x=665, y=405, width=120, height=35)     
    
        btnExit = Button(root,height=2,width=7,text="Exit",bg='#3BB9FF',border=0,fg='white',command=lambda:exitBack(),padx=5,pady=0) 
        btnExit.place(x=0,y=0) 
        
        mainloop()
        


class SingleAddition:
    def main_screen():
        # Main root window
        root = Tk()
        root.geometry("500x400")
        root.title(" Question Creation ")
        root.configure(bg='white')      


        # Variables  
        combinations=[]
        combo1=[]
        combo2=[]


        # Functions
        def add_question():
            # cursor
            if questiontxt.get("1.0","end-1c")=="" or answertxt.get("1.0","end-1c")=="":
                messagebox.showinfo('','Question and answer cannot be left empty')
                return
            
            question_input=questiontxt.get("1.0","end-1c")
            answer_input=answertxt.get("1.0","end-1c")
            level_input=int(spnBoxLevel.get())

            combinations.append(question_input)
            combo1.append(answer_input)
            combo2.append(level_input)

            questiontxt.delete("1.0","end-1c")
            answertxt.delete("1.0","end-1c")
            print(combinations)
            print(combo1)
            print(combo2)
        
        def add_questions():
            #id=0
            if questiontxt.get("1.0","end-1c")!="" or answertxt.get("1.0","end-1c")!="":
                messagebox.showinfo('','There is a combination which you have not added yet. Question and answer inputs need to be empty.')
                return
            if (messagebox.askokcancel("Create Questions","Are you sure you want to submit these combinations?")):
                for i in range(0, len(combinations),1):
                    id=Logic.QuestionsUtility.getLastQuestion(combo2[i])
                    x=(id[0])
                    s=str(x)
                    s=s[1:-1]   
                    y = [(b.strip()) for b in s.split(',')]
                    iid=int(y[0])                
                    Logic.QuestionsUtility.createQuestions(iid+1,combo2[i],combinations[i],combo1[i])
            messagebox.showinfo('','Questions succesfully added!')
            root.destroy()
            LecturerHomeForm.main_screen()
                
        def exitBack():
            if (messagebox.askokcancel("Generate Questions","Are you sure you want to exit? None of the combinations will be saved.")):
                root.destroy()
                LecturerHomeForm.main_screen()
            

        # Widgets
        l = Label(text = "Assignment Question Creation",bg='white', fg='#3BB9FF', font=('Arial',18,'bold'),padx=5,pady=5)
        l.pack()

        q=Label(text = "Input the question:",bg='white', fg='#3BB9FF', font=('Arial',15,),padx=10,pady=10)
        q.pack()
        questiontxt = Text(root, height = 2,width = 75,bg = "light yellow")
        questiontxt.pack()

        a=Label(text="Input the SQL answer:",bg='white', fg='#3BB9FF', font=('Arial',15),padx=10,pady=10)
        a.pack()
        answertxt = Text(root, height = 2,width = 75,bg = "light yellow")
        answertxt.pack()

        level=Label(text="Input the level of the question here:",bg='white', fg='#3BB9FF', font=('Arial',15),padx=10,pady=10)
        level.pack()
        spnBoxLevel = Spinbox(root, from_= 1, to=3)
        spnBoxLevel.pack()
        
        Display = Button(root, height = 2,width = 20,text ="Save and Exit", bg='#3BB9FF',fg='white',command = lambda:add_questions())
        Display.place(x=340,y=290)
        save_input=Button(root, height=2, width=20,text="Add combination", bg='#3BB9FF',fg='white', command=lambda:add_question())
        save_input.place(x=10,y=290)

        btnexit=Button(root,height=2,width=7,text="Exit",bg='#3BB9FF', border=0,fg='white',command=lambda:exitBack(),padx=5,pady=0)
        btnexit.place(x=0,y=0)
        
        mainloop()       


LoginForm.main_screen()