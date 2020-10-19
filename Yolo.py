import cv2
import numpy as np
import time

class Yolov3:
    # pass the path of files weights, cfg and names
    def __init__(self, weights, cfg, names):
        # Load YOLO
        self.net = cv2.dnn.readNet(weights, cfg)  # Original yolov3
        self.classes = []
        with open(names, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # print(self.classes)
        self.layerName = self.net.getLayerNames()
        self.outputlayers = [self.layerName[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def Yolov3Detection(self, frame):
        height, width, channels = frame.shape
        # detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)  # reduce 416 to 320
        self.net.setInput(blob)
        outs = self.net.forward(self.outputlayers)
        # print(outs[1])

        # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # onject detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                    # rectangle co-ordinaters
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                    boxes.append([x, y, w, h])  # put all rectangle areas
                    confidences.append(
                        float(confidence))  # how confidence was that object detected and show that percentage
                    class_ids.append(class_id)  # name of the object tha was detected

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)
        labels = []
        for i in range(len(boxes)):
            if i in indexes:
                labels.append(str(self.classes[class_ids[i]]))
        return labels, confidences, boxes # return objects name list, matching rate list, coordinate list in images

if __name__=="__main__":
    print('Yolo Test Module')
    yolo=Yolov3('../data/yolov3-tiny.weights', '../data/yolov3-tiny.cfg','../data/yolov3-tiny.names')
    img = cv2.imread('../data/images/dog.jpg')
    print(yolo.Yolov3Detection(img))
