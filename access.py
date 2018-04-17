#Matthew Witkowski. Access Control Model Project
import sys
import re
from sets import Set
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
        self.logLock = True



class User:
    def __init__(self, isRoot, username, password):
        self.isRoot = isRoot
        self.username = username
        self.password = password
        self.loggedIn = False

    def getUsername(self):
        return self.username

    def getPassword(self,usr):
        return self.password

class File:
    def __init__(self, fileName, owner, perms1, perms2, perms3):
        self.fileName = fileName
        self.owner = owner
        self.perms1 = perms1
        self.perms2 = perms2
        self.perms3 = perms3
        self.groupName = "nil"

class Group:#add check later to snsure no duplicate groups
    def __init__(self, groupName):
       self.userList = list()
       self.groupName = groupName
       #link files and permissions
       self.filePermMap = {}




#holds what user is currently logged in
loggedIn = loginState()
loggedIn.logLock = True
#holds the group objects
groupList = list()
#holds the files
fileList = list()
#holds the users
userList = list()


def checkGroupDup(groupNameIn):
    for groupCheck in groupList:
        if groupCheck.groupName == groupNameIn:
            return True
    return False
def getGroup(groupNameIn):
    for groupCheck in groupList:
        if groupCheck.groupName == groupNameIn:
            return groupCheck
    return None
def checkFileDup(fileNameIn):
    for fileCheck in fileList:
        if fileCheck.fileName == fileNameIn:
            return True
    return False

def checkUserExists(userNameIn):
    for userCheck in userList:
        if userCheck.username == userNameIn:
            return True
    return False
def getUser(userNameIn):
    for userCheck in userList:
        if userCheck.username == userNameIn:
            return userCheck
    return None
def getFile(fileNameIn):
    for fileCheck in fileList:
        if fileCheck.filename == fileNameIn:
            return fileCheck
    return None

def checkUserOwns(userNameIn, fileNameIn):

    for fileCheck in fileList:
        if fileCheck.owner.username == userNameIn and fileCheck.fileName == fileNameIn:
            return True
    return False

def checkPermCharsValid(permIn):
    if len(permIn) != 3:
        return False
    legalPerms = Set('rwx-')

    if Set(permIn).issubset(legalPerms):
        return True
    else:
        return False
#
def checkUserInGroup(userNameIn, groupNameIn):
    group = getGroup(groupNameIn)
    for entry in group.userList:
        if entry.username == userNameIn:
            return True
    return False


#see what file permissions the user gets because of the group they're in. None if they're not in group
def checkUserGroupPerms(userNameIn, groupNameIn,fileName):
    group = None
    for groupCheck in groupList:
        if groupNameIn == groupCheck:
            group = groupCheck
    if group is None:
        return None
    if checkUserInGroup(userNameIn, groupNameIn):
        fileMap = group.filePermMap
        return fileMap[fileName]

    return None




#define methods to sort permissions. Still must be logged in before these methods work
def checkCanRead(userNameIn, fileNameIn):

    user = getUser(userNameIn)
    file = getFile(fileNameIn)
    if user is None:
        return False
    if user.isRoot:
        return True
    if file.owner.userNameIn == user.userNameIn:#check owner perms
        if file.perms1[0:1] == "r":
            return True
        else:
            return False
    if file is not None and file.groupName != "nil":
        perms = checkUserGroupPerms(userNameIn, file.groupName, fileNameIn)
        if perms is not None and perms[0:1] == "r":
            return True
    if file.perms3[0:1] == "r":
        return True
    return False



