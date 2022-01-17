import argparse
from collections import defaultdict
from curses.ascii import isdigit
import json
from operator import sub
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
        if os.path.basename(arg_obj.rep_dir) in d:
            d.remove(os.path.basename(arg_obj.rep_dir))
        for file in f:
            if arg_obj.file_ext in file and arg_obj.file_pat in file:
                files_for_searching.append(os.path.join(r,file))
    if (len(files_for_searching) > 0):
        return files_for_searching
    else:
        print("Files not found")
        exit()

def is_float_digit(num_str):
    dot_count = 0
    for character in num_str:
        if not character.isdigit() and character != '.':
            return False
        if character == '.':
            dot_count += 1
    if dot_count > 1:
        return False
    return True

def avg(my_list):
    return sum(my_list) / len(my_list)

def create_json_file(file_path, file_num, dict_for_report, arg_obj):
    file_name = os.path.basename(file_path) + ".report" + str(file_num) + ".json"
    file_ab_path = os.path.join(arg_obj.rep_dir, file_name)
    try:
        with open(file_ab_path, "w") as outfile:
            json.dump(dict_for_report, outfile)
    except:
        print("Can't create report file or dump dictionary")
        exit()
    return 0

def create_anom_file(file_path, file_num, dict_anom, arg_obj):
    file_name = os.path.basename(file_path) + ".anom" + str(file_num) + ".json"
    file_ab_path = os.path.join(arg_obj.rep_dir, file_name)
    try:
        with open(file_ab_path, "w") as outfile:
            json.dump(dict_anom, outfile)
    except:
        print ("Can't create anomaly report file or dump dictionary")
        exit()
    return 0
            
def create_all_report(file_path, file_num, dict_maxminvg, arg_obj):
    file_name = os.path.basename(file_path) + ".all_report" + str(file_num) + ".json"
    file_ab_path = os.path.join(arg_obj.rep_dir, file_name)
    try:
        with open(file_ab_path, "w") as outfile:
            json.dump(dict_maxminvg, outfile)
    except:
        print ("Can't create all_report file or dump dictionart")
        exit()
    return 0

def get_dict_of_nums(arg_obj, files_list):
    str_list = arg_obj.reg_exp
    for file_num, file in enumerate(files_list):
        dict_for_report = {}
        dict_anomal = {}
        dict_maxminavg = {}
        for mystr in str_list:
            list_maxminavg = []
            dict_for_report[mystr] = {}
            dict_anomal[mystr] = {}
            dict_maxminavg[mystr] = {}
            try:
                fd = open(file, "r")
            except:
                print("Can't open file for reading")
                exit()
            for line_num,line in enumerate(fd):
                if "Path" in line: #Ask how to find subspaces in file it'st hardcoding and I don't like it
                    nums_of_subspace = []
                    temp_line = line.strip("\n")
                    for line in fd:
                        line_sp = line.split()
                        if mystr in line_sp:
                            id = line_sp.index(mystr)
                            num_count = 0
                            while id < len(line_sp):
                                if is_float_digit(line_sp[id]):
                                    nums_of_subspace.append(float(line_sp[id]))
                                    list_maxminavg.append(float(line_sp[id]))
                                    num_count += 1
                                id += 1
                            if(num_count == 0):
                                dict_anomal[mystr][temp_line] = "ErrorInSubSpace"
                        if len(line) == 1:
                            break
                    if len(nums_of_subspace) != 0:
                        dict_for_report[mystr][temp_line] = avg(nums_of_subspace)
            fd.close()
            if(len(list_maxminavg) != 0 ):
                dict_maxminavg[mystr] = dict(zip(["max", "min", "avg"],[max(list_maxminavg), min(list_maxminavg), avg(list_maxminavg)]))
        create_json_file(file, file_num, dict_for_report, arg_obj)
        create_anom_file(file, file_num, dict_anomal, arg_obj)
        create_all_report(file, file_num, dict_maxminavg, arg_obj)
    