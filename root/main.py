import sys
import os
from GoParser import GoParser
from GoHtmlCreator import GoHtmlCreator


# python main.py file ./test_files/string.go ./string_result.html
# python main.py folder ./test_files/testDirectory ./result_directory


def proceed_directory(input_directory, destination_directory):
    if os.path.exists(input_directory):
        if os.path.isdir(input_directory):
            if not os.listdir(input_directory):
                print("The input directory is epmty")
            else:
                if os.path.isdir(destination_directory):
                    print("The destination directory already exists.")
                    return False
                else:
                    return True
        else:
            print("There is file on the path, not directory.")
            return False
    else:
        print("The input directory is not exist.")
        return False


def proceed_file(input_file, destination_file):
    if os.path.exists(input_file):
        if os.path.isfile(input_file):
            if os.path.isfile(destination_file):
                print("The destination file already exists.")
                return False
            else:
                return True
        else:
            print("There is directory on the path, not file.")
            return False
    else:
        print("The input file is not exist.")
        return False


if __name__ == "__main__":
    parser = GoParser()
    htmlCreator = GoHtmlCreator()

    if len(sys.argv) == 1:
        print("This is the Goland Documentator.")
        print("Please, type \"--help\" for manual of usage.")
    elif len(sys.argv) == 4:
        if sys.argv[1] == "file":
            if proceed_file(sys.argv[2], sys.argv[3]):
                parser.start_file(sys.argv[2], sys.argv[3])
                htmlCreator.create_file(sys.argv[3])
        elif sys.argv[1] == "folder":
            if proceed_directory(sys.argv[2], sys.argv[3]):
                path_list = parser.start_folder(sys.argv[2], sys.argv[3])
                htmlCreator.create_folder(path_list)
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
            print("       Warning! The file must not exist before")
            print("  If you have chose Folder:")
            print("    2) Path to the target folder")
            print("    3) Path to the destination folder, which will be created")
            print("       Warning! The folder must not exist before")
        else:
            print("Unknown parameter. Please, type \"--help\" for manual of usage.")
    else:
        print("Wrong quantity of the parametrs.")
