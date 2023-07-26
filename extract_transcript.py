import cv2 as cv

from video_services.transcript import TranscriptExtractor



class ExtractTranscript:
    def __init__(self):
        self.extract_transcriptr = TranscriptExtractor()

    def from_video(self, video):
        print('start video extract transcriptr')
        segments = self.extract_transcriptr.extract(video.url)
        for clip in video.clips:
            for segment in segments:
                domain1 = (segment['start'],segment['end'])
                domain2 = (clip.start,clip.end)
                if self.do_domains_intersect(domain1,domain2):
                    print(segment['text'])
                    clip.sound_caption = segment['text']
                    
        print(f'end video extract transcriptr: {video.name}')
        
        



    def do_domains_intersect(self, domain1, domain2):
        if domain1[1] < domain2[0] or domain1[0] > domain2[1]:
            return False
        else:
            return True
        
        