import requests
import json
import cv2
from time import sleep
import numpy as np

capture = cv2.VideoCapture('/Users/mengjiunchiou/keras-retinanet/videos/IMG_8766.MOV')

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

multiplier = 1

while(True):
	ret, frame = capture.read()
	bounding_boxes = []
	scores = []
	if ret:
		if int(round(capture.get(1))) % multiplier == 0:
			_, img_encoded = cv2.imencode('.jpg', frame)
			response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
			data = json.loads(response.text)
			print(data)
			# import pdb; pdb.set_trace()
			bounding_boxes = data['bounding_boxes']
			scores = data['scores']

		for i in range(0, len(bounding_boxes)):
			b = bounding_boxes[i]
			cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), RGB_tuples[0], 6)
			caption = "%s: %.1f%%"%(labels_to_names[0], scores[i]*100)
			cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
			cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

		cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()
