#-------------------------------------------------------------------------------
# Name:        Initialize Project Tool
# Purpose:     Organize data sources and prepare overlays
# Author:      Mohammed Mwijaa
# Created:     15/01/2017
# Copyright:   (c) Mohammed Mwijaa 2017
# Status:      <Draft>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import ToolSettings
import os

class initializeProject:
    def __init__(self):
        self.projectName=ToolSettings.setProjectName()
        self.projectSourceDirectory=ToolSettings.setSourceDirectory()
        self.projectWorkingDirectory=ToolSettings.setWorkingDirectory()
        #self.projectLogFile=ToolSettings.setLogFile()

    def copySourceFiles(self):
        """Copy Source Feature Classes from Source to the Working Directory. """
        env.workspace=self.projectSourceDirectory
        msg='Starting Log For copySourceFiles; \n'
        try:
            if os.path.exists(env.workspace):
                fcList=arcpy.ListFeatureClasses()
                for fc in fcList:
                    outName='{}\{}.{}'.format(self.projectWorkingDirectory,fc,'shp')
                    arcpy.Copy_management(fc, outName)
                msg+=arcpy.GetMessages()
            else:
                raise ValueError('Invalid Directory Path')
        except ValueError as e:
            msg+=str(e)
        ToolSettings.dumpToLogFile(msg)

    def createGDB(self):
        """Create personal geodatabase that will be the tool's main workspace.
        All feature classes and tables will be housed in the geodatabase"""

        env.workspace=self.projectWorkingDirectory
        msg='Starting Log For createGDB; \n'

        try:
            if os.path.exists(env.workspace):
                dbName='{}GDB'.format(self.projectName)
                arcpy.CreatePersonalGDB_management(env.workspace, dbName, 'CURRENT')
                msg+=arcpy.GetMessages()
            else:
                raise ValueError('Invalid Directory Path')
        except ValueError as e:
            msg+=str(e)
        ToolSettings.dumpToLogFile(msg)


    def createExtents(self):
        """Create extents shapefile that will serve as the clip feature for other
        functions. Extent parameters are also given. """

        env.workspace=self.projectWorkingDirectory
        msg='Starting Log For createExtents; \n'
        fClass='Kenya_Counties'

        try:
            if os.path.exists(env.workspace):
                if arcpy.Exists(fClass):
                    sqlExp="NAME='{}'".format(self.projectName)
                    fLayer=arcpy.MakeFeatureLayer_management(fClass)
                    arcpy.SelectLayerByAttribute_management(fLayer, 'NEW_SELECTION', sqlExp)
                    arcpy.CopyFeatures_management(fLayer, 'CountyExtents')
                    msg+=arcpy.GetMessages()
                else:
                    raise arcpy.AddError('{} feature class not found'.format(fClass))
                    msg+=arcpy.GetMessages(2)
            else:
                raise ValueError('Invalid Directory Path')
        except ValueError as e:
            msg+=str(e)
        ToolSettings.dumpToLogFile(msg)


    def clipFeatures(self):
        """Clip Working Files Using Extents Feature Class"""
        env.workspace=self.projectWorkingDirectory
        msg='Starting Log For clipFeatures; \n'
        try:
            if os.path.exists(env.workspace):
                fcList=arcpy.ListFeatureClasses()
                for fc in fcList:
                    if fc=='countyExtents':
                        continue
                    else:
                        arcpy.Clip_analysis(fc, 'countyExtents',fc+'_clip')
                msg+=arcpy.GetMessages()
            else:
                raise ValueError('Invalid Directory Path')
        except ValueError as e:
            msg+=str(e)
        ToolSettings.dumpToLogFile(msg)

    def deleteRedundantFiles(self):
        """Remove Source Files After Clipping"""
        env.workspace=self.projectWorkingDirectory
        msg='Starting Log For deleteRedundantFiles; \n'
        try:
            if os.path.exists(env.workspace):
                fcList=arcpy.ListFeatureClasses()
                for fc in fcList:
                    suffix=fc[-5:]
                    if suffix=='_clip':
                        continue
                    else:
                        arcpy.Delete_management(fc) #will delete 'county extents', deal with it
                msg+=arcpy.GetMessages()
            else:
                raise ValueError('Invalid Directory Path')
        except ValueError as e:
            msg+=str(e)
        ToolSettings.dumpToLogFile(msg)


def main():
    """Main Program"""
    initialize=initializeProject()
    initialize.copySourceFiles()
    initialize.createGDB()
    initialize.createExtents()
    initialize.clipFeatures()
    initialize.deleteRedundantFiles()

if __name__ == '__main__':
    main()
