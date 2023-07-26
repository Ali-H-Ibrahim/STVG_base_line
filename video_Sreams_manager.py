import cv2 as cv

from VideoStream import VideoStream
from extract_transcript import ExtractTranscript

# Initialize Detector object
class videoStreamsManager:
    def __init__(self):
        self.video_Sreams = []
        self.detection = True
        self.count = 0
        self.extractor_transcript = ExtractTranscript()



    def add_video_Stream(self, path):
        # Initialize VideoSream objects for each camera
        video_Stream = VideoStream(path)
        print('add video Stream')
        # init video Stream
        video_Stream.Clips_Image.save()
        video_Stream.Clips_pkl.save()
        video_Stream.Clips_pkl.load()

        print('total_frames',video_Stream.total_frames)
        print('duration',video_Stream.duration)
        print('fps',video_Stream.fps)
        self.video_Sreams.append(video_Stream)


    def clear_video_Sreams(self):
        self.video_Sreams = []

    
        
    def destroyAllWindows(self):
        for video_Sream in self.video_Sreams:
            video_Sream.stop()
        cv.destroyAllWindows()





    def run_processes(self,YOLO,CAPTION):
        try:
            
            for video_Sream in self.video_Sreams:
                    if YOLO :
                        video_Sream.extractor_objects.by_yolo()
                    if CAPTION:  
                        video_Sream.extractor_caption.by_GPT2_VIT()
                    self.extractor_transcript.from_video(video_Sream)    

                    video_Sream.sever_exel.save()    
                        
        except Exception as e:
            print(f"Error: {e}")
            self.destroyAllWindows()
        finally:
            self.destroyAllWindows()           
