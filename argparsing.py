import argparse


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

