from helper.file_checker import FileChecker
from helper.folder_checker import FolderChecker
from clip import videoClip
from pickle import dump
from os import listdir
import pickle
import os
import pandas as pd

class SaveExel:
    def __init__(self, video_stream):
        self.video_stream =  video_stream

    

    def save(self):
        print(self.video_stream.path_data)
        newpath = self.video_stream.path_data + "/excel"
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        for clip in self.video_stream.clips:    
            names = ''
            for name in set(clip.list_names_objects):
                names=names  + name+","
            # create some sample data
            data = { 'id':clip.image_name.split('.')[0],
                    'start': clip.start,
                    'end': clip.end,
                    'names_objects' : names,
                    'caption' : clip.caption

                    }
            # create a DataFrame from the data
            df = pd.DataFrame(data,index=[0])

            if os.path.isfile(newpath+ '/clip_file'+'.csv'):
                # Load the Excel file
                df_last = pd.read_csv(newpath+ '/clip_file'+'.csv')
                df = pd.concat([df_last, df], ignore_index=True)

            # save the DataFrame to an Excel file
            df.to_csv(newpath + '/clip_file' +'.csv', index=False)