from PIL import Image
from keras.backend import clear_session
from keras import models
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import io
import numpy as np
import logging

logger = logging.getLogger()

from config import MODEL_INPUT_IMG_SIZE, DEFAULT_MODEL_PATH

def read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    return image

def preprocess_image(image, target, mode='tf'):
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image, mode=mode)
    return image

def post_process_result(preds):
	return imagenet_utils.decode_predictions(preds)[0]

class ModelWrapper(object):
	"""Model wrapper for Keras models"""
	def __init__(self, path=DEFAULT_MODEL_PATH):
		logger.info('Loading model from: {}...'.format(path))
		clear_session()
		self.model = models.load_model(path)
		# this seems to be required to make Keras models play nicely with threads
		self.model._make_predict_function()
		logger.info('Loaded model: {}'.format(self.model.name))

	def predict(self, x):
		x = preprocess_image(x, target=MODEL_INPUT_IMG_SIZE)
		preds = self.model.predict(x)
		return post_process_result(preds)


		