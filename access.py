#Matthew Witkowski. Access Control Model Project
import sys

filename = sys.argv[-1]
#make sure it's a text file in the command line
if not filename[-4:] == '.txt':
    print('invalid file type')
    sys.exit(0)


f = open(filename, 'r')
lines = f.readlines()

class loginState:
    def __init__self(self, login, logout):#probably won't need logout, may be useful for audit logs
        self.login = login
        self.logout = logout


class User:
    def __init__(self, isRoot, username, password):
        self.isRoot = isRoot
        self.username = username
        self.password = password
        self.loggedIn = False

class File:
    def __init__(self, fileName, owner, perms1, perms2, perms3, groupName):
        self.isRoot = fileName
        self.owner = owner
        self.perms1 = perms1
        self.perms2 = perms2
        self.perms3 = perms3
        self.groupName = groupName

class Group:#add check later to snsure no duplicate groups
    def __init__(self, groupName):
       self.userList = list()
       self.groupName = groupName


#holds what user is currently logged in
loggedIn = loginState()
#holds the group objects
groupList = list()
#holds the files
fileList = list()
#holds the users
userList = list()

#useradd username password
#login username password
#logout
#groupadd groupname
#usergrp username groupname
#mkfile filename
#chmod filename rwx rwx rwx
#chown filename username
#hgrp filename groupname
#read filename
#write filename text
#execute filename
#ls filename
#end
#In order to create the super user for the system, the very first line of the instructions file has to be of
#the form:
#useradd root password

def checkGroupDup(groupNameIn):
    for groupCheck in groupList:
        if groupCheck.groupName == groupNameIn:
            return True
    return False
def checkFileDup(fileNameIn):
    for fileCheck in fileList:
        if fileCheck.fileName == fileNameIn:
            return True
    return False


#method that takes in list of user commands and creates global simplified commands list
def makeCMDList(lines): #TODO make sure command to create root user is the first line
    for line in lines:
        line = line.strip()
        argList = line.split()
        argCount = len(argList)

        # group ifs by the argument count.
        if argCount > 5 or argCount < 1:
                print("Invalid arguments. Incorrect count of clauses at command: " + line)
        if argCount == 1:
            if(line.equals("logout")):
                #TODO
                return
            elif(line.equals("end")):
                #TODO
                return
            else:
                print("Invalid arguments. Unrecognized command: " + line)
                return

        if argCount == 2:
            if argList[0] == "groupadd" and (argList[1] is not None and len(argList[1]) < 30 and argList[1] != "nil"
                                             and not checkGroupDup(argList[1])):
                #TODO
                return
            if argList[0] == "mkfile" and (loggedIn.login is not None and not checkFileDup(arlList[1])):
                #TODO
                return


        return
        #keep going up to 5
makeCMDList(lines)






