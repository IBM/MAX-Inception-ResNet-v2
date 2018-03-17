# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'list'

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# Model settings
keras_builtin_models = {
	'inception_v3': {'size': (299, 299), 'license': 'Apache2'},
	'inception_resnet_v2': {'size': (299, 299), 'license': 'Apache2'},
	'xception': {'size': (299, 299), 'license': 'MIT'},
	'resnet50': {'size': (224, 224), 'license': 'MIT'}
}

# default model
MODEL_NAME = 'inception_resnet_v2'
DEFAULT_MODEL_PATH = 'assets/{}.h5'.format(MODEL_NAME)
# for image models, may not be required
MODEL_INPUT_IMG_SIZE = keras_builtin_models[MODEL_NAME]['size']
MODEL_LICENSE = keras_builtin_models[MODEL_NAME]['license']

MODEL_META_DATA = {
    'id': '{}-keras-imagenet'.format(MODEL_NAME.lower()),
    'name': '{} Keras Model'.format(MODEL_NAME),
    'description': '{} Keras model trained on ImageNet'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}
