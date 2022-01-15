import util_functions
import os


def main():
    args = util_functions.parsing_argument()
    if not util_functions.check_arguments(args):
        print("Invalid Arguments passed, make sure you did it in the right way")
        exit()
    arg_obj = util_functions.init_obj(args)
    files_ab_paths = util_functions.get_files_path(arg_obj, os.getcwd())
    print(files_ab_paths)

if __name__ == "__main__":
    main()