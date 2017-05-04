#-------------------------------------------------------------------------------
# Name:        Tool Settings
# Purpose:     Settings Module For The Initialize Project Tool
# Author:      Mohammed Mwijaa
# Created:     15/01/2017
# Copyright:   (c) Mohammed Mwijaa 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import os


def getProjectTitle():#check for numeric
    """
    Prompt the user to enter a title for the intended project. This will be
    validated by setProjectName function to become the project name. Function
    returns a string that represents the Project Title.

    getProjectTitle()
        INPUTS:
            None

    *Use 'input' instead of 'raw_input' for Python 3.x
    """
    msg='Setting Project Title: \n'
    char=[',',':',';','/','.','']
    projectTitle=str(raw_input('Name: '))
    if projectTitle=='':
        raise ValueError('Title Cannot Be Empty')
    else:
        for i in projectTitle:
            for ii in char:
                if i==ii:
                    raise ValueError('Title Cannot Contain {}'.format(ii))
    msg+='"{}" Set As Project Title'.format(projectTitle)
    dumpToLogFile(msg)
    return projectTitle

def setSourceDirectory():
    """
    Prompt the user to enter a path that holds the project's source files. This
    will provide the workspace for the copySourceFiles function. Function returns
    a string that represents the source directory path.

    setSourceDirectory()
        INPUTS:
            None

    *Use 'input' instead of 'raw_input' for Python 3.x
    """
    sourceDir=str(raw_input('Source Dir: '))#check if empty
    msg='Setting Project Source Directory: \n'
    if os.path.exists(sourceDir):
        msg+='"{}" is a valid directory \n'.format(os.path.abspath(sourceDir))
    else:
        raise ValueError('Directory Not Found: "{}"'.format(os.path.abspath(sourceDir)))
    dumpToLogFile(msg)
    return sourceDir


def setProjectName(Title, Path):
    """
    Set the name of the intended project. Note that Project Names SHOULD be
    valid County names in Kenya. Fuction returns a python string representing
    the validated project name.

    setProjectName(Title, Path)
        INPUTS:
            Title(string):
                The Project Title string returned by the getProjectTitle function.
                This will be validated using a list of valid County names in
                Kenya.
            Path(string):
                The path to the source directory containing the counties feature
                class. Names in the attribute table will be used for validation.
    """
    env.workspace=Path
    projectName=unicode(Title.capitalize())
    msg='Setting Project Name: \n'
    if os.path.exists(env.workspace):
        fc='County.shp' #remove hardcoded file
        if arcpy.Exists(fc):
            with arcpy.da.SearchCursor(fc, ['COUNTY']) as cursor:
                try:
                    for row in cursor:
                        if row[0]==projectName:
                            msg+='{} Set As Project Name \n'.format(projectName)
                            return projectName
                except:
                    return None
        else:
            raise ValueError('Feature Class NOT found: {}'.format(fc))
    else:
        raise ValueError('Invalid Directory Path: {}'.format(env.workspace))
    dumpToLogFile(msg)


def setWorkingDirectory(Name):
    """
    Create the directory that will hold working files. These will be
    copied from the source directory and analyses done. The directory will also house
    the working Geodatabase. Function returns a string that represents the path
    to the working directory.

    setWorkingDirectory(Name)
        INPUTS:
            Name(string):
                The validated project name returned by setProjectName. The created
                directory will bear the same name as the project.

    *Working directory will be generated on the desktop for starters. Further
    improvements shall be made.
    """

    msg='Creating the working directory: \n'
    if Name==None:
        raise ValueError('Provide A Valid County Name')

    userName=os.environ.get('USERNAME')
    workDir=r'C:\Users\{}\Desktop\{}'.format(userName, Name)
    try:
        os.mkdir(workDir)
        msg+='Working directory successfully created \n'
        msg+='"{}" set as working directory'.format(workDir)
    except WindowsError, e:
        raise e
    dumpToLogFile(msg)
    return workDir

def createGDB(Name, Path):
    """
    Create personal geodatabase that will be the tool's main workspace.All
    feature classes and tables-after clipping-will be housed in the
    geodatabase. Function returns a string that represents the path to the
    geodatabase.

    createGDB(Name, Path)
        INPUTS:
            Name(string):
                The validated project name returned by setProjectName. The created
                geodatabase will bear the same name as the project.
            Path(string):
                The path to the working directory to house the geodatabase.
    """
    msg='Creating the project Database \n'
    env.workspace=Path
    if os.path.exists(env.workspace):
        dbPath=arcpy.CreatePersonalGDB_management(Path, Name, 'CURRENT')
        msg+=arcpy.GetMessages()
    else:
        raise ValueError('Directory Not Found: {}'.format(os.path.abspath(env.workspace)))
    dumpToLogFile(msg)
    return str(dbPath)


def dumpToLogFile(msg):
    """
    Write out tool geoprocessing messages to a Log File. This function will
    be called by each other function to make sure that messages of all severity
    are written to a log file.

    dumpToLogFile(Message)
        INPUTS:
            Message(string):
                Cross severity messages passed by each individual function.
    """
    try:
        if msg=='':
            raise ValueError('No Message Received') #change this to arcpy warning
        else:
            tFile=open('test.txt', 'a')
            tFile.write('\n'+msg)
            tFile.close()
    except ValueError as e:
        print(e)
