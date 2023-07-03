import cv2 as cv
import numpy as np
import torch
from models.experimental import attempt_load
from numpy import random
from utils.general import check_img_size, non_max_suppression, \
    scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device

class Detector:
    def __init__(self,
                 weights='weights\yolov7x.pt',
                 is_draw_aoi=True,
                 img_size=640,
                 conf_threshold=0.35,  # try 0.5
                 iou_threshold=0.45,  # try 0.5
                 ):

        self.weights = weights
        self.device = select_device("")
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        # Load model
        self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        self.img_size = check_img_size(img_size, s=self.stride)  # check img_size
        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]
        self.list_names_objects = []

    def is_inside_aoi(self, point, aoi):
        # Check if a point is inside the area of interest (AOI)
        return cv.pointPolygonTest(aoi, point, False) >= 0

    def preprocess_image_for_inference(self, frame):
        # Perform a padded resize and get the resized image
        img = self.letterbox(frame, self.img_size, stride=self.stride)[0]
        # Convert the image to the correct format for PyTorch models
        # Convert BGR to RGB and transpose to 3xHxW format
        img = img[:, :, ::-1].transpose(2, 0, 1)
        # Convert the image to a contiguous array for faster processing
        img = np.ascontiguousarray(img)
        # Convert the image to a PyTorch tensor and move it to the specified device
        img = torch.from_numpy(img).to(self.device)
        # Convert the image to float and scale the pixel values to [0, 1]
        img = img.float() / 255.0
        return img

    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True,
                  stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better test mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv.resize(img, new_unpad, interpolation=cv.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=color)  # add border
        return img, ratio, (dw, dh)

    def counting_detect_by_frame(self, frame):
        self.list_names_objects.clear()

        image = self.preprocess_image_for_inference(frame)

        if image.ndimension() == 3:
            image = image.unsqueeze(0)
            # Inference
            try:
                with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
                    pred = self.model(image, augment=False)[0]
            except Exception as e:
                print(f"Error model: {e}")

            # Apply NMS
            pred = non_max_suppression(
                pred,
                self.conf_threshold,
                self.iou_threshold,
                None,
                False)  

            # Process detections
            if pred is not None and len(pred):
                for detection in pred:  # Detections per image
                    if detection is not None and len(detection):
                        # Rescale boxes from img_size to frame size
                        detection[:, :4] = scale_coords(image.shape[2:], detection[:, :4], frame.shape).round()

                        # Compute detection statistics per class 
                        for c in detection[:, -1].unique():

                            # Draw bounding boxes and label for each detection
                            for *xyxy, confidence, cls in reversed(detection):

                                self.list_names_objects.append(self.names[int(cls)])

                                if False:
                                    label = f'{self.names[int(cls)]} {confidence:.2f}'
                                    color = self.colors[int(cls)]
                                    line_thickness = 1
                                    plot_one_box(xyxy, frame, label=label, color=color, line_thickness=line_thickness)
                                   

        

        return frame , self.list_names_objects
