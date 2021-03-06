#Matthew Witkowski. Access Control Model Project
import sys
import re
from sets import Set

auditFile = open("audit.txt","a")


filename = sys.argv[-1]
#make sure it's a texot file in the command line
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
       self.userList = set()
       self.groupName = groupName
       #link files and permissions
       self.filePermMap = {}




#holds what user is currently logged in
loggedIn = loginState()
loggedIn.logLock = True
#holds the group objects
groupList = set()
#holds the files
fileList = set()
#holds the users
userListGlobal = set()


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
    for userCheck in userListGlobal:
        if userCheck.username == userNameIn:
            return True
    return False
def getUser(userNameIn):
    for userCheck in userListGlobal:
        if userCheck.username == userNameIn:
            return userCheck
    return None
def getFile(fileNameIn):
    for fileCheck in fileList:
        if fileCheck.fileName == fileNameIn:
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



    group = getGroup(groupNameIn)
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
    if file.owner.username == user.username:#check owner perms
        if file.perms1[0:1] == "r":
            return True
    if file is not None and file.groupName != "nil":
        perms = checkUserGroupPerms(userNameIn, file.groupName, fileNameIn)
        if perms is not None and perms[0:1] == "r":
            return True
    #print (file.perms3)
    if file.perms3[0:1] == "r":
        return True
    return False
def checkCanWrite(userNameIn, fileNameIn):
    #print userNameIn
    #print fileNameIn
    user = getUser(userNameIn)
    file = getFile(fileNameIn)
    #print "file gname " + file.groupName
    if user is None:
        return False
    if user.isRoot:
        return True

    if file.owner.username == user.username:#check owner perms

        if file.perms1[1:2] == "w":
            return True
    if file is not None :

        perms = checkUserGroupPerms(userNameIn, file.groupName, fileNameIn)

        if perms is not None and perms[1:2] == "w":

            return True
    #print (file.perms3)
    if file.perms3[1:2] == "w":
        return True

    return False

def checkCanExecute(userNameIn, fileNameIn):

    user = getUser(userNameIn)
    file = getFile(fileNameIn)
    if user is None:
        return False
    if user.isRoot:
        return True
    if file.owner.username == user.username:#check owner perms
        if file.perms1[2:3] == "x":
            return True
    if file is not None and file.groupName != "nil":
        perms = checkUserGroupPerms(userNameIn, file.groupName, fileNameIn)
        if perms is not None and perms[2:3] == "x":
            return True
    #print (file.perms3)
    if file.perms3[2:3] == "x":
        return True
    return False

def fillWrite(splitlist):
    stringyboi = ''
    i = 2
    for i in range (len(splitlist)):
        stringyboi += splitlist[i] + " "
    return stringyboi

def retGroupUsers(groupName):
    group = getGroup(groupName)
    retstring = ''
    for entry in group.userList:
        retstring += entry.username + " "
    return retstring


def writeGroup():
    gFile = open("groups.txt","a")
    if gFile is None:
        print "GROUPS file never found!! HELP!!"
    print "GROUPS "+ "\n"
    for entry in groupList:
        print entry.groupName + ": "+retGroupUsers(entry.groupName) + " "
        gFile.write(entry.groupName + ": "+retGroupUsers(entry.groupName)+ " " + "/n")

def writeFiles():
    fFile = open("files.txt", "a")
    if fFile is None:
        print "FILES file never found!! HELP!!"
    print "FILES " + "\n"
    for file in fileList:
        print file.fileName +" "+file.owner.username+ " " + file.perms1 + " " + file.perms2 + " " + file.perms3
        fFile.write(file.fileName +" "+file.owner.username+ " " + file.perms1 + " " + file.perms2 + " " + file.perms3 + "/n")



#method that takes in list of user commands and creates global simplified commands list
def makeCMDList(lines): #TODO make sure command to create root user is the first line
    linecount = 0
    for line in lines:

        linecount += 1
        if line == "end":
            auditFile.write("end")
            writeGroup()
            writeFiles()
            return
        line = line.strip()
        argList = line.split()
        argCount = len(argList)

        # group ifs by the argument count.
        if argList[0] != "write" and (argCount > 5 or argCount < 1) or argCount == 4:

            auditFile.write(
                "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
            print(
                        "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
                #return
        elif argList[0] == "useradd" and linecount == 1 and argList[1] == "root" and argCount == 3:
            print("root user created\n")
            auditFile.write("root user created\n")
            rootUser = User(True, "root", argList[2])
            userListGlobal.add(rootUser)
        elif argList[0] == "write" and not loggedIn.logLock and (checkFileDup(argList[1]) ): #add perms later
            #print loggedIn.login.username
            if checkCanWrite(loggedIn.login.username, argList[1]):
                auditFile.write("user " + loggedIn.login.username + "wrote " + fillWrite(argList) + "\n")
                print "user " + loggedIn.login.username + "wrote " + fillWrite(argList) + "\n"
                #return

            # TODO
           # return  and

        elif argCount == 1 and not loggedIn.logLock:
            if line == "logout":
                outtie = loggedIn.login.username
                loggedIn.logLock = True
                loggedIn.login = None
                auditFile.write("user logout " +outtie +"\n")
                print("user logout " +outtie +"\n")
                #TODO
            #    return




                #TODO
             #   return
            else:
                auditFile.write(
                    "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
                print(
                            "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")

        elif argCount == 2:
            if argList[0] == "groupadd" and not loggedIn.logLock and (argList[1] is not None
                                            and len(argList[1]) < 30 and argList[1] != "nil"
                                             and not checkGroupDup(argList[1])):

                groupGuy = Group(argList[1])
                groupList.add(groupGuy)
                auditFile.write("group " + argList[1] + " made " "\n")
                print "group " + argList[1] + " made " "\n"
                #TODO
              #  return
            elif argList[0] == "mkfile" and not loggedIn.logLock and (loggedIn.login is not None and not checkFileDup(argList[1])):

                madeFile = File(argList[1], loggedIn.login, "rw-","---","---")
                fileList.add(madeFile)
                auditFile.write("file " + argList[1] + " made with owner " + loggedIn.login.username +" made with default permissions" "\n")
                print "file " + argList[1] + " made with owner " + loggedIn.login.username +" made with default permissions" "\n"


                #TODO
               # return
            elif argList[0] == "read" and not loggedIn.logLock and (checkFileDup(argList[1])): #Check permissions later
                if checkCanRead(loggedIn.login.username, argList[1]):
                    auditFile.write("User " + loggedIn.login.username + " read " +argList[1] +" as " + fillWrite(argList)  +"\n")
                    print "User " + loggedIn.login.username + " read " +argList[1] +" as " + fillWrite(argList)  +"\n"
                else:
                    auditFile.write("User " + loggedIn.login.username + " denied read access of" + argList[1]+ "\n")
                    print "User " + loggedIn.login.username + " denied read access of" + argList[1]+ "\n"

                #TODO
                #return
            elif argList[0] == "execute" and not loggedIn.logLock and (checkFileDup(argList[1])): #Check permissions later
                if checkCanExecute(loggedIn.login.username, argList[1]):
                    auditFile.write("User " + loggedIn.login.username + " executes " +argList[1] +" as " + fillWrite(argList)  +"\n")
                    print "User " + loggedIn.login.username + " executes " +argList[1] +" as " + fillWrite(argList)  +"\n"
                else:
                    auditFile.write("User " + loggedIn.login.username + " denied execute access of" + argList[1]+ "\n")
                    print "User " + loggedIn.login.username + " denied execute access of" + argList[1]+ "\n"
            else:
                auditFile.write(
                    "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
                print(
                            "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
               # return

        elif argCount == 3:
            if argList[0] == "usergrp" and not loggedIn.logLock and (loggedIn.login.isRoot and checkUserExists(argList[1])) and checkGroupDup(argList[2]):

                getGroup((argList[2])).userList.add(getUser(argList[1]))
                #TODO
                auditFile.write(
                    "User " + argList[1] + " added to group " + argList[2] +"\n")
                print "User " + argList[1] + " added to group " + argList[2] +"\n"


                #return
            elif argList[0] == "useradd" and not loggedIn.logLock and (loggedIn.login.isRoot and not checkUserExists(argList[1]) and linecount > 1):

                #TODO
                user = User(False, argList[1], argList[2])
                userListGlobal.add(user)
                auditFile.write("User " + argList[1] + " created "+"\n")
                print "User " + argList[1] + " created "+"\n"
                #return
            elif argList[0] == "chown" and not loggedIn.logLock and (loggedIn.login.isRoot and checkFileDup(argList[1]))\
                    and checkUserExists(argList[2]):
                tempPerms = getFile(argList[1]).perms1

                getFile(argList[1]).owner = getUser(argList[2])
                getFile(argList[1]).perms1 = tempPerms
                auditFile.write("File " + argList[1] + " changed ownership of to  " + argList[2] + "\n")
                print "File " + argList[1] + " changed ownership of to  " + argList[2] + "\n"

                #TODO
                #return
            elif argList[0] == "chgrp" and not loggedIn.logLock and checkGroupDup(argList[2]) and \
                    ((loggedIn.login.isRoot or checkUserOwns(loggedIn.login.username, argList[1]))
                                           and checkFileDup(argList[1])):
                #print "boi"
                #get old group
               # print getFile(argList[1]).perms1+ " " + getFile(argList[1]).perms2 +" " +getFile(argList[1]).perms3
                file = getFile(argList[1])

                if file.groupName == "nil":
                   # print 'boi1'

                    getGroup(argList[2]).filePermMap[argList[1]] = getFile(argList[1]).perms2
                    file.groupName = argList[2]
                    auditFile.write("File " + argList[1] + " changed group to  " + argList[2] + "\n")
                    print "File " + argList[1] + " changed group to  " + argList[2] + "\n"
                else:
                    #print 'boi2'
                    tempperms = getGroup(file.groupName).filePermMap[argList[1]]#temp swap to update new perms
                    getGroup(file.groupName).filePermMap[argList[1]] = "nil"
                    getGroup(argList[2]).filePermMap[argList[1]] = tempperms
                    file.groupName = argList[2]
                    auditFile.write("File " + argList[1] + " changed group to  " + argList[2] + "\n")
                    print "File " + argList[1] + " changed group to  " + argList[2] + "\n"
                #TODO
                #return


            elif argList[0] == "login" and loggedIn.logLock:

                    if not checkUserExists(argList[1]):
                        auditFile.write(argList[1] + " tried to login. No account found"  +"\n")
                        print argList[1] + " tried to login. No account found"  +"\n"
                    else:
                        if not getUser(argList[1]).password == argList[2]:
                            auditFile.write(argList[1] + " tried to login. Wrong Password!" + "\n")
                            print argList[1] + " tried to login. Wrong Password!" + "\n"
                        else:
                            loggedIn.login = getUser(argList[1])
                            loggedIn.logLock = False
                            auditFile.write(argList[1] + " logged in!" + "\n")
                            print argList[1] + " logged in!" + "\n"

            elif(argList[0] == "login" and not loggedIn.logLock):
                auditFile.write(argList[1] + " tried to login, but someone's already logged in!" + "\n")
                print argList[1] + " tried to login, but someone's already logged in!" + "\n"

                #TODO

                #return
            else:
                auditFile.write(
                    "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
                print(
                            "Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
        elif argCount == 5:

            if argList[0] == "chmod" and not loggedIn.logLock and(checkFileDup(argList[1]) and (checkUserOwns(loggedIn.login.username, argList[1]) or
                                         loggedIn.login.isRoot)) and(checkPermCharsValid(argList[2]) and
                                                                      checkPermCharsValid(argList[3]) and
                                                                      checkPermCharsValid(argList[4])):
                file = getFile(argList[1])
                file.perms1 = argList[2]
                file.perms2 = argList[3]
                file.perms3 = argList[4]

                #TODO
                auditFile.write("Changed permissions of " + argList[1] + " to " +argList[2]+ " " + argList[3]+ " "+argList[4] + " by "+ loggedIn.login.username+"\n")
                print "Changed permissions of " + argList[1] + " to " +argList[2]+ " " + argList[3]+ " "+argList[4] + " by "+ loggedIn.login.username+"\n"
                #return
            else:

                auditFile.write("Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")
                print("Invalid arguments or command never ran due to no user being logged in, invalid permissions, etc: " + line + "\n")

    return
        #keep going up to 5
makeCMDList(lines)







