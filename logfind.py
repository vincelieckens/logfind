# logfind.py
# Project explanation: http://projectsthehardway.com/
# A basic implementation of the linux grep command. The program will search for the given strings in files that are listed in a logfind.txt file. 
# By default the program will search for all the given strings in a file. If -o option is enabled, the program will return the file if one of the strings is present. 
# The results will be written to results.txt located in the current working directory.

import argparse
import os
import re

def cl_handler():
    """
    Handles the command line input, with strings as the words to search for in files, and -o as optional argument
    """
    
    parser = argparse.ArgumentParser(description="find strings inside files")
    parser.add_argument("strings", nargs = "*", help="The files will be searched according to this words")
    parser.add_argument("-o", action="store_true", help="This option resets the string1 AND string2 and string3 logic to a string1 OR string2 OR string3 search logic")
    args = parser.parse_args()
    return args.strings, args.o


def scan_logfind(logfind_dir):
    """
    Opens the logfind file and scans it for filenames according to a regular expression (filename.extension). 
    Returns a list with the filenames
    """
    files = []
    with open(logfind_dir, "r") as logfind:
        regex = re.compile(r"^[\w,\s-]+\.[A-Za-z]+$")  
        for word in logfind.read().split():            
            file = regex.match(word)
            if file:
                files.append(word)
    return files
    
    
def scan_directory(file):
    """
    Scans the computer for a specified file, starting with the home directory. 
    Returns the absolute directory of the file
    """
    home = os.path.expanduser("~")
    for root, dirs, files in os.walk(home):
        for f in files:
            if f == file:        
               file_directory = os.path.join(root, f)
               return file_directory


def search_strings(file_dir, strings, or_option=False):
    """
    Searches the file for the specified files. Returns boolean true if all strings are found in the file
    If the or_option is enabled the function will return boolean true if one string is found in the file.
    """
    with open(file_dir, "r") as logfile:
        logfile = logfile.read().lower()
        results = []
        for string in strings:
            if string in logfile:
                results.append("True")
            else:
                results.append("False")
                
    if or_option:
        for result in results:
            if result == "True":
                return True
        return False
    else:
        for result in results:
            if result == "False":
                return False
        return True
        
        
def main():
    """ 
    main 
    """
    results = open("results.txt", "w")
    strings, or_option = cl_handler()                 
    logfind = scan_directory("logfind.txt")          
                                                  
    logfiles = scan_logfind(logfind)
    logfiles_dir = []        
    for logfile in logfiles:
        logfiles_dir.append(scan_directory(logfile))
    for logfile_dir in logfiles_dir:
            if search_strings(logfile_dir, strings, or_option):
                results.write("{}\n".format(logfile_dir))
    print("Search complete. Results written to results.txt")

if __name__ == "__main__":
    main()

   
      


