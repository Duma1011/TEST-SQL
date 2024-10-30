# TEST-SQL
### Developers:
- Phumezile Tsitsa
- Kane Gibson
- Alex Ikin
### Project Overview
TESTSQL is a comprehensive system that empowers second-year computer science lectures with tools necessary to create and automate SQL assignments for their database courses. The system streamlines the process of creating assignments by allowing lecturers to tailor assessments based on desired criteria. With the aid of an efficient database, the system will generate unique assignments for each student, ensuring fairness and combatting cheating. Additionally, the system includes an automatic grading component that evaluates and provides feedback to student submissions. This helps improve the overall efficiency and value of the SQL assignment management process at the UCT (University of Cape Town) (University of Cape Town) Computer Science department. 

### Functional Requirements
#### Data Input and Validation 
The only time new questions and answers will be added into the system database is through the lecture. When new questions are added into the system the instructor should ensure the English question and SQL statement answer corresponds and behave as expected. 

#### Data Retrieval and Display 
- Students should only be able to complete an assignment after the opening date but before the closing date. 
- Students should not be allowed to view the assignment answer before it has been closed and marked. 
- Assignments marks are only released once every student has submitted and the assignment has been closed. 
- The only data that will be visible to student at time they complete an assignment or practice test are English question and the data tables they are querying.

#### Error Handling and Logging 
Great importance and focus were placed on data input and validation. Invalid data, which is the cause of many errors, was pre-empted and prevented from even being inputted at the presentation layer level. The possibility of errors was therefore rare, and the need to handle errors was few and far between.  

#### User Training and Help Documentation 
The system will be accompanied by a user manual which should be read and understood by the user before they interact with the system. This is pre-training that the student and instructor must walk through to ensure they understand the system prior to interaction with it for the first time. See appendix B for user manual.

### Non-Functional Requirements 
#### Performance 
A specific system response time is not a requirement. However, for the sake of efficiency and user satisfaction, the system should take no longer than 10 seconds to evaluate SQL queries and generate feedback on a stable internet connection. It should upload and process lecturer information in under 5 seconds. The system must generate questions based on the inputted lecturer specifications in under 5 seconds per 100 students. 

#### Security 
To protect student data and information every system user is someone registered into the university with accredited student or staff number from the computer science department. Depending on the level of authority and individual has in the department they only will be granted access to data that pertains to their line of work and their interaction with the system to complete delegated department duties. Every user will then be required to have a password and username which will be used to determine how much system data they should be exposed to. 

#### Usability Requirements 

We have designed the user interface to be as simple as possible, making sure we only include necessary and important information on our screens, avoiding distractions and unnecessary complexity that would clutter users’ focus. I our design we have employed various UI design principles to make sure we build an easy-to-use software that increase students’ efficiency when completing assessments. 

#### Clarity:  
This system will be used by students while taking closed practical in the labs. We made sure to include descriptive button names and limit the information we show to a student to one question on a screen at a time only showing the tables they supposed to query, text box to written answers and the test button where they can test answer before submitting. All button names and content on screen is in English as it is the language of instruction in the institution. This is to allow ease system navigation allowing student to focus on what really matters under time constraints. 

#### Consistency:  
All buttons intended for the same functionality have the same color and size throughout the system and are only visible when the student needs to execute their functionality. This fosters familiarity which builds up as the user interacts with the system and builds ease of instruction execution increase productivity and reduce frustrations. 

#### Feedback:  
Each time a user executes an instruction that requires button click or any other user-system interaction they get a pop-up message on screen detailing the success or failure of their execution. The system then gives a discretion of the error and allows the user a chance to correct their deeds by either reentering information or restarting the execution from scratch depending on the depth of the error. This idea of instant feedback helps users understand the system’s response to their actions in real time, so they can correct their deeds. 

#### Simplicity:  
Information shown on a screen only pertains to a single instruction execution to avoid unnecessary content that can overwhelm users. This leads to easy navigation and clarity to steps to be taken to complete a task at hand, and it gives progress satisfaction to the user. 

#### Efficiency:  
The instruction-task separation in our UI design increases user productivity, by reducing destruction ensuring they can accomplish their tasks quickly and with minimal effort.  

#### Error Prevention:  
System user interface includes descriptive labels, provides warning in terms of user input type expected, and offers undo options. This reduces the likelihood of user errors. 

#### Compatibility:  
The system is built so that it can be compatible with the UCT Vula student site that is used for academic activities across the institution. 

#### User training:  
The system is accompanied by a clear and comprehensive user manual detailing system navigation from different user perspectives. This gives an overview of the task completion step for all the tasks that can be accomplished using the system. Students also get to practice questions with assignment similar structure to allow system familiarity before going for the main task, to make sure they know their way around the system they allow encouraged to complete these exercises. 

#### Availability: 
The system should be available to students to at least up to the end of semester when they are taking the database course. During this period students should be able to use the system whenever they need to practice or complete an assignment as part of course work.  

### Software Development Methodology 
Our software development process followed a test-driven approach, combining elements from both the waterfall and agile software development methodologies while incorporating SCRUM techniques. The project was divided into several distinct stages/iterations, each building upon the previous one. Every stage had its own predefined deliverables and typically spanned a one-week duration, apart from the implementation and testing stage, which lasted for a month. 

### Design Overview 

TESTSQL empowers second-year computer science lectures with tools necessary to create and automate SQL assignments for their database courses and provides student with a structured tool to exercise their SQL skills and allow them to complete course assessment. Whereby: 
- The system user can sign into the system.  
- The system allows lectures to tailor assessments based on desired criteria.  
- With the aid of an efficient database, the system generates unique assignments for each student, ensuring fairness.  
- Students can practice SQL with tailored questions that meet desired criteria. 
- Students can complete class assessments which have been allocated by the instructor. 
- The lecture and students can view grades of previous assignment.  
- The system includes an automatic grading component that evaluates and provides feedback to student submissions.

### Tools
- Python- Back-end
- Tkinter- Front-end
- SQL- Database
- Google Docks - Reporting


