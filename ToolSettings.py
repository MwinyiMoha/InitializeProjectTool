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

def dumpToLogFile(msg):
    """
    Write out tool geoprocessing messages to a Log File. This function will
    be called by each other function to make sure that messages of all severity
    are written to a log file.

        INPUTS:
            msg(string):
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


def setProjectName():
    """Enter name of the intended project. Note that Project Names SHOULD NOT
    be 'Null', 'None', Empty strings or have spaces and periods within the name.
    Hyphens and Underscores are allowed. """

    projectName='Homa Bay' #change to capture user input
    env.workspace=setSourceDirectory.sourceDir
    fClass='Kenya_Counties'
    msg='Starting Log For setProjectName;'
    try:
        if arcpy.Exists(fClass):
            with arcpy.da.SearchCursor(fClass, 'NAME') as cursor:
                for i in cursor:
                    if i==projectName:
                        msg+='{} is a valid county'.format(projectName)
                    else:
                        arcpy.AddError('{} is not a valid county'.format(projectName))
                        msg+=arcpy.GetMessages(2)
        else:
            raise TypeError('{} feature class not found'.format(fClass))
    except TypeError as e:
        msg+=str(e)
    dumpToLogFile(msg)
    return projectName


def setSourceDirectory():
    """Navigate to the local directory holding source data. As good practice, we
    copy the original files to a working directory so that the original data is
    not corrupted just in case something goes wrong. """
    pass

def setWorkingDirectory():
    """Navigate to the local folder that will hold working files. These will be
    copied from the source files and analyses done. The folder will also house
    the working Geodatabase. The folder should be created in advance."""
    pass
