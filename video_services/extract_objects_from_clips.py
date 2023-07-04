import cv2 as cv
from core_services.object_detection import Detector

class ExtractObjectsFromClips:
    def __init__(self, video_stream):
        self.video_stream =  video_stream
        self.detector = Detector()
    
    def by_yolo(self):
        print('start yolo extraction objects ')
        images = []
        print(self.video_stream.clips[0].start)
        for clip in self.video_stream.clips:
            clip_image_path = self.video_stream.path_frames + clip.image_name
            i_image = cv.imread(clip_image_path)
            i_image = cv.cvtColor(i_image, cv.COLOR_BGR2RGB)
            i_image, clip.list_names_objects = self.detector.counting_detect_by_frame(i_image)
            clip.save_clip_objects_list_in_exel_file()
            images.append(i_image)
        return images
    