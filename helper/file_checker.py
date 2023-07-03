import os

class FileChecker:
    def __init__(self, path):
        self.path =  path
    
    def checker(self):
        if os.path.exists(self.path):
            print("File or folder exists")
            return True
        else:
            print("File or folder does not exist")
            return False
