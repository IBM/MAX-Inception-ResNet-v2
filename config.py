# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# default model
MODEL_NAME = 'inception_resnet_v2'
DEFAULT_MODEL_PATH = 'assets/{}.h5'.format(MODEL_NAME)

MODEL_INPUT_IMG_SIZE = (299, 299)
MODEL_LICENSE = "Apache v2"

