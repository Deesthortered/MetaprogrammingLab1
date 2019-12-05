import os

class GoParser:
    def __init__(self):
        pass

    def prepare_directory_ierarhy(self, root_path):
        if os.path.exists(root_path):
            if os.path.isdir(root_path):
                if not os.listdir(root_path):
                    print("The input directory is epmty")
                else:
                    print(os.listdir(root_path))
            else:
                print("There is file on the path, not directory.")
                return False
        else:
            print("The input directory is not exist.")
            return False

