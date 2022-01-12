import json
import argparsing
import checkings

class ArgsInfo:
    def __init__(self, reg_exp, rep_dir, file_pat, file_ext):
        self.reg_exp = reg_exp
        self.rep_dir = rep_dir
        self.file_pat = file_pat
        self.file_ext = file_ext
    def __str__(self):
        return f"{self.reg_exp} {self.rep_dir} {self.file_pat} {self.file_ext}"

def main():
    args = argparsing.parsing_argument()
    arg_obj = checkings.init_obj(args)
    
    
    # if (checkings.check_arguments(args)):
    #     if(args.confpath is None):
    #         arg_obj = ArgsInfo(args.regexp, args.repdir, args.filepat, args.fileext)
    #     else:
    #         try:
    #             with open(args.confpath, "r") as myfile:
    #                 json_data = json.load(myfile)
    #         except:
    #             print("Error with opening config file")
    #             exit()
    #         arg_obj = ArgsInfo(json_data["regexp"],json_data["repdir"],
    #                            json_data["filepat"], json_data["fileext"])
    #         print(arg_obj)



if __name__ == "__main__":
    main()