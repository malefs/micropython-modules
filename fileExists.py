# Source: https://forum.micropython.org/viewtopic.php?t=4245

from uos import stat

def check(fileName):
    try:
        stat(fileName)
        #print("File found!")
        return True
    except OSError:
        #print("No file found!")
        return False

# import fileExists
# fileExists.check('boot.py')
