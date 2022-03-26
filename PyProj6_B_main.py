"""
This script uses multiprocessing to increase the speed at which it clips objects. 
The worker function is imported from PyProj6_A_support. It also uses the time module
to display how long it takes for the process to complete.

This is one of two scripts that accomplishes the same function; this script takes
hard-coded folder paths and clips multiple featuer classes against the clipper.  

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""
import os, sys
import arcpy 
import multiprocessing 
from PyProj6_B_support import worker

import time 
process_start_time = time.time() 

# overwrites the output from previous runs to give new dataset
arcpy.env.overwriteOutput = True

workspace = r""
arcpy.env.workspace = workspace

# Input parameters
clipper = r""                                   # Path to feature class that clips
tobeclipped = []
outputFolder = r""                              # Path to output folder
fcList = arcpy.ListFeatureClasses()

updatedClipper = os.path.basename(os.path.splitext(clipper)[0])

for fc in fcList:
    if fc != updatedClipper:
        tobeclipped.append(fc)

def get_install_path():
    ''' Return 64bit python install path from registry (if installed and registered),
        otherwise fall back to current 32bit process install path.
    '''
    if sys.maxsize > 2**32: return sys.exec_prefix #We're running in a 64bit process
  
    #We're 32 bit so see if there's a 64bit install
    path = r'SOFTWARE\Python\PythonCore\2.7'
  
    from _winreg import OpenKey, QueryValue
    from _winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY
  
    try:
        with OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_READ | KEY_WOW64_64KEY) as key:
            return QueryValue(key, "InstallPath").strip(os.sep) #We have a 64bit install, so return that.
    except: return sys.exec_prefix #No 64bit, so return 32bit path 
    
def mp_handler():
 
    try: 
        # Create a list of object IDs for clipper polygons 
         
        arcpy.AddMessage("Creating Polygon OID list...") 
        print("Creating Polygon OID list...") 
        clipperDescObj = arcpy.Describe(clipper) 
        field = clipperDescObj.OIDFieldName 
      
        idList = [] 
        with arcpy.da.SearchCursor(clipper, [field]) as cursor: 
            for row in cursor: 
                id = row[0] 
                idList.append(id)
 
        arcpy.AddMessage("There are " + str(len(idList)) + " object IDs (polygons) to process.") 
        print("There are " + str(len(idList)) + " object IDs (polygons) to process.") 
 
        # Create a task list with parameter tuples for each call of the worker function. Tuples consist of the clippper, tobeclipped, field, and oid values.
        
        jobs = []
        
     
        for id in idList:
            for fc in tobeclipped:
                jobs.append((clipper,fc,field,id, outputFolder)) # adds tuples of the parameters that need to be given to the worker function to the jobs list
 
        arcpy.AddMessage("Job list has " + str(len(jobs)) + " elements.") 
        print("Job list has " + str(len(jobs)) + " elements.") 
 
        # Create and run multiprocessing pool.

        multiprocessing.set_executable(os.path.join(get_install_path(), 'pythonw.exe')) # make sure Python environment is used for running processes, even when this is run as a script tool
 
        arcpy.AddMessage("Sending to pool") 
        print("Sending to pool") 
 
        cpuNum = multiprocessing.cpu_count()  # determine number of cores to use
        print("there are: " + str(cpuNum) + " cpu cores on this machine") 
  
        with multiprocessing.Pool(processes=cpuNum) as pool: # Create the pool object 
            res = pool.starmap(worker, jobs)  # run jobs in job list; res is a list with return values of the worker function
 
        # If an error has occurred report it 
         
        failed = res.count(False) # count how many times False appears in the list with the return values
        if failed > 0:
            arcpy.AddError("{} workers failed!".format(failed)) 
            print("{} workers failed!".format(failed)) 
         
        arcpy.AddMessage("Finished multiprocessing!") 
        print("Finished multiprocessing!") 
 
    except arcpy.ExecuteError:
        # Geoprocessor threw an error 
        arcpy.AddError(arcpy.GetMessages(2)) 
        print("Execute Error:", arcpy.ExecuteError) 
    except Exception as e: 
        # Capture all other errors 
        arcpy.AddError(str(e)) 
        print("Exception:", e)
 
if __name__ == '__main__':   
    mp_handler() 
    
# Output how long the whole process took at the end of the process. 
arcpy.AddMessage("--- %s seconds ---" % (time.time() - process_start_time)) 
print ("--- %s seconds ---" % (time.time() - process_start_time))
