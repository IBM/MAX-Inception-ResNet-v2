from PIL import Image
from keras.backend import clear_session
from keras import models
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import io
import numpy as np
import logging
from config import MODEL_INPUT_IMG_SIZE, DEFAULT_MODEL_PATH

logger = logging.getLogger()


def _read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    return image


def _pre_process(image, target, mode='tf'):
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image, mode=mode)
    return image


def _post_process(preds):
    return imagenet_utils.decode_predictions(preds)[0]


class ModelWrapper(object):
    """Model wrapper for Keras models"""

    MODEL_META_DATA = {
        'id': 'inception_resnet_v2-keras-imagenet',
        'name': 'inception_resnet_v2 Keras Model',
        'description': 'inception_resnet_v2 Keras model trained on ImageNet',
        'type': 'image_classification',
        'license': 'Apache v2'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        clear_session()
        self.model = models.load_model(path)
        # this seems to be required to make Keras models play nicely with threads
        self.model._make_predict_function()
        logger.info('Loaded model: {}'.format(self.model.name))

    def _predict(self, x):
        x = _pre_process(x, target=MODEL_INPUT_IMG_SIZE)
        preds = self.model.predict(x)
        return _post_process(preds)
