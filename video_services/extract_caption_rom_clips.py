import cv2 as cv
from core_services.caption_Generator import ImageCaptionGenerator

class ExtractCaptionFromClips:
    def __init__(self, video_stream):
        self.video_stream =  video_stream
        self.caption_Generator = ImageCaptionGenerator()
    
    def by_GPT2_VIT(self):
        print('start image captioning by GPT2 VIT')
        self.video_stream.Clips_pkl.load()
        print(self.video_stream.clips[0].start)
        for clip in self.video_stream.clips:
            clip_image_path = self.video_stream.path_frames + clip.image_name
            i_image = cv.imread(clip_image_path)
            i_image = cv.cvtColor(i_image, cv.COLOR_BGR2RGB)
            clip.caption = self.caption_Generator.caption_generator(i_image)
            clip.save_clip_caption_in_exel_file()   