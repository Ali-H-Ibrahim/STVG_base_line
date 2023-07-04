from helper.file_checker import FileChecker
from helper.folder_checker import FolderChecker
from clip import videoClip
from pickle import dump
from os import listdir
import pickle


class ClipsPkl:
    def __init__(self, video_stream):
        self.video_stream =  video_stream

    def save(self):
        print('Saving the Pikl clips')
        newpath = self.video_stream.path_clips     
        if not FolderChecker(newpath).checker() or not FileChecker(newpath+'clips.pkl').checker():
            directory_clips = self.video_stream.path_frames
            clip_names = listdir(directory_clips)
            # define a function to extract the numeric portion of the file name
            def get_numeric_part(file_name):
                return int(file_name.split('.')[0])
            clip_names = sorted(clip_names, key=get_numeric_part)
            for clip_name in clip_names:
                number_clip = int(clip_name.split('.')[0])
                print(number_clip)
                clip = videoClip()
                clip.path_data = self.video_stream.path_data
                clip.image_name = clip_name
                clip.end = self.video_stream.index_to_time(self.video_stream.step_detect *  number_clip)
                clip.start = self.video_stream.index_to_time((self.video_stream.step_detect *  number_clip) - self.video_stream.step_detect)
                print('start' ,clip.start)
                self.video_stream.clips.append(clip)
            clips = self.video_stream.clips   
            dump(clips,open(newpath + '/clips.pkl','wb'))
    
    
    def load(self):
        try:
            with open( self.video_stream.path_clips +  'clips.pkl', 'rb') as f:
                self.video_stream.clips = pickle.load(f)
        except:
            print("clips.pkl File does not exist")