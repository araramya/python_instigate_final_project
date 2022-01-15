import argparse
from curses.ascii import isdigit
from main import ArgsInfo
import json
import os



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
    return result_list
    
def get_avreage_list(num_list):
    '''
    this function return avreage value of list 
    '''
    return round(sum(num_list) / len(num_list), 1)

def create_json_report(dict_for_json, arg_obj, i):
    '''
    This function is for creating json file which will contain avreage values of searched words
    and save that value in json format in repdir
    '''
    file_name = arg_obj.file_pat + str(i) + "_report" + ".json"
    full_file_name = os.path.join(arg_obj.rep_dir, file_name)
    try:
        with open(full_file_name, "w") as outfile:
            json.dump(dict_for_json, outfile)
    except:
        print("Error with creating json report file or dumping dictionary")
        
def create_anomaly_report(anomal_values, arg_obj, j):
    '''
    this function works as create_json_report function
    it's create report for any anomal data and save it in json format
    int repdir
    '''
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
    '''
    this function check if numbers after searched words are anomal or not
    if it's not a number it it's anomal
    '''
    anomal_values = []
    for num in num_str_list:
        for char in num:
            if  not char.isdigit() and  char != '.':
                anomal_values.append(num)
                num_str_list.remove(num)
                break
        if(len(anomal_values) > 0):
            create_anomaly_report(anomal_values, arg_obj, j)
    return ([float(x) for x in num_str_list])


def find_str_get_nums(str_list, files_list, arg_obj):
    '''
    this function finds our words in file and if it find some get the right value 
    '''
    for j, myfile in enumerate(files_list):
        dict_for_json = {}
        for mystr in str_list:
            number_list = []
            try:
                fd = open(myfile, "r")
            except:
                print("Can't open file for reading, make suure you have valid file or permissions")
                exit()
            text = fd.read().split()
            for i, word in enumerate(text):
                if word == mystr:
                    number_list.append(text[i+1])
            value = get_avreage_list(check_anomaly(number_list, arg_obj, j))
            dict_for_json[mystr] = value 
        create_json_report(dict_for_json, arg_obj, j)