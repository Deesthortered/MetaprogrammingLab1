import sys
from GoParser import GoParser

testString = ""

if __name__ == "__main__":
    parser = GoParser()

    if len(sys.argv) == 1:
        print("This is the Goland Documentator.")
        print("Please, type \"--help\" for manual of usage.")
    elif len(sys.argv) == 4:
        if (sys.argv[1] == "file"):
            pass
        elif (sys.argv[1] == "folder"):
            pass
        else:
            print("Unknown 2-nd parameter.")
            print("Please, type \"--help\" for manual of usage.")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            print("Please, enter next parameters for launching the program:")
            print("1) Documentation target: \"file\" or \"folder\"")
            print("  If you have chose File:")
            print("    2) Path to the target file (*.go)")
            print("    3) Path to the result file (any)")
            print("  If you have chose Folder:")
            print("    2) Path to the target folder")
            print("    3) Path to the destination folder, which will be created")
            print("       Warning! The folder must not exist before")
        else:
            print("Unknown parameter. Please, type \"--help\" for manual of usage.")
    else:
        print("Wrong quantity of the parametrs.")

