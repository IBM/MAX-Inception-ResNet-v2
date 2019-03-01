from PIL import Image
from keras.backend import clear_session
from keras import models
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import io
import numpy as np
import logging
from flask import abort
from config import DEFAULT_MODEL_PATH, MODEL_INPUT_IMG_SIZE, MODEL_META_DATA as model_meta
from maxfw.model import MAXModelWrapper

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = model_meta

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        clear_session()

        self.model = models.load_model(path)
        # this seems to be required to make Keras models play nicely with threads
        self.model._make_predict_function()
        logger.info('Loaded model: {}'.format(self.model.name))

    def _read_image(self, image_data):
        try:
            image = Image.open(io.BytesIO(image_data))
            #.convert('RGB')
            return image
        except IOError as e:
            logger.error(str(e))
            abort(400, "The provided input is not a valid image (PNG or JPG required).")

    def _pre_process(self, image, target, mode='tf'):
        image = image.resize(target)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image, mode=mode)
        return image

    def _post_process(self, preds):
        return imagenet_utils.decode_predictions(preds)[0]

    def _predict(self, x):
        x = self._pre_process(x, target=MODEL_INPUT_IMG_SIZE)
        preds = self.model.predict(x)
        return self._post_process(preds)
