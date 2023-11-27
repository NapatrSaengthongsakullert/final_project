import database,csv

# define a funcion called initializing
def initializing():
# here are things to do in this function:
    # create an object to read all csv files that will serve as a persistent state for this program

    # for i in database:
    #     myFile = open(i.csv, 'w')
    #     reader = csv.reader(myFile)
    #     row = [x for x in list_dict[0].keys()]
    #     reader.writerow(row)
    #     for dictionary in list_dict:
    #         reader.writerow(dictionary.values())
    #     myFile.close()
    # Not completed yet.

    # create all the corresponding tables for those csv files
    Person_table = {"ID":"","First":"","Last":"","Type":""}
    Login_table = {"ID":"","Username":"","Password":"","Role":""}
    Project_table = {"ProjectID":"","Title":"","Lead":"","Member1":"","Member2":"","Advisor":"","Status":""}
    Advisor_table = {"ProjectID":"","to_be_advisor":"","Response":"","Respongse_date":""}
    Member_table = {"ProjectID":"","to_be_member":"","Response":"","Respongse_date":""}
    # see the guide how many tables are needed
    # add all these tables to the database
    DB = database.Database()
    person = database.Table("Person",Person_table)
    login = database.Table("Login",Login_table)
    project = database.Table("Project",Project_table)
    advisor = database.Table("Advisor",Advisor_table)
    member = database.Table("Member",Member_table)
    DB.insert(person)
    DB.insert(login)
    DB.insert(project)
    DB.insert(advisor)
    DB.insert(member)

# define a funcion called login
def login():
    username = input("Please input\nUsername: ")
    password = input("Password: ")
    for i in range(len(database.login)):
        if database.login[i]["username"] == username:
            if database.login[i]["password"] == password:
                return [database.login[i]["ID"],database.login[i]["role"]]
        else:
            return None
# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None

def write_csv(name, list_dict):
    myFile = open(name.csv, 'w')
    writer = csv.writer(myFile)
    row = [x for x in list_dict[0].keys()]
    writer.writerow(row)
    for dictionary in list_dict:
        writer.writerow(dictionary.values())
    myFile.close()



# define a function called exit
def exit():

    break

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

# initializing()
val = login()
print(val)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
#     see and do admin related activities
# elif val[1] = 'student':
#     see and do student related activities
# elif val[1] = 'member':
#     see and do member related activities
# elif val[1] = 'lead':
#     see and do lead related activities
# elif val[1] = 'faculty':
#     see and do faculty related activities
# elif val[1] = 'advisor':
#     see and do advisor related activities

# once everyhthing is done, make a call to the exit function
exit()
