import json
import argparsing
import functions
import os

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

def main():
    result_list = []
    path = os.getcwd()
    args = argparsing.parsing_argument()
    arg_obj = functions.init_obj(args
    )
    #file_path = checkings.get_file_path(arg_obj)
    #print(file_path)
    files_list = functions.get_files_path(arg_obj, path, result_list)
    if len(files_list) == 0:
        print("Can't find files, make sure file name and extention are valid")
        exit()
    #print(files_list)
    functions.find_str_get_nums(arg_obj.reg_exp, files_list)


if __name__ == "__main__":
    main()