# Import necessary modules
from video_Sreams_manager import videoStreamsManager


# Define paths to video streams for each camera
path ='data/videos/Johnny.English.mkv'

YOLO = False
CAPTION = True



if __name__ == "__main__":


    # Initialize CameraCollection object
    video_sreams_manager = videoStreamsManager()

    # # Add video_Sream
    video_sreams_manager.add_video_Stream(path)

    # run 
    video_sreams_manager.run_processes(YOLO,CAPTION)

        