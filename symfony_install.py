# Library Imports
import json
import os
import sys
import subprocess
import time
import urllib2
import shutil
import zipfile

# Classes
# Project Class
class Project:
    def __init__(self):
        self.data = {"name": "", "directory":os.getcwd(), "jquery": "http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js", "foundation": "http://foundation.zurb.com/files/foundation-4.3.2.zip"}
    def setName(self, name):
        self.data["name"] = name
    def getName(self):
        return self.data["name"]
    def setDirectory(self, directory):
        self.data["directory"] = directory
    def getDirectory(self):
        return self.data["directory"]
    def getJquery(self):
        return self.data["jquery"]
    def getFoundation(self):
        return self.data["foundation"]

# Global Variable
projectGlobal = Project()

# Progress Printing
def progressPrint(percent, stepTitle, taskTitle):
    strProgressArray = []
    strProgressArray.append("\n%% " + stepTitle + ": " + taskTitle + "\n" + str(percent) + "% ! ")
    for i in range(int(percent / 5)):
        strProgressArray.append("===")
    strProgressArray.append(">\n")
    return ''.join(strProgressArray)

# Answer Handling
'''
Then we ask if the user wants to continue
If the user says yes, we proceed in the installation
If the user says no, we quit the installation
If the user says something otherwise, we ask again
'''
def askUser():
    continueProject = raw_input("Would you like to continue ?(y|n) ")
    if continueProject == "y":
        return True
    elif continueProject == "n":
        return False
    else:
        print "You said something wrong"
        return askUser()

