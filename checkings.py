import argparse
from main import ArgsInfo
import json

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
    if (check_arguments(args)):
        if(args.confpath is None):
            arg_obj = ArgsInfo(args.regexp, args.repdir, args.filepat, args.fileext)
            return arg_obj
        else:
            try:
                with open(args.confpath, "r") as myfile:
                    json_data = json.load(myfile)
            except:
                print("Error with opening config file")
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
