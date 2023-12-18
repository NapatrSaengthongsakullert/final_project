# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

List Of Files

  1.Database.py
  
    1.)class Database
      -to save and update infomation
    2.)class Table
      -to call info and to keep info in database
    3.)out of class
      -to write and read csv file 

  2.CSV.files
  
    -login.csv
    -person.csv
    -project.csv
    -member.csv
    -advisor.csv

  3.project_manage.py
  
    1.)class User
      -keep user.id and user.name
    2.)class Student
      -to do everything for student
    3.)class Member
      -to do everything for member
    4.)class Lead
      -to do everything for leader
    5.)class Faculty
      -to do everything for faculty
    6.)class Advisor
      -to do everything for advisor
    7.)class Admin
      -to do everything for admin

To compile and run your project.

  -Student creates his/her project, send requests to faculty and other students
  -Faculty and other students come in program and accept to be members and advisor
  -And after that up to you 
  

| Role | Action | Method  | Class | Completion percentage |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Student  | view request from leader student  | view_pending_requests  | Student  | 80  |
| Student  | accept or deny request from leader student  | accept_or_deny_request  | Student  | 80  |
| Student  | make your project and become leader  | create_project  | Student  | 100  |
| Leader  | check project status  | view_project_status  | Leader  | 100  |
| Leader  | change information in project  | modify_project_information  | Leader  | 100  |
| Leader  | send request to student to be your member  | send_member_requests  | Leader  | 80  |
| Leader  | send request to faculty to be your advisor  | send_advisor_request  | Leader  | 80  |
| Member  | check project status  | view_project_status  | Member  | 100  |
| Member  | change information in project  | modify_project_information  | Member  | 100  |
| Faculty  | view request from leader student  | view_supervisor_requests  | Faculty  | 100  |
| Faculty  | accept or deny request from leader student  | send_response_to_request  | Faculty  | 80  |
| Faculty  | view all projects | view_all_projects  | Faculty  | 100  |
| Faculty  | i still dont know | evaluate_projects  | Faculty  | 0  |
| Advisor  | view request from leader student | view_supervisor_requests  | Advisor  | 100  |
| Advisor  | accept or deny request from leader student | send_response_to_request  | Advisor  | 80  |
| Advisor  | view all projects | view_all_projects  | Advisor  | 100  |
| Advisor  | i still dont know | evaluate_projects  | Advisor  | 0  |
| Advisor  | approve project to solicit | approve_project  | Advisor  | 80  |
| Admin  | can see all project and change information in it  | view_and_modify_all_projects  | Admin  | 80  |
| Admin  | add or remove person to the system  | add_or_remove_person  | Admin  | 0  |

BugAndMissingfeatures
  -
  1.Bug
  

    
  2.MissingFeatures
  
    -I didnt do evaluate projects at all ;-;(Could you possibly change deadline? Im sure that if I get 1-2 more days,I will finish it.)
    -Now I didnt make an exit choice for you. If you finish any choice you want to try,you have to stop the program and start it again. I really really really sorry about this. T-T
    -For all valueerror(if you try to put any names in my program whether has it or not, it wont error)
