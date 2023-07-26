import cv2 as cv
from helper.folder_checker import FolderChecker
import os

class ImageClipsService:
    def __init__(self, video_stream):
        self.video_stream =  video_stream
    
    def save(self):
        print('Saving the image')
        # Saving the image
        newpath1 = self.video_stream.path_frames
        if not FolderChecker(newpath1).checker():
            # read the first frame
            success, frame = self.video_stream.cap.read()
            count = 1
            self.video_stream.frame_number += 1
            # loop through the frames and save them as images
            while success:
                if count>=self.video_stream.step_detect:
                    # save the current frame as an image
                    cv.imwrite(os.path.join(newpath1, '%d.jpg' % self.video_stream.frame_number), frame)
                    self.video_stream.frame_number += 1
                    count = 0      
                count+=1 
                # read the next frame
                success, frame = self.video_stream.cap.read() 
    