#-------------------------------------------------------------------------------
# Name:        Initialize Project Tool
# Purpose:     Organize data sources and prepare overlays
# Author:      Mohammed Mwijaa
# Created:     07/12/2016
# Copyright:   (c) Mohammed Mwijaa 2016
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
        self.projectTitle=ToolSettings.setProjectTitle()
        self.projectSourceDirectory=ToolSettings.setSourceDirectory()
        self.projectName=ToolSettings.setProjectName(self.projectTitle, self.projectSourceDirectory)
        self.projectWorkingDirectory=ToolSettings.setWorkingDirectory(self.projectName)
        self.projectDatabase=ToolSettings.createGDB(self.projectName, self.projectWorkingDirectory)

    def copySourceFiles(self):
        """Copy Source Feature Classes from Source to the Working Directory. """

        msg='Copying Source Files... \n'
        print(msg)

        env.workspace=self.projectSourceDirectory
        dest=self.projectDatabase
        if os.path.exists(env.workspace):
            fcList=arcpy.ListFeatureClasses()
            for fc in fcList:
                outName=os.path.join(dest, fc[:-4])
                arcpy.MakeFeatureLayer_management(fc, 'Layer')
                arcpy.CopyFeatures_management('Layer', outName)
                msg+=arcpy.GetMessages()
        else:
            raise ValueError('Invalid Directory Path')
        ToolSettings.dumpToLogFile(msg)

    def createExtents(self):
        """Create extents shapefile that will serve as the clip feature for the
        clipFeatures function. """

        msg='Creating County Extents... \n'
        print(msg)

        env.workspace=self.projectDatabase
        fc=sys.argv[3].split('.')[0]
        if os.path.exists(env.workspace):
            if arcpy.Exists(fc):
                sqlExp="COUNTY='{}'".format(self.projectName)
                arcpy.MakeFeatureLayer_management(fc,'fLayer')
                msg+=arcpy.GetMessages()+'\n'
                arcpy.SelectLayerByAttribute_management('fLayer', 'NEW_SELECTION', sqlExp)
                msg+=arcpy.GetMessages()+'\n'
                arcpy.CopyFeatures_management('fLayer', '{}_Extents'.format(self.projectName))
                msg+=arcpy.GetMessages()+'\n'
            else:
                raise TypeError('Feature Class Not Found: {}'.format(fc))
        else:
            raise ValueError('Invalid Directory Path: {}'.format(env.workspace))
        ToolSettings.dumpToLogFile(msg)


    def clipFeatures(self):
        """Clip Source Files Using Extents Feature Class"""

        msg='Clipping Features... \n'
        print(msg)

        env.workspace=self.projectDatabase
        if os.path.exists(env.workspace):
            inFeatures='{}_Extents'.format(self.projectName)
            if arcpy.Exists(inFeatures):
                arcpy.MakeFeatureLayer_management(inFeatures, 'Extents_Layer')
                fcList=arcpy.ListFeatureClasses()
                for fc in fcList:
                    if fc==inFeatures or fc=='County':
                        continue
                    else:
                        arcpy.MakeFeatureLayer_management(fc, 'Layer')
                        arcpy.Clip_analysis('Layer', 'Extents_Layer', '{}\{}_clip'.format(env.workspace,fc))
                        msg+=arcpy.GetMessages()
            else:
                raise ValueError('Feature Class Not Found: {}'.format(inFeatures))
        else:
            raise ValueError('Directory Not Found: {}'.format(env.workspace))
        ToolSettings.dumpToLogFile(msg)


    def deleteRedundantFiles(self):
        """Remove Source Files After Clipping"""

        msg='Deleting Redundant Files... \n'
        print(msg)

        env.workspace=self.projectDatabase
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
        ToolSettings.dumpToLogFile(msg)


def main():
    """Main Program"""
    initialize=initializeProject()
    initialize.copySourceFiles()
    initialize.createExtents()
    initialize.clipFeatures()
    initialize.deleteRedundantFiles()


if __name__ == '__main__':
    if len(sys.argv)==4:
        if sys.argv[1].isalpha and sys.argv[2].isalpha:
            main()
        else:
            raise ValueError('Provide Valid Title and Directory Name')
    else:
        raise ValueError('Tools Takes Three Parameters: Title, Source Directory and Counties Feature Class')
