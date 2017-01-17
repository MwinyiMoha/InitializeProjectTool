#-------------------------------------------------------------------------------
# Name:        Initialize Project Tool
# Purpose:     Organize data sources and prepare overlays
# Author:      Mohammed Mwijaa
# Created:     15/01/2017
# Copyright:   (c) Mohammed Mwijaa 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import arcpy
import ToolSettings
import os

class initializeProject:
    def __init__(self):
        self.projectName=ToolSettings.setProjectName()
        self.projectSourceDirectory=ToolSettings.setSourceDirectory()
        self.projectWorkingDirectory=ToolSettings.setWorkingDirectory()
        self.projectDatabase=ToolSettings.createGDB()
        self.projectExtents=ToolSettings.createExtents()

    def copySourceFiles(self):
        """Copy Source Feature Classes from Source to the Working Directory. """
        pass

    def clipFeatures(self):
        """Clip Working Files Using Extents Feature Class"""
        pass

    def deleteRedundantFiles(self):
        """Remove Source Files After Clipping"""
        pass

def main():
    """Main Program"""
    initialize=initializeProject()
    initialize.copySourceFiles()
    initialize.clipFeatures()
    initialize.deleteRedundantFiles()

if __name__ == '__main__':
    main()
