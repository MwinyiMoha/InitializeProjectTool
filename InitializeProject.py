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
import sys

env.overwriteOutput=True

class initializeProject:
    def __init__(self):
        self.projectTitle=ToolSettings.getProjectTitle()
        self.projectSourceDirectory=ToolSettings.setSourceDirectory()
        self.projectName=ToolSettings.setProjectName(self.projectTitle, self.projectSourceDirectory)
        self.projectWorkingDirectory=ToolSettings.setWorkingDirectory(self.projectName)
        self.projectDatabase=ToolSettings.createGDB(self.projectName, self.projectWorkingDirectory)

    def copySourceFiles(self):
        """Copy Source Feature Classes from Source to the Working Directory. """
        env.workspace=self.projectSourceDirectory
        dest=self.projectWorkingDirectory
        msg='Copying Source Files; \n'

        if os.path.exists(env.workspace):
            fcList=arcpy.ListFeatureClasses()
            for fc in fcList:
                outName='{}\{}'.format(dest,fc)
                arcpy.Copy_management(fc, outName)
            msg+=arcpy.GetMessages()
        else:
            raise ValueError('Invalid Directory Path')
        ToolSettings.dumpToLogFile(msg)

    def createExtents(self):
        """Create extents shapefile that will serve as the clip feature for the
        clipFeatures function. """

        env.workspace=self.projectWorkingDirectory
        msg='Creating County Extents; \n'
        fClass='County.shp'
        if os.path.exists(env.workspace):
            if arcpy.Exists(fClass):
                sqlExp="COUNTY='{}'".format(self.projectName)
                arcpy.MakeFeatureLayer_management(fClass,'fLayer')
                msg+=arcpy.GetMessages()+'\n'
                arcpy.SelectLayerByAttribute_management('fLayer', 'NEW_SELECTION', sqlExp)
                msg+=arcpy.GetMessages()+'\n'
                arcpy.CopyFeatures_management('fLayer', '{}_Extents'.format(self.projectName))
                msg+=arcpy.GetMessages()+'\n'
            else:
                raise TypeError('{} feature class not found'.format(fClass))
        else:
            raise ValueError('Invalid Directory Path: {}'.format(env.workspace))
        ToolSettings.dumpToLogFile(msg)


    def clipFeatures(self):
        """Clip Source Files Using Extents Feature Class"""
        msg='Clipping Features \n'
        env.workspace=self.projectWorkingDirectory
        if os.path.exists(env.workspace):
            inFeatures='{}_Extents.shp'.format(self.projectName)
            if arcpy.Exists(inFeatures):
                arcpy.MakeFeatureLayer_management(inFeatures, 'Extents_Layer')
                fcList=arcpy.ListFeatureClasses()
                for fc in fcList:
                    if fc==inFeatures or fc=='County.shp':
                        continue
                    else:
                        arcpy.MakeFeatureLayer_management(fc, 'Layer')
                        arcpy.Clip_analysis('Layer', 'Extents_Layer', '{}\{}_clip'.format(env.workspace,fc[:-4]))
                        msg+=arcpy.GetMessages()
            else:
                raise ValueError('Feature Class Not Found: {}'.format(inFeatures))
        else:
            raise ValueError('Directory Not Found: {}'.format(env.workspace))
        ToolSettings.dumpToLogFile(msg)


    def deleteRedundantFiles(self):  #Untested function
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
                    elif fc=='{}_Extents'.format(self.projectName):
                        continue
                    else:
                        arcpy.Delete_management(fc)
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
    initialize.createExtents()
    initialize.clipFeatures()
    initialize.deleteRedundantFiles()

if __name__ == '__main__':
    main()
