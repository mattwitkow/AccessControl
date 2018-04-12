#Matthew Witkowski. Access Control Model Project
import sys

filename = sys.argv[-1]
#make sure it's a text file in the command line
if not filename[-4:] == '.txt':
    print('invalid file type')
    sys.exit(0)






#Define command list

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
f = open('filename', 'r')
lines = f.readlines()



class User:
    def __init__(self, isRoot, username, password):
        self.isRoot = isRoot
        self.username = username
        self.password = password

class File:
    def __init__(self, fileName, owner, perms1, perms2, perms3, groupName):
        self.isRoot = fileName
        self.owner = owner
        self.perms1 = perms1
        self.perms2 = perms2
        self.perms3 = perms3
        self.groupName = groupName

class Group:#add check later to snsure no duplicate groups
    def __init__(self, userList):
       self.userList = userList

#method that takes in list of user commands and creates global simplified commands list
def makeCMDList(self, lines): #TODO make sure command to create root user is the first line
    for line in lines:
        line = line.strip().trim
        argList = line.split()
        argCount = argList.size()

        # group ifs by the argument count.
        if argCount > 5 or argCount < 1:
                print("Invalid arguments. Incorrect count of clauses at command: " + line)
        if argCount == 1:
            if(line.equals("logout")):
                #TODO
                return
            if(line.equals("end")):
                #TODO
                return
    return
        #keep going up to 5






