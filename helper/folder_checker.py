import os

class FolderChecker:
    def __init__(self, path):
        self.path =  path
    
    
    
    def checker(self):
        print(self.path)
        if os.path.isdir(self.path):
            file_list = os.listdir(self.path)
            if len(file_list) >= 1:
                print("Folder contains more than zero file")
                return True
            else:
                print("Folder does not contain more than zero file")
                return False
        else:
            os.makedirs(self.path)
            print("Not a folder")
            return False