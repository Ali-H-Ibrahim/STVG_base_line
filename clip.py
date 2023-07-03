import os
import pandas as pd

class videoClip:
    def __init__(self):
        self.image_name = ''
        self.path_data = ''
        self.start = 0
        self.end = 0
        self.list_names_objects = []
        self.caption = ''



    def save_clip_objects_list_in_exel_file(self):
        print(self.path_data)
        newpath = self.path_data + "/excel"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        names = ''
        for name in set(self.list_names_objects):
            names=names  + name+","
        # create some sample data
        data = {'start': self.start,
                'end': self.end,
                'names_objects' : names
                }
        # create a DataFrame from the data
        df = pd.DataFrame(data,index=[0])

        if os.path.isfile(newpath+ '/clip_objects_file'+'.csv'):
            # Load the Excel file
            df_last = pd.read_csv(newpath+ '/clip_objects_file'+'.csv')
            df = pd.concat([df_last, df], ignore_index=True)

        # save the DataFrame to an Excel file
        df.to_csv(newpath + '/clip_objects_file' +'.csv', index=False)



    def save_clip_caption_in_exel_file(self):
        print(self.path_data)
        newpath = self.path_data + "/excel"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
      
            
        # create some sample data
        data = {'start': self.start,
                'end': self.end,
                'caption' : self.caption
                }
        # create a DataFrame from the data
        df = pd.DataFrame(data,index=[0])

        if os.path.isfile(newpath+ '/clip_caption_file'+'.csv'):
            # Load the Excel file
            df_last = pd.read_csv(newpath+ '/clip_caption_file'+'.csv')
            df = pd.concat([df_last, df], ignore_index=True)

        # save the DataFrame to an Excel file
        df.to_csv(newpath + '/clip_caption_file' +'.csv', index=False)    