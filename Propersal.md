For program
  -Every action that user does will return in a dic pattern with 2keys(name what they wanna change, how it changes)
    ex. If advisor accepts to be a supervisor
          return name:brabrabra,role:supervisor

  -DB updated its table by looking for the heading name that has the same as dic keys that we gave it

For EACH ROLE
  -Admin
    He can do everything we can. This role is the easiest role to do.(right?)

  -Student
    -I think persons who are invited by the leader students will have a name in member_pending_request table.
If they come into the program, the program will print out an invitational message.
    -Persons who have a name in member_pending_request table will see an invitational message and they can choose either accept or deny.
if they accept, their status will turn to "member student" and delete member_pending_request table.
elif they deny, the Program deletes member_pending_request table with their name inside.
    -To see the project status and details we can do it by calling info from DB.
    -To modify the project we can do it by updating info from DB.
    -To create a Project. The program will create a new Project table.After putting all info completely,this table will update to DB.
    -To send a request message to advisor I think we have to do it just like inviting member students.
    -Submit project is update project in DB.

  -Faculty and advisor
    -Just like the student. we use the same way to make them see a request to be a supervisor 
and they can make decisions that they wanna accept or deny.
    -Faculty have power to see all project
    -To approve the project.We can do it by change project table->status

Everything I said I didnt do it yet but I would try it after I get feedback.
