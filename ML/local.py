# import keras
import keras

# import keras_retinanet
from keras_retinanet.models.resnet import custom_objects
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

# use this environment flag to change which GPU to use
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# set the modified tf session as backend in keras
keras.backend.tensorflow_backend.set_session(get_session())

# adjust this to point to your downloaded/trained model
# models can be downloaded here: https://github.com/fizyr/keras-retinanet/releases
model_path = os.path.join('..', 'snapshots', 'resnet50_coco_best_v2.0.3.h5')

# load retinanet model
model = keras.models.load_model(model_path, custom_objects=custom_objects)
#print(model.summary())

# load label to names mapping for visualization purposes
labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}


import json
import cv2
from time import sleep
import numpy as np

capture = cv2.VideoCapture('stream0.ts')

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)

bounding_boxes = []
scores = []
people_count = 0

while(True):
	ret, frame = capture.read()
	if ret:
		draw = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# preprocess image for network
		image = preprocess_image(frame)
		image, scale = resize_image(image)

		# process image
		start = time.time()
		boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
		print("processing time: ", time.time() - start)

		# correct for image scale
		boxes /= scale

		# visualize detections
		for box, score, label in zip(boxes[0], scores[0], labels[0]):
		    # scores are sorted so we can break
		    if score < 0.5:
		        break

		    color = label_color(label)

		    b = box.astype(int)
		    draw_box(frame, b, color=color)

		    caption = "{} {:.3f}".format(labels_to_names[label], score)
		    draw_caption(frame, b, caption)
		    #print(b,caption)

		temp_bounding_boxes = bounding_boxes
		temp_scores = scores
		temp_people_count = people_count
		for i in range(0, len(temp_bounding_boxes)):
			b = temp_bounding_boxes[i]
			cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), RGB_tuples[0], 6)

			# Write label & score
			caption = "%s: %.1f%%"%(labels_to_names[0], temp_scores[i]*100)
			cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 5)
			cv2.putText(frame, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

			# write number of people
			cv2.putText(frame, 'Number of People: ' + str(temp_people_count), (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)

		cv2.imshow('image',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()
