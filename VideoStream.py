import cv2 as cv
from helper.constants import DATA_PATH,CLIP_DURATION
from video_services.extract_objects_from_clips import ExtractObjectsFromClips
from video_services.extract_caption_rom_clips import ExtractCaptionFromClips
from video_services.imageClipsService import ImageClipsService
from video_services.clips_pkl import ClipsPkl
from video_services.save_excel import SaveExel
import os


class VideoStream:
    def __init__(self, url):
        self.url = url
        self.cap = cv.VideoCapture(url)
        self.name = url.split('/')[-1].split('.')[0]
        self.path_data = DATA_PATH  + self.name
        self.path_frames = self.path_data + '/frames/'
        self.path_clips = self.path_data + '/clips/'
        self.path_excel = self.path_data + '/excel/'
        self.total_frames = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.duration = self.total_frames / self.fps 
        self.step_detect = CLIP_DURATION * self.fps
        self.frame_number=0
        self.clips = []
        self.extractor_objects = ExtractObjectsFromClips(self)
        self.extractor_caption = ExtractCaptionFromClips(self)
        
        self.Clips_Image = ImageClipsService(self)
        self.Clips_pkl = ClipsPkl(self)
        self.sever_exel = SaveExel(self)



    def stop(self):
        return
    



    def index_to_time(self,frame_number):
        # Get the time in seconds for the given frame number
        return self.duration * (frame_number / self.fps)
 
      
                