import database,csv,os
class User:
    def __init__(self, ID , username):
        self.ID = ID
        self.username = username


class Student(User):
    def __init__(self, ID , username):
        super().__init__(ID, username)


    def view_pending_requests(self):
        invite_member = db.search("member_pending_request_info")
        project_member = db.search("project_info")
        request_info = invite_member.join(project_member, 'ProjectID').select(["ProjectID","to_be_member","response","lead"])
        for i in request_info:
            if i["to_be_member"] == self.username:
                if i["response"] == "Waiting":
                    print(f"ProjectID:{i['ProjectID']} from {i['lead']} has invited you to be a member")
                    return i['ProjectID']
        print("No invitation found")


    def accept_or_deny_request(self,project_id):
        user_input = str(input("Accept(A)/Denied(D) request? : "))
        invite_table = db.search("member_pending_request_info").select(["to_be_member", "response"])
        if user_input == "Accept" or user_input == "A":
            self.project = db.search("project_info").filter(lambda x: x['ProjectID'] == project_id).select(['ProjectID','title','lead','member1','member2','advisor','status'])
            db.search("person_info").update_row('ID',self.ID,'type','member')
            db.search("login_info").update_row('ID',self.ID,'role','member')
            if self.project[0]['member1'] == "None":
                db.search("project_info").update_row('ProjectID',project_id,"member1",self.username)
            elif self.project[0]["member1"] != "None":
                db.search("project_info").update_row('ProjectID', project_id, "member2", self.username)
        #     for i in invite_table
        #
        # elif user_input == "Denied" or user_input == "D":
        #     for i in invite_table:
        #         if i["to_be_member"] == self.ID:
        #             if i["response"] == "Waiting":
        #                 i["response"] = "Denied"
        #


    def create_project(self):
        user_input = str(input("Select your title: "))
        project_info = {'ProjectID': len(db.search("project_info").select(["title"])) + 1, 'title': user_input, 'lead': self.ID, 'Member1': "None",
                'Member2': "None", 'Advisor': "None", 'Status': "Created"}
        db.search("project_info").insert_row(project_info)
        print(f'ProjectID: {len(db.search("project_info").select(["title"]))} created')
        db.search("person_info").update_row('ID', self.ID, 'type', 'lead')
        db.search("login_info").update_row('ID', self.ID, 'role', 'lead')


class Leader(Student):
    def __init__(self, ID,username,project):
        super().__init__(ID , username,project)


    def view_project_status(self):
        project_table = db.search("project_info").filter(lambda x: x['lead'] == self.username).select(['status'])
        print(f"Now your project is {project_table[0]['status']}")


    def modify_project_information(self):
        choice = str(input("Are you sure?(press s,but if not press n) : "))
        if choice == "s":
            user_input = str(input("Input your new title: "))
            db.search("project_info").update_row('lead', self.username, 'title', user_input)
        elif choice == "n":
            pass


    def send_member_requests(self):
        user_input = str(input("Please enter his/her name: "))
        for i in db.search("project_info").select(['ProjectID','lead',"member1","member2"]):
            if i["member1"] or i["member2"] or i['lead'] == user_input:
                print(f"You cant send request to {user_input}")
        member_info = {"ProjectID":self.project[0]['ProjectID'],"to_be_member":user_input,"response":"Waiting"}
        db.search('member_pending_request_info').insert_row(member_info)
        print("Successful!")


    def send_advisor_request(self):
        user_input = str(input("Please enter his/her name: "))
        for i in db.search("project_info").select(['ProjectID', 'advisor']):
            if i["advisor"] == user_input:
                print(f"You cant send request to {user_input}")
        advisor_info = {"ProjectID": self.project[0]['ProjectID'], "to_be_advisor": user_input, "response": "Waiting"}
        db.search('advisor_pending_request_info').insert_row(advisor_info)
        print("Successful!")


class Member(Student):
    def __init__(self, ID , username,project):
        super().__init__(ID,username,project)


    def view_project_status(self):
        project_table = db.search("project_info").filter(lambda x: x['member1'] == self.username or x['member2'] == self.username).select(['status'])
        print(f"Now your project is {project_table[0]['status']}")


    def modify_project_information(self):
        choice = str(input("Are you sure?(s) : "))
        if choice == "Sure" or choice == "s":
            user_input = str(input("Input your new title: "))
            db.search("project_info").update_row('ProjectID',self.project[0]['ProkectID'],'title',user_input)


class Faculty(User):
    def __init__(self,ID ,username):
        super().__init__(ID , username)


    def view_supervisor_requests(self):
        list = []
        count = 0
        invite_advisor = db.search("advisor_pending_request_info")
        project_member = db.search("project_info")
        request_info = invite_advisor.join(project_member, 'ProjectID').select(
            ["ProjectID", "to_be_advisor", "response", "lead"])
        for i in request_info:
            if i["to_be_advisor"] == self.username:
                if i["response"] == "Waiting":
                    print(f"ProjectID:{i['ProjectID']} from {i['lead']} has invited you to be an advisor")
                    list.append(i['ProjectID'])
                    count += 1
        if count == 0:
            print("No invitation found")
        else:
            return list


    def send_response_to_request(self,list):
        for i in list:
            user_input = str(input(f"Accept(A)/Denied(D) request from ProjectID:{i}? : "))
            if user_input == "Accept" or user_input == "A":
                db.search("person_info").update_row('ID', self.ID, 'type', 'advisor')
                db.search("login_info").update_row('ID', self.ID, 'role', 'advisor')
                db.search("project_info").update_row('ProjectID', i, 'advisor', self.name)
                db.search("advisor_pending_request_info").update_row('ProjectID', i, 'status', "Accepted")
            elif user_input == "Denied" or user_input == "D":
                db.search("advisor_pending_request_info").update_row('ProjectID', i, 'status', "Denied")


    def view_all_projects(self):
        for i in db.search("project_info").select(['ProjectID','title','lead','member1','member2','advisor','status']):
            print(f"ProjectID:{i['ProjectID']} title: {i['title']} from "
                  f"{i['lead']} with {i['member1']} and {i['member2']} "
                  f"advisor:{i['advisor']} status:{i['status']}")


    def evaluate_projects(self, projects):
        pass


class Advisor(User):
    def __init__(self, ID, username):
        super().__init__(ID , username)


    def view_supervisor_requests(self):
        list = []
        count = 0
        invite_advisor = db.search("advisor_pending_request_info")
        project_member = db.search("project_info")
        request_info = invite_advisor.join(project_member, 'ProjectID').select(
            ["ProjectID", "to_be_advisor", "response", "lead"])
        for i in request_info:
            if i["to_be_advisor"] == self.username:
                if i["response"] == "Waiting":
                    print(f"ProjectID:{i['ProjectID']} from {i['lead']} has invited you to be an advisor")
                    list.append(i['ProjectID'])
                    count += 1
        if count == 0:
            print("No invitation found")
        else:
            return list


    def send_response_to_request(self, list):
        for i in list:
            user_input = str(input(f"Accept(A)/Denied(D) request from {i}? : "))
            invite_table = db.search("advisor_pending_request_info").select(["to_be_advisor", "response"])
            if user_input == "Accept" or user_input == "A":
                db.search("person_info").update_row('ID', self.ID, 'type', 'advisor')
                db.search("login_info").update_row('ID', self.ID, 'role', 'advisor')
                db.search("project_info").update_row('ProjectID', i, 'advisor', self.name)
                db.search("advisor_pending_request_info").update_row('ProjectID', i, 'status', "Accepted")
            elif user_input == "Denied" or user_input == "D":
                db.search("advisor_pending_request_info").update_row('ProjectID', i, 'status', "Denied")


    def view_all_projects(self):
        for i in db.search("project_info").select(
                ['ProjectID', 'title', 'lead', 'member1', 'member2', 'advisor', 'status']):
            print(f"ProjectID:{i['ProjectID']} title: {i['title']} from "
                  f"{i['lead']} with {i['member1']} and {i['member2']} "
                  f"advisor:{i['advisor']} status:{i['status']}")


    def evaluate_projects(self):
        pass


    def approve_project(self):
        a = 0
        while a != 1:
            user_input = int(input('Input ProjectID that you want to approve: '))
            user_input_2 = int(input('Are you sure?(no/yes)'))
            if user_input_2 == "yes":
                db.search('project_info').update_row('ProjectID',user_input,'status','Approved')


class Admin(User):
    def __init__(self, ID, username):
        super().__init__(ID , username)


    def view_and_modify_all_projects(self):
        for i in db.search("project_info").select(
                ['ProjectID', 'title', 'lead', 'member1', 'member2', 'advisor', 'status']):
            print(f"ProjectID:{i['ProjectID']} title: {i['title']} from "
                  f"{i['lead']} with {i['member1']} and {i['member2']} "
                  f"advisor:{i['advisor']} status:{i['status']}")
        user_input = int(input("1.ProjectID\n2.title\n3.lead\n4.member1\n"
                               "5.member2\n6.advisor\n7.status\nWhat you want"
                               " to change? "))
        if user_input == 1:
            user_choice = int(input("Which projects do you want to change ProjectID: "))
            user_choice_2 = int(input("Enter new ProjectID: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'ProjectID',user_choice_2)
            print(f"Sucessful! Now ProjectID:{user_choice} is {user_choice_2}")
        if user_input == 2:
            user_choice = int(input("Which projects do you want to change title: "))
            user_choice_2 = str(input("Enter new title: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'title',user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'s title is {user_choice_2}")
        if user_input == 3:
            user_choice = int(input("Which projects do you want to change leader: "))
            user_choice_2 = str(input("Enter new leader's name: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'lead',user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'s leader is {user_choice_2}")
        if user_input == 4:
            user_choice = int(input("Which projects do you want to change member1: "))
            user_choice_2 = str(input("Enter new member1's name: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'member1',user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'s member1 is {user_choice_2}")
        if user_input == 5:
            user_choice = int(input("Which projects do you want to change member2: "))
            user_choice_2 = str(input("Enter new member2's name: "))
            db.search('project_info').updaterow('ProjectID', user_choice, 'member2', user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'s member2 is {user_choice_2}")
        if user_input == 6:
            user_choice = int(input("Which projects do you want to change advisor: "))
            user_choice_2 = str(input("Enter new advisor's name: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'advisor',user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'advisor is {user_choice_2}")
        if user_input == 7:
            user_choice = int(input("Which projects do you want to change status: "))
            user_choice_2 = int(input("Enter new status: "))
            db.search('project_info').updaterow('ProjectID',user_choice,'status',user_choice_2)
            print(f"Sucessful! Now Project:{user_choice}'s status is {user_choice_2}")


    def add_or_remove_person(self):
        choice = int(input("1.add person\n2.remove person"))
        if choice == 1:
            print("I havent done it yet")
        elif choice == 2:
            ID = int(input("Input his/name ID: "))
            username = input('Input his/her username: ')
            password = input('Input his/her password: ')
            first = str(input('Input his/her firstname: '))
            last = str(input('Input his/her lastname: '))
            role = str(input('Input his/her role: '))
            login_dict = {"ID":ID,'username':username,'password':password,'role':role}
            person_dict = {'ID':ID,'first':first,'last':last,'type':role}
            db.search('login_info').insert_row(login_dict)
            db.search('person_info').insert_row(person_dict)


    def manage_advisor_request(self):
        for i in db.search("advisor_pending_request_info").select(['ProjectID','to_be_advisor','response']):
            print(f"ProjectID:{i['ProjectID']} request {i['to_be_advisor']} to be advisor and now {i['response']}")


    def manage_member_request(self):
        for i in db.search("advisor_pending_request_info").select(['ProjectID', 'to_be_member', 'response']):
            print(f"ProjectID:{i['ProjectID']} request {i['to_be_member']} to be member and now {i['response']}")

#Finished line of role class

# define a funcion called initializing
db = database.Database()

def initializing():
# here are things to do in this function:
    # create an object to read all csv files that will serve as a persistent state for this program
    login = database.reader("login.csv")
    person = database.reader("person.csv")
    project = database.reader("project.csv")
    advisor = database.reader("advisor.csv")
    member = database.reader("member.csv")

    # create all the corresponding tables for those csv files
    person_table = database.Table("person_info", person)
    login_table = database.Table("login_info", login)
    project_table = database.Table("project_info", project)
    advisor_pending_request_table = database.Table("advisor_pending_request_info"
                                      , advisor)
    member_pending_request_table = database.Table("member_pending_request_info",
                                     member)
    # see the guide how many tables are needed


    # add all these tables to the database
    db.insert(person_table)
    db.insert(login_table)
    db.insert(project_table)
    db.insert(advisor_pending_request_table)
    db.insert(member_pending_request_table)


# define a funcion called login
def login():
    username = input("Please input\nUsername: ")
    password = input("Password: ")
    table = db.search("login_info").select(['ID',"username","password",'role'])
    for i in table:
        if i["username"] == username:
            if i["password"] == password:
                return [i["ID"],i["role"]]
    return None
# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None


# define a function called exit
def exit():
    login_list = db.search("login_info").select(["ID","username","password","role"])
    person_list = db.search("person_info").select(["ID","first","last","type"])
    project_list = db.search("project_info").select(["ProjectID","title","lead","member1","member2","advisor","status"])
    advisor_list = db.search("advisor_pending_request_info").select(["ProjectID","to_be_advisor","response"])
    member_list = db.search("member_pending_request_info").select(["ProjectID","to_be_member","response"])
    database.writer("login.csv",login_list,["ID","username",'password','role'])
    database.writer("person.csv",person_list,['ID','first','last','type'])
    database.writer("project.csv",project_list,['ProjectID','title','lead','member1','member2','advisor','status'])
    database.writer("member.csv",member_list,['ProjectID','to_be_member','response'])
    database.writer("advisor.csv",advisor_list,['ProjectID','to_be_advisor','response'])

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above
initializing()
val = login()
# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

user = db.search("person_info").filter(lambda x: x['ID'] == val[0]).select(["first","last","type"])
print(f"Welcome Back! {user[0]['first']} {user[0]['last']},{user[0]['type']}")
if val[1] == 'admin':
    user = Admin(val[0], user[0]["first"])
    user_input = int(input("1.Manage projects\n2.Mange member request"
                           "\n3.Manage advisor request\n4.Exit"
                           "\n""Please enter your choice: "))
    if user_input == 1:
        user.view_and_modify_all_projects()
    if user_input == 2:
        user.manage_member_request()
    if user_input == 3:
        user.manage_advisor_request()
    if user_input == 4:
        pass



elif val[1] == 'student':
    user = Student(val[0], user[0]["first"])
    user_input = int(input("1.See request\n2.Create project\n3.Exit\n"
                           "Please enter your choice: "))
    if user_input == 1:
        result = user.view_pending_requests()
        if result == 1:
            user.accept_or_deny_request()
            user_input = int(input("1.Back to menu\n2.Exit\nPlease enter your choice: "))
            if user_input == 1:
                pass
            if user_input == 2:
                pass
        if result == 0:
            user_input = int(input("1.Back to menu\n2.Exit\nPlease enter your choice: "))
            if user_input == 1:
                pass
            if user_input == 2:
                pass
    if user_input == 2:
        user.create_project()
    if user_input == 3:
        pass


elif val[1] == 'member':
    user = Member(val[0], user[0]["first"])
    user_input = int(input("1.See project status\n2.Check project\n3.Exit\n"
                            "Please enter your choice: "))
    if user_input == 1:
        user.view_project_status()
    if user_input == 2:
        user.modify_project_information()
    if user_input == 3:
        pass


elif val[1] == 'lead':
    user = Leader(val[0], user[0]["first"])
    user_input = int(input("1.See project status\n2.Invite members\n3.Invite advisor\n4.Check project\n5.Exit\n"
                           "Please enter your choice: "))
    if user_input == 1:
        user.view_project_status()
    if user_input == 2:
        user.send_member_requests()
    if user_input == 3:
        user.send_advisor_request()
    if user_input == 4:
        user.modify_project_information()
    if user_input == 5:
        pass

elif val[1] == 'faculty':
    user = Faculty(val[0], user[0]["first"])
    user_input = int(input("1.See request\n2.See projects\n3.Evaluate projects"
                           "\n4.Exit\nPlease enter your choice: "))
    if user_input == 1:
        projectid_list = user.view_supervisor_requests()
        user.send_response_to_request(projectid_list)
    if user_input == 2:
        user.view_all_projects()
    if user_input == 3:
        user.evaluate_projects()
    if user_input == 4:
        pass


elif val[1] == 'advisor':
    user = Advisor(val[0], user[0]["first"])
    user_input = int(input("1.See request\n2.See projects\n3.Evaluate projects"
                           "\n4.Approve Project""\n5.Exit"
                           "\nPlease enter your choice: "))
    if user_input == 1:
        projectid_list = user.view_supervisor_requests()
        user.send_response_to_request(projectid_list)
    if user_input == 2:
        user.view_all_projects()
    if user_input == 3:
        user.evaluate_projects()
    if user_input == 4:
        user.approve_project()
    if user_input == 5:
        pass


# once everyhthing is done, make a call to the exit function
exit()
