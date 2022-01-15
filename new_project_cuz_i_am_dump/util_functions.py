import argparse
from curses.ascii import isdigit
import json
import os
import glob
import fnmatch
from tracemalloc import start


class ArgsInfo:
    '''
    As I don't know which way user will choose to pass arguments to my progran
    I need some stucture to take arguments in both ways and save it somewhere
    for future use
    '''
    def __init__(self, reg_exp, rep_dir, file_pat, file_ext):
        self.reg_exp = reg_exp
        self.rep_dir = rep_dir
        self.file_pat = file_pat
        self.file_ext = file_ext
    def __str__(self):
        return f"{self.reg_exp} {self.rep_dir} {self.file_pat} {self.file_ext}"


def parsing_argument():
    '''
    This fuction take from command line 
    '''
    parser = argparse.ArgumentParser(prog = "File_parser", description = "Read the given file and find some numbers after some words")
    parser.add_argument("--confpath",metavar='confpath',
                        type=str, required=False, help="Path to configuration file")
    parser.add_argument("--regexp", metavar='regexp',
                         type=str, nargs = '+', required=False, help="List of words thet program must find")
    parser.add_argument("--repdir", metavar='repdir', type=str,
                        required=False, help="Path to where program will create report file")
    parser.add_argument("--filepat", metavar='filepat', type=str,
                        required=False, help="File name that program should find")
    parser.add_argument("--fileext", metavar='fileext', type=str,
                        required=False, help="File extention that program should find")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("Catched an Argument Error")
    
    return (args)

def check_arguments(args):
    '''
    As I don't know will user pass arguments with config file or wirhout
    I couldn't require conffile or other arguments, so this function just check
    which of parsing type choose user and does user parse arguments in the right way
    if yes it return True eles  False
    '''
    if (args.confpath and
        args.regexp is None and
        args.repdir is None and
        args.filepat is None and
        args.fileext is None ):
        return True

    elif (args.confpath is None and
          args.regexp and args.repdir and
          args.filepat and args.fileext):
          return True
    else:
        return False

def init_obj(args):
    '''
    This function just initiliazing class object and if everything is ok return it
    also this function check can the program open config_file and is config file written in
    the right way
    '''
    if(args.confpath is None):
        arg_obj = ArgsInfo(args.regexp, args.repdir, args.filepat, args.fileext)
        return arg_obj
    else:
        try:
            with open(args.confpath, "r") as myfile:
                json_data = json.load(myfile)
        except:
            print("Error with opening config file or loading json file.")
            exit()
        if len(json_data) != 4:
            print("Invalid configuration file")
        try:
            arg_obj = ArgsInfo(json_data["regexp"],json_data["repdir"],
                               json_data["filepat"], json_data["fileext"])
        except:
            print("Invalid configuration file")
            exit()
        return arg_obj

def get_files_path(arg_obj, start_dir):
    '''
    This function search return list of paths for files that program should find and read
    also it checks does user give us valid file name and extention
    '''
    files_for_searching = []
    root = start_dir
    for r,d,f in os.walk(start_dir):
        for file in f:
            if arg_obj.file_ext in file and arg_obj.file_pat in file:
                files_for_searching.append(os.path.join(root,file))
    if (len(files_for_searching) > 0):
        return files_for_searching
    else:
        print("Files not found")
        exit()