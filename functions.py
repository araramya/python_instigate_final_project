import argparse
from curses.ascii import isdigit
from main import ArgsInfo
import json
import os

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


def get_files_path(arg_obj, path, result_list):
    '''
    This function search return list of paths for files that program should find and read
    also it checks does user give us valid file name and extention
    '''
    files_list = os.listdir(path)
    for file_name in files_list:
        file_ab_path = os.path.join(path, file_name)
        if os.path.isdir(file_ab_path):
            get_files_path(arg_obj, file_ab_path, result_list)
        else:
            if file_name == arg_obj.file_pat + arg_obj.file_ext:
                result_list.append(file_ab_path)
    # if len(result_list) == 0:
    #     print("Can't find file, make sure file name and extention is valid")
    #     exit()
    return result_list
    

    # path = os.getcwd()
    # file_name = arg_obj.file_pat + arg_obj.file_ext

    # for root, dirs, files in os.walk(path):
    #     if file_name in files:
    #         file_path = os.path.join(root, file_name)
    #         return file_path
    # print("Can't find file, make sure file name and extention is valid")
    # exit()
def get_avreage_list(num_list):
    return round(sum(num_list) / len(num_list), 1)

def create_json_report(dict_for_json, arg_obj, i):
        print(dict_for_json)
        file_name = arg_obj.file_pat + str(i) + "_report" + ".json"
        full_file_name = os.path.join(arg_obj.rep_dir, file_name)

        #full_file_name = arg_obj.rep_dir + file_name
        print(full_file_name)
        try:
            with open(full_file_name, "w") as outfile:
                json.dump(dict_for_json, outfile)
        except:
            print("Error with creating json report file or dumping dictionary")
        
def create_anomaly_report(anomal_values, arg_obj, j):
    dict_for_json = {}
    for i, elem in enumerate(anomal_values):
        dict_for_json[i] = elem
    file_name = arg_obj.file_pat + str(j) + "_anomaly.json"
    full_file_name = os.path.join(arg_obj.rep_dir, file_name)
    try:
        with open(full_file_name, "w") as outfile:
            json.dump(dict_for_json, outfile)
    except:
        print("Error with creaeting json anomal report file or dumping dictionary")



def check_anomaly(num_str_list, arg_obj, j):
    anomal_values = []
    for num in num_str_list:
        for char in num:
            if  not char.isdigit() and  char != '.':
                anomal_values.append(num)
                num_str_list.remove(num)
                break
        if(len(anomal_values) > 0):
            create_anomaly_report(anomal_values, arg_obj, j)
    print([float(x) for x in num_str_list])
    return ([float(x) for x in num_str_list])


def find_str_get_nums(str_list, files_list, arg_obj):
    for j, myfile in enumerate(files_list):
        dict_for_json = {}
        for mystr in str_list:
            number_list = []
            print(mystr)
            try:
                fd = open(myfile, "r")
            except:
                print("Can't open file for reading, make suure you have valid file or permissions")
                exit()
            text = fd.read().split()
            for i, word in enumerate(text):
                if word == mystr:
                    print(text[i], text[i + 1])
                    number_list.append(text[i+1])
            
            print(number_list)
            value = get_avreage_list(check_anomaly(number_list, arg_obj, j))
            dict_for_json[mystr] = value 
        create_json_report(dict_for_json, arg_obj, j)
        #print (dict_for_json)

    # for myfile in files_list:
    #     for mystr in str_list:
    #        # print("hifromfirst for")
    #         try:
    #             fd = open(myfile, "r")      
    #         except:
    #             print("Can't open file for reading, make sure you have valid file or permissions")
    #             exit()
    #         for line_num, line in enumerate(fd):
    #             #if mystr in line:
    #             line_splitted = line.split()
    #             for i, w in enumerate(line_splitted):
    #                 if w == mystr:
    #                     print(line_splitted[i + 1])
    #                     print("line_num ", line_num) 
    #         fd.close()