# Installations Checking
'''
We check if php is installed (pretty mandatory for symfony)
We check if curl is installed
'''
def stepOneChecks():
# First we check if PHP is installed
    print "****** Checking PHP installation"
    phpChecking = subprocess.Popen(["which", "php"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if phpChecking == 1:
        print "PHP is installed [FALSE]"
        print "###### Error: PHP is not installed !!!!"
        print "###### You should install PHP before launching this script"
        return False
    print "PHP is installed [TRUE]"
# Then we check if curl is installed
    print "****** Checking Curl installation"
    curlChecking = subprocess.Popen(["which", "curl"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if curlChecking == 1:
        print "Curl is installed [FALSE]"
        print "###### Error: Curl is not installed !!!!"
        print "###### You should install Curl before launching this script"
        return False
    print "Curl is installed [TRUE]"
    return True

# Composer Installation
'''
We simply install composer
'''
def composerInstall():
    print "****** Composer installation"
    composerInstallation = subprocess.Popen(["curl", "-s", "http://getcomposer.org/installer", "|", "php"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if composerInstallation == 1:
        print "Composer is installed [FALSE]"
        print "###### Error: Cannot install composer !!!!"
        print "###### You should check your internet connection first"
        return False
    print "Composer is installed [TRUE]"
    return True

#Project Caract Asked
'''
Project Caract Handler
'''
def projectCaractHandler(type):
    global projectGlobal
    if type == 1:
# Project Name
        projectName = raw_input("Please enter a project name: ")
        projectGlobal.setName(projectName)
        continueName = raw_input("You entered :\n" + projectName + "\nIs that correct ?(y|n)")
        if continueName == "y":
            return True
        else:
            return projectCaractHandler(1)
    elif type == 2:
# Project Directory
        print "The project will be installed in the following directory:\n"
        print projectGlobal.getDirectory() + "/" + projectGlobal.getName()
        continueName = raw_input("\nIs that correct ?(y|n)")
        if continueName == "y":
            return True
        else:
            projectDirectory = raw_input("Please enter a project directory: ")
            projectGlobal.setDirectory(projectDirectory)
            return projectCaractHandler(2)
    else:
        return False

#Symfony install function
'''
It checks if the directory exists
delete it if so
then it call the symfony installer 
with composer
'''
def symfonyInstall():
    global projectGlobal
    print "****** Symfony installation"
    pathToInstall = projectGlobal.getDirectory() + "/" + projectGlobal.getName()
    if os.path.exists(pathToInstall) == True:
        shutil.rmtree(pathToInstall)
    symfonyInstall = subprocess.call(["php", "composer.phar", "create-project", "symfony/framework-standard-edition", pathToInstall])
    if symfonyInstall == 1:
        print "Symfony is installed [FALSE]"
        print "###### Error: Cannot install symfony !!!!"
        print "###### You should check your internet connection first"
        return False
    print "Symfony is installed [TRUE]"
    os.mkdir(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js")
    print "JS Directory created"
    os.mkdir(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/css")
    print "CSS Directory created"
    os.mkdir(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/img")
    print "IMG Directory created"
    return True

# Extract the foundation archive
def handleFoundationArchive():
    foundationZip = zipfile.ZipFile(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/foundation-4.3.2.zip", "r")
    print "Extracting Foundation"
# Extract the archive
    archivePath = projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/foundation"
    print "Archive Extracted"
    jsLib = projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js/lib"
    cssLib = projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/css"
    foundationZip.extractall(archivePath)
# Copy the files
    print "Copying Foundation JS Min File"
    shutil.copyfile(archivePath + "/js/foundation.min.js", jsLib + "/foundation.min.js")
    print "File Copied\nCopying Zepto JS File"
    shutil.copyfile(archivePath + "/js/vendor/zepto.js", jsLib + "/zepto.js")
    print "File Copied\nCopying Modernizr JS File"
    shutil.copyfile(archivePath + "/js/vendor/custom.modernizr.js", jsLib + "/custom.modernizr.js")
    print "File Copied\nCopying Foundation JS directory"
    shutil.copytree(archivePath + "/js/foundation", jsLib + "/foundation")
    print "Directory copied\nCopying Normalize CSS File"
    shutil.copyfile(archivePath + "/css/normalize.css", cssLib + "/normalize.css")
    print "File copied\nCopying Foundation Min CSS File"
    shutil.copyfile(archivePath + "/css/foundation.min.css", cssLib + "/foundation.min.css")
    print "File copied\nCopying Foundation CSS File"
    shutil.copyfile(archivePath + "/css/foundation.css", cssLib + "/foundation.css")
    print "File copied\n"
# Delete the archive and the directory
    print "Deleting Extracted Files"
    shutil.rmtree(archivePath)
    print "Files Deleted\nDeleting Archive"
    os.remove(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/foundation-4.3.2.zip")
    print "Archive Deleted"
    return True

    
#Download files
def downloadFile(type):
    global projectGlobal
    if type == 1:
# Jquery
        os.mkdir(projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js/lib")
        print "JS Lib Directory created"
        url = projectGlobal.getJquery()
        file_name = projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js/lib/" + url.split('/')[-1]
        if os.path.exists(file_name) == True:
            os.remove(file_name)
    elif type == 2:
        url = projectGlobal.getFoundation()
        file_name = projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/" + url.split('/')[-1]
        if os.path.exists(file_name) == True:
            os.remove(file_name)
    else:
        return False
# Launch the HTTP call and dowload the file
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    if (type == 2):
        return handleFoundationArchive()
    return True

# Symfony Checking
def symfonyChecking():
    global projectGLobal
    symfonyCheck = subprocess.call(["php", projectGlobal.getDirectory() + "/" + projectGlobal.getName() +"/app/check.php"])
    if symfonyCheck == 1:
        print "######## Your symfony installation is almost done"
        print "You just need to check the problems displayed above"
    return True;

# Welcome Message
print "**************** Python Symfony Project Installer ****************"
print "Welcome in the symfony project installer.\n"
print "This program will install a new symfony project in this directory : "
print (os.getcwd() + "\n")
print "The following steps will be followed :\n"
print "1. Checking and installation of composer"
print "2. Symfony installation"
print "3. Javascript framework installation"
print "4. Responsive HTML Framework installation\n"
print "5. Checking the installation"

# Ask user to continu
continueProj = askUser()
if continueProj == False:
    print "\nOkay, see you next time"
time.sleep(2)
# Step ONE
print "--------> Proceding with Step #1\n"
print "# Checking the system installs\n"
time.sleep(1)

# We launch the system's checks
continueProj = stepOneChecks()
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(50, "Step #1", "Installation Checked")
time.sleep(1)

# We launch the composer installation
print "# Checking the system installs\n"
continueProj = composerInstall()
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(100, "Step #1","Installation Composer")
time.sleep(1)

print "--------> Step #1 is Over\n"
time.sleep(2)

# Step TWO
print "--------> Proceding with Step #2\n"
print "# Symfony installation\n"
time.sleep(1)

#Project Name
continueProj = projectCaractHandler(1)
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(25, "Step #2", "Project Name")
print "Project Name : " + projectGlobal.getName()
time.sleep(1)

#Project Directory
continueProj = projectCaractHandler(2)
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(50, "Step #2", "Project Directory")
print "Project Directory : " + projectGlobal.getDirectory() + "/" + projectGlobal.getName()
time.sleep(1)


#Symfony Install
continueProj = symfonyInstall()
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(100, "Step #2", "Symfony Installation")
print "Project installed in : " + projectGlobal.getDirectory() + "/" + projectGlobal.getName()
time.sleep(1)


print "--------> Step #2 is Over\n"
time.sleep(2)

# Step THREE
print "--------> Proceding with Step #3\n"
print "# Jquery installation\n"
time.sleep(1)

# Jquery Install
continueProj = downloadFile(1)
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(100, "Step #3", "Jquery Installation")
print "Jquery Installed in : " + projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js/lib"
time.sleep(1)

print "--------> Step #3 is Over\n"
time.sleep(2)

# Step FOUR
print "--------> Proceding with Step #4\n"
print "# Foundation installation\n"
time.sleep(1)

# Foundation Install
continueProj = downloadFile(2)
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(100, "Step #4", "Foundation Installation")
print "Foundation Installed in : " + projectGlobal.getDirectory() + "/" + projectGlobal.getName() + "/web/js/lib"
time.sleep(1)

print "--------> Step #4 is Over\n"
time.sleep(2)

# Step FIVE
print "--------> Proceding with Step #5\n"
print "# Symfony Checking\n"
time.sleep(1)

# Symfony Checking
continueProj = symfonyChecking()
if continueProj == False:
    print "The installation program cannot complete"
print  progressPrint(100, "Step #5", "Symfony Checking")

print "--------> Step #5 is Over\n"
time.sleep(2)

print "Symfony is currently installed in " + projectGlobal.getDirectory() + "/" + projectGlobal.getName()
print "With the Following tools :\n* Jquery\n* Foundation"
print "Have fun making the web better"

print "Don't forget to add"
print "<script>\n\t$(document).foundation();\n</script>"
print "At the end of your body"

print "Please go to :\nhttp://symfony.com/\nhttp://foundation.zurb.com/\nFor help"