#method that takes in list of user commands and creates global simplified commands list
def makeCMDList(lines): #TODO make sure command to create root user is the first line
    linecount = 0
    for line in lines:
        linecount += 1
        line = line.strip()
        argList = line.split()
        argCount = len(argList)

        # group ifs by the argument count.
        if argList[0] != "write" and (argCount > 5 or argCount < 1) or argCount == 4:
                print("Invalid arguments. Incorrect count of clauses at command: " + line)
                return
        elif argList[0] == "useradd" and linecount == 1 and argList[1] == "root" and argCount == 3:
            print("useraddroot\n")
            rootUser = User(True, "root", argList[2])
            userList.append(rootUser)

            # TODO
           # return  and

        elif argCount == 1 and not loggedIn.logLock:
            if line == "logout":
                loggedIn.logLock = True
                loggedIn.login = None
                print("logout\n")
                #TODO
            #    return
            elif line == "end" and not loggedIn.logLock:

                print("end\n")
                return
                #TODO
             #   return
            else:
                print("Invalid arguments. Unrecognized command: " + line + "\n")
                return

        elif argCount == 2:
            if argList[0] == "groupadd" and not loggedIn.logLock and (argList[1] is not None
                                            and len(argList[1]) < 30 and argList[1] != "nil"
                                             and not checkGroupDup(argList[1])):
                groupGuy = Group(argList[1])
                groupList.append(groupGuy)
                print("groupadd\n")
                #TODO
              #  return
            elif argList[0] == "mkfile" and not loggedIn.logLock and (loggedIn.login is not None and not checkFileDup(argList[1])):

                madeFile = File(argList[1], loggedIn.login, "rw-","---","---")
                fileList.append(madeFile)

                print("mkfile\n")
                #TODO
               # return
            elif argList[0] == "read" and not loggedIn.logLock and (checkFileDup(argList[1])): #Check permissions later
                print("readfile\n")
                #TODO
                #return
            elif argList[0] == "execute" and not loggedIn.logLock and (checkFileDup(argList[1])): #Check permissions later
                print("execute\n")
                #TODO
                #return
            elif argList[0] == "ls" and not loggedIn.logLock and (checkFileDup(argList[1])): #Check permissions later
                #TODO
                print("ls\n")
                #return
            else:
                print("Invalid arguments. Unrecognized command: " + line +"\n")
                return

        elif argCount == 3:
            if argList[0] == "usergrp" and not loggedIn.logLock and (loggedIn.login.isRoot and checkUserExists(argList[1])
                                            and checkGroupDup(argList[2])):
                #TODO
                print("usergrp\n")
                #return
            elif argList[0] == "useradd" and not loggedIn.logLock and (loggedIn.login.isRoot and not checkUserExists(argList[1]) and linecount > 1):

                #TODO
                user = User(False, argList[1], argList[2])
                userList.append(user)
                print("useradd\n")
                #return
            elif argList[0] == "chown" and not loggedIn.logLock and (loggedIn.login.isRoot and checkFileDup(argList[1]))\
                    and checkUserExists(argList[2]):
                print("chown\n")
                #TODO
                #return
            elif argList[0] == "chgrp" and not loggedIn.logLock and checkGroupDup(argList[2]) and ((loggedIn.login.isRoot or checkUserOwns(loggedIn.login.username, argList[1]))
                                           and checkFileDup(argList[1]) ):
                print("chgrp\n")
                #TODO
                #return
            elif argList[0] == "write" and not loggedIn.logLock and (checkFileDup(argList[1]) and ()): #add perms later
                #TODO
                print("write\n")
                #return

            elif argList[0] == "login" and loggedIn.logLock:

                    if not checkUserExists(argList[1]):
                            print "user no exists"
                    else:
                        if not getUser(argList[1]).password == argList[2]:
                            print "bad pw"
                        else:
                            loggedIn.login = getUser(argList[1])
                            loggedIn.logLock = False
                            print("login\n")
            elif(argList[0] == "login" and not loggedIn.logLock):
                print"log out before in"
                #TODO

                #return
            else:
                print("Invalid arguments. Unrecognized command: " + line + "\n")
                return
        elif argCount == 5:

            if argList[0] == "chmod" and not loggedIn.logLock and(checkFileDup(argList[1]) and (checkUserOwns(loggedIn.login.username, argList[1]) or
                                         loggedIn.login.isRoot)) and(checkPermCharsValid(argList[2]) and
                                                                      checkPermCharsValid(argList[3]) and
                                                                      checkPermCharsValid(argList[4])):

                #TODO
                print("chmod\n")
                #return
            else:

                print("Invalid arguments. Unrecognized command: " + line + "\n")
                return

    return
        #keep going up to 5
makeCMDList(lines)






