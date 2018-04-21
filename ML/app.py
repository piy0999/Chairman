from requests_futures.sessions import FuturesSession
import requests
import json
import cv2
from time import sleep
import numpy as np

capture = cv2.VideoCapture('stream0.ts')

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)

addr = 'http://localhost:5000'
test_url = addr + '/api/count_people'
content_type = 'image/jpeg'
headers = {'content-type': content_type}

labels_to_names = {0: 'person'}
import colorsys
import random
N = len(labels_to_names)
HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
RGB_tuples = list(map(lambda x: tuple(255*np.array(colorsys.hsv_to_rgb(*x))), HSV_tuples))

bounding_boxes = []
scores = []

multiplier = 40
session = FuturesSession()

def save_analysis(sess,resp):
    global bounding_boxes
    global scores
    data = json.loads(resp.text)
    bounding_boxes = data['bounding_boxes']
    scores = data['scores']

    people_count = data['people_count']
    requests.post('http://chairman.southeastasia.cloudapp.azure.com:8080/dbdata',data = {'space':'hkust_lib_zone_2','nOfSeats':200,'nOfPeople':people_count})

ret, frame = capture.read()
_, img_encoded = cv2.imencode('.jpg', frame)
future_one = session.post(test_url, data=img_encoded.tostring(), headers=headers, background_callback=save_analysis)

while(True):
    ret, frame = capture.read()
    if ret:
        if int(round(capture.get(1))) % multiplier == 0:
            _, img_encoded = cv2.imencode('.jpg', frame)
            future_one = session.post(test_url, data=img_encoded.tostring(), headers=headers, background_callback=save_analysis)
        if future_one.done():
            print(future_one.result())
        temp_bounding_boxes = bounding_boxes
        temp_scores = scores
        for i in range(0, len(temp_bounding_boxes)):
            b = temp_bounding_boxes[i]
            cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), RGB_tuples[0], 6)
            caption = "%s: %.1f%%"%(labels_to_names[0], temp_scores[i]*100)
            cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
            cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()