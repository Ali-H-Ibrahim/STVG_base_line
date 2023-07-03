import cv2 as cv
from object_detection import Detector
from caption_Generator import ImageCaptionGenerator
from VideoStream import VideoStream

# Initialize Detector object
class videoStreamsManager:
    def __init__(self):
        self.detector = Detector()
        self.caption_Generator = ImageCaptionGenerator()
        self.video_Sreams = []
        self.detection = True
        self.count = 0


    def add_video_Stream(self, path):
        # Initialize VideoSream objects for each camera
        video_Sream = VideoStream(path)
        print('add video Stream')
        video_Sream.save_images_clips()
        print('total_frames',video_Sream.total_frames)
        print('duration',video_Sream.duration)
        print('fps',video_Sream.fps)
        self.video_Sreams.append(video_Sream)


    def clear_video_Sreams(self):
        self.video_Sreams = []

    
        
    def destroyAllWindows(self):
        for video_Sream in self.video_Sreams:
            video_Sream.stop()
        cv.destroyAllWindows()


    def index_to_time(self,duration,frame_number,fps):
        # Get the time in seconds for the given frame number
        return duration * (frame_number / fps)
    
    def read_cap_only(self):
        for video_Sream in self.video_Sreams:
                video_Sream.frame = video_Sream.only_read()
                video_Sream.frame_number+=1



    def yolo_extraction_objects(self):
        print('start yolo extraction objects ')
        images = []
        for video_Sream in self.video_Sreams:
            video_Sream.load_clips()
            print(video_Sream.clips[0].start)
            for clip in video_Sream.clips:
                clip_image_path = video_Sream.path_frames + clip.image_name
                i_image = cv.imread(clip_image_path)
                i_image = cv.cvtColor(i_image, cv.COLOR_BGR2RGB)
                i_image, clip.list_names_objects = self.detector.counting_detect_by_frame(i_image)
                clip.save_clip_objects_list_in_exel_file()
                images.append(i_image)
        return images    
    


    def image_captioning(self):
        print('start image captioning ')
        for video_Sream in self.video_Sreams:
            video_Sream.load_clips()
            print(video_Sream.clips[0].start)
            for clip in video_Sream.clips:
                clip_image_path = video_Sream.path_frames + clip.image_name
                i_image = cv.imread(clip_image_path)
                i_image = cv.cvtColor(i_image, cv.COLOR_BGR2RGB)
                clip.caption = self.caption_Generator.caption_generator(i_image)
                clip.save_clip_caption_in_exel_file()


    def run_processes(self,YOLO,CAPTION):
        try:

            if YOLO :
                self.yolo_extraction_objects()

            if CAPTION:  
                    self.image_captioning()
                        
        except Exception as e:
            print(f"Error: {e}")
            self.destroyAllWindows()
        finally:
            self.destroyAllWindows()           
