import os
import sys

##
# @brief check if another instance of application is running
# based on pid file if pid in the file is running then
# application quits
def check_single_instance(pid_file):
    old_pid = 0
    try:
        ## file exists
        fp = open(pid_file, "rw")
        old_pid = int(fp.readline())    
        fp.close()                        
    except:
        ## doesnt exist
        pass

    ## check if the pid in file is running or not           
    if _check_pid(old_pid):
        print "Another instance is running. exit"
        sys.exit(1)
        
    fp = open(pid_file,"w")
    fp.write(str(os.getpid()))
    fp.close()

def _check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
    
