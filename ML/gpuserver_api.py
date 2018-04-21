from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from flask_cors import CORS, cross_origin

# Initialize the Flask application
app = Flask(__name__)
CORS(app)


# route http posts to this method
@app.route('/api/count_people', methods=['POST'])
def count_people():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    people_count = 0
    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                'people_count':people_count,}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)