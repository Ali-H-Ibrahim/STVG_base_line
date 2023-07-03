import cv2 as cv
from clip import videoClip
import os
from helper.file_checker import FileChecker
from helper.folder_checker import FolderChecker
from helper.constants import DATA_PATH,CLIP_DURATION
import pickle
from pickle import dump

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

        
    def get_current_video_clip(self):
        return videoClip()

    def stop(self):
        return
    
    def read_and_display(self):
        try:
            success, img = self.cap.read()
            if not success:
                return
            img = cv.resize(img, (640, 640))
            if img is not None:
                cv.imshow('Video' + str(self.numCamera), img)
                key = cv.waitKey(1)
                if key == ord('q'):
                    return
        except Exception as e:
            print(f"Error: {e}")


    def only_read(self):
        try:
            success, img = self.cap.read()
            if not success:
                # print("error in read cam")
                return
            img = cv.resize(img, (640, 640))
            if img is not None:
                return img
        except Exception as e:
            print(f"Error: {e}")


    def load_clips(self):
        try:
            with open( self.path_clips +  'clips.pkl', 'rb') as f:
                self.clips = pickle.load(f)

        except:
            print("clips.pkl File does not exist")

            

    def index_to_time(self,frame_number):
        # Get the time in seconds for the given frame number
        return self.duration * (frame_number / self.fps)
            

    def save_images_clips(self):
        print('Saving the image')
        # Saving the image
        newpath1 = self.path_frames
        newpath2 = self.path_clips     
        
        if not FolderChecker(newpath1).checker() or not FileChecker(newpath2).checker() or not FileChecker(newpath2+'clips.pkl').checker():
          
            # read the first frame
            success, frame = self.cap.read()
            count = 1
            self.frame_number += 1
            # loop through the frames and save them as images
            while success:
                if count>=self.step_detect:
                    # save the current frame as an image
                    cv.imwrite(os.path.join(newpath1, '%d.jpg' % self.frame_number), frame)
                    clip = videoClip()
                    clip.path_data = self.path_data
                    clip.image_name = '%d.jpg' % self.frame_number
                    clip.end = self.index_to_time(self.step_detect *  self.frame_number)
                    clip.start = self.index_to_time((self.step_detect *  self.frame_number) - self.step_detect)
                    print('start' ,clip.start)
                    self.clips.append(clip)
                    self.frame_number += 1
                    count = 0      
                count+=1 
                # read the next frame
                success, frame = self.cap.read() 
            clips = self.clips   
            dump(clips,open(newpath2 + '/clips.pkl','wb'))    
      
                