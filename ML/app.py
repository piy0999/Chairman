import requests
import json
import cv2
from time import sleep

capture = cv2.VideoCapture('stream0.ts')

addr = 'http://localhost:5000'
test_url = addr + '/api/count_people'
content_type = 'image/jpeg'
headers = {'content-type': content_type}

while(True):
    ret, frame = capture.read()

    if ret:
        cv2.imshow('frame',frame)
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
        print(json.loads(response.text))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()