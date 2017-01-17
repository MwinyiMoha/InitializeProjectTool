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

def setProjectName():
    """Enter name of the intended project. Note that Project Names SHOULD NOT
    be 'Null', 'None', Empty strings or have spaces and periods within the name.
    Hyphens and Underscores are allowed. """
    pass

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

def createGDB():
    """Create personal geodatabase that will be the tool's main workspace. All
    feature classes and tables will be housed in the geodatabase"""
    pass

def createExtents():
    """Create extents shapefile that will serve as the clip feature for other
    functions. Extent parameters are also given. """
    pass
