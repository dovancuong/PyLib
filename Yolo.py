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


'''
# Load YOLO
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")  # Original yolov3
# net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg") #Tiny Yolo
classes = []
with open("yolov3-tiny.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

print(classes)
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
# loading image
cap = cv2.VideoCapture("data/videos/video2.mp4")  # 0 for 1st webcam
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

while True:
    _, frame = cap.read()  # 
    frame_id += 1

    height, width, channels = frame.shape
    # detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)  # reduce 416 to 320    

    net.setInput(blob)
    outs = net.forward(outputlayers)
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

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255), 2)

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)  # wait 1ms the loop will start again and we will process the next frame

    if key == 27:  # esc key stops the process
        break;

cap.release()
cv2.destroyAllWindows()
'''