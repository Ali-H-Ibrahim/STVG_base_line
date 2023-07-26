

import whisper
import os
from pydub import AudioSegment
from moviepy.editor import *

# @singleton
class TranscriptExtractor:
    def __init__(self, model_size="medium.en"):
        self.model = whisper.load_model(model_size)


    def extract(self, vedeo_path):
           
        path  = self.preprocessing(vedeo_path)
        result = self.model.transcribe(path)
        segments = result["segments"]
        segments_result = []
        for segment in segments:
            sem = {'start': segment["start"],'end': segment["end"],'text':segment["text"]}
            segments_result.append(sem)
            
        if os.path.exists(path):
            # delete the file
            os.remove(path)

        return segments_result
    
    
    def preprocessing(self,path):
        if path[-3:] != 'wav':
            # create a VideoFileClip object
            video_clip = VideoFileClip(path)
            # extract the audio and save it as an audio file
            audio_clip = video_clip.audio
            audio_clip.write_audiofile('audio.wav')
            # close the clips
            audio_clip.close()
            video_clip.close()
            path = 'audio.wav'
            

        # Load the stereo audio file
        audio = AudioSegment.from_file(path, format="wav")    
        # Extract the left and right channels
        left_channel = audio.split_to_mono()[0]
        right_channel = audio.split_to_mono()[1]
        # Combine the left and right channels into a single mono channel
        mono_audio = left_channel + right_channel
        # Export the mono audio as a new file
        mono_audio.export("mono_"+path, format="wav")
        temp_path = path
        path = "mono_"+path      
        if os.path.exists(temp_path):
        # delete the file
            os.remove(temp_path)
         
        return path    
        
        


        
    
    
    
    







