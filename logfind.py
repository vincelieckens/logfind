# logfind_verbeterd.py
# Project explanation: http://projectsthehardway.com/
# A basic implementation of the linux grep command. The program will search for the given strings in files that are listed in a logfind.txt file. This file must be placed in the home directory! 
# By default the program will search for all the given strings in a file. If -o option is enabled, the program will return the file if one of the strings is present. 
# The results will be written to results.txt located in the current working directory.
# Completed on 30/10/15, revision on 07/11/15 completed
# Commentary on codereview.stackexchange => http://codereview.stackexchange.com/questions/109815/learn-projects-the-hard-way-logfind-project/109916#109916

import argparse
import os
import re
import unicodedata

def cl_handler():
    """
    Handles the command line input, with strings as the words to search    
    for in files and -o as optional argumen
    """
    
    parser = argparse.ArgumentParser(description="find strings inside files")
    parser.add_argument("strings", nargs = "*", help="The files will be searched according to this words")
    parser.add_argument("-o", action="store_true", help="This option resets the string1 AND string2 and string3 logic to a string1 OR string2 OR string3 search logic")
    args = parser.parse_args()
    return args.strings, args.o


def scan_logfind(logfind_dir):
    """
    Opens the logfind file and scans it for filenames 
    according to a regular expression (filename.extension). 
    Returns a generator with the filenames
    """
    
    with open(logfind_dir, "r") as logfind:
        regex = re.compile(r"^[\w,\s-]+\.[A-Za-z]+$")  
        for word in logfind.read().split():            
            if regex.match(word):
                yield word
    
    
def scan_directory(file):
    """Scans the computer for a specified file, 
    starting with the home directory. 
    Returns the absolute directory of the file
    """
    home = os.path.expanduser("~")
    for root, dirs, files in os.walk(home):
        for f in files:
            if f == file:        
               return os.path.join(root, f)


def file_contains_strings(file_path, strings, conjunction=all):
    """
    Checks whether the file contains the specified strings.
    The conjunction should be either the builtin function all()
    (the default) or any()
    """
    search = {text.lower(): False for text in strings}
    with open(file_path, "r") as f:
        for line in f:
            line = line.lower()
            for text, found in search.items():
                search[text] = found or (text in line)
            if conjunction(search.values()):
                return True
    return False
    
def normalize_caseless(string):
    """
    This function normalizes the string and sets it to lower letters
    """
    return unicodedata.normalize("NFKD", string.casefold())
    
        
def main():
    with open("results.txt", "a") as results:
        strings, or_option = cl_handler()
        strings = [normalize_caseless(string) for string in strings]       
        home = os.path.expanduser("~")
        logfiles = scan_logfind(r"{}\logfind.txt".format(home))          
        logfiles_dir = [scan_directory(logfile) for logfile in logfiles]
        for logfile_dir in logfiles_dir:
                if file_contains_strings(logfile_dir, strings, any if or_option else all):
                    results.write("{}\n".format(logfile_dir))
    print("Search complete. Results written to results.txt")

if __name__ == "__main__":
    main()

   
      


