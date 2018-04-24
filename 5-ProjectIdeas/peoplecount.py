#
# Copyright Amazon AWS DeepLens, 2017
#

import os
import greengrasssdk
from threading import Timer
import time
import awscam
import cv2
from threading import Thread

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# The information exchanged between IoT and clould has
# a topic and a message body.
# This is the topic that this code uses to send messages to cloud
iotTopic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])
ret, frame = awscam.getLastFrame()
ret,jpeg = cv2.imencode('.jpg', frame)
Write_To_FIFO = True
class FIFO_Thread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        fifo_path = "/tmp/results.mjpeg"
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        f = open(fifo_path,'w')
        client.publish(topic=iotTopic, payload="Opened Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue

def greengrass_infinite_infer_run():
    try:
        modelPath = "/opt/awscam/artifacts/mxnet_deploy_ssd_resnet50_300_FP16_FUSED.xml"
        modelType = "ssd"
        input_width = 300
        input_height = 300
        max_threshold = 0.25
        outMap = { 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7 : 'car', 8 : 'cat', 9 : 'chair', 10 : 'cow', 11 : 'dinning table', 12 : 'dog', 13 : 'horse', 14 : 'motorbike', 15 : 'person', 16 : 'pottedplant', 17 : 'sheep', 18 : 'sofa', 19 : 'train', 20 : 'tvmonitor' }
        results_thread = FIFO_Thread()
        results_thread.start()
        # Send a starting message to IoT console
        client.publish(topic=iotTopic, payload="Object detection starts now")

        # Load model to GPU (use {"GPU": 0} for CPU)
        mcfg = {"GPU": 1}
        model = awscam.Model(modelPath, mcfg)
        client.publish(topic=iotTopic, payload="Model loaded")
        ret, frame = awscam.getLastFrame()
        if ret == False:
            raise Exception("Failed to get frame from the stream")

        yscale = float(frame.shape[0]/input_height)
        xscale = float(frame.shape[1]/input_width)

        doInfer = True
        while doInfer:
            # Get a frame from the video stream
            ret, frame = awscam.getLastFrame()
            # Raise an exception if failing to get a frame
            if ret == False:
                raise Exception("Failed to get frame from the stream")

            # Resize frame to fit model input requirement
            frameResize = cv2.resize(frame, (input_width, input_height))

            # Run model inference on the resized frame
            inferOutput = model.doInference(frameResize)


            # Output inference result to the fifo file so it can be viewed with mplayer
            parsed_results = model.parseResult(modelType, inferOutput)['ssd']
            persons = 0
            label = '{'
            for obj in parsed_results:
                if obj['prob'] > max_threshold:
                    if(obj['label'] == 'person')
                        persons = persons + 1
                    xmin = int( xscale * obj['xmin'] ) + int((obj['xmin'] - input_width/2) + input_width/2)
                    ymin = int( yscale * obj['ymin'] )
                    xmax = int( xscale * obj['xmax'] ) + int((obj['xmax'] - input_width/2) + input_width/2)
                    ymax = int( yscale * obj['ymax'] )
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 165, 20), 4)
                    label += '"{}": {:.2f},'.format(outMap[obj['label']], obj['prob'] )
                    label_show = "{}:    {:.2f}%".format(outMap[obj['label']], obj['prob']*100 )
                    cv2.putText(frame, label_show, (xmin, ymin-15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 20), 4)
            label += '"null": 0.0'
            label += '}'
            #client.publish(topic=iotTopic, payload = label)
            client.publish(topic=iotTopic, payload = "{ 'persons' : " + str(persons) + "}" )
            global jpeg
            ret,jpeg = cv2.imencode('.jpg', frame)

    except Exception as e:
        msg = "Test failed: " + str(e)
        client.publish(topic=iotTopic, payload=msg)

    # Asynchronously schedule this function to be run again in 15 seconds
    Timer(15, greengrass_infinite_infer_run).start()


# Execute the function above
greengrass_infinite_infer_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
