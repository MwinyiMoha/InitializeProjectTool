# InitializeProjectTool

ABOUT THE TOOL
-----------------------
The Initialize Project Tool is a basic tool for automating preparation of overlays and feature classes for a particular 
region. It is written in Python 2.7 using ESRI's ArcPy Site Package which enables access to a plethora of geoprocessing
functionality of ArcGIS. Currently, the focus is on Kenya and her 47 counties. I realized i was spending too much time 
clipping Kenya datasets with County extents to prepare overlays for a certain County-say i got about 30 feature classes 
of Kenya data such as roads, forests, water bodies, schools, parks etc. So, i thought why not write a script that will do 
that for me while i dwell on other things. With this tool, all i have to do is enter the name of the County and specify 
the source directory which holds data. The tool does the rest.

TOOL LAYOUT
-----------------------
The tool features two files:

1. Main Class File
   The tool file that contains the Initialize Project Class and the main program. It contains functions that carry out the 
   geoprocessing tasks. The class organizes the tool into properties and methods while the main programme initializes the
   class and implements the tool workflow.

		Class Properties
	----------------------------------
	***projectName
	***projectSourceDirectory
	***projectWorkingDirectory
	
		Class Methods
	---------------------------------
	***copySourceFiles
	***createGDB
	***createExtents
	***clipFeatures
	***deleteRedundantFiles
	
2. Tool Settings  Module
   As the name suggests, it is a settings module for the tool. It contains functions that return paths and settings to 
   the main class file. It also contains the unique dumpToLogFile function which actually does something rather than 
   simply returning parameters. It is explicitly called to write log files.

		Module Functions
	---------------------------------
   	***dumpToLogFile
   	***setProjectName
   	***setSourceDirectory
   	***setWorkingDirectory
	
    Help on the functions is available with the Python 'help' function. For Example:
		>>>import ToolSettings
		>>>help(ToolSettings.dumpToLogFile)

TOOL WORKFLOW
-----------------------
The workflow implements a basic algorithm that can be illustrated by the following steps. However, this is subject to
change as i venture to make the tool better and better.
	~Set the project name
	~Set source directory
	~Set working directory
	~Create project geodatabase
	~Copy source files
	~Create County Extents
	~Clip features
	~Delete redundant files

