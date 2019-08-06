#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API Metadata
API_TITLE = 'MAX Image Classifier - Inception ResNet v2'
API_DESC = 'Identify objects in images using a third-generation deep residual network.'
API_VERSION = '1.2.0'

# Model settings
keras_builtin_models = {
    'inception_v3': {'size': (299, 299), 'license': 'Apache v2'},
    'inception_resnet_v2': {'size': (299, 299), 'license': 'Apache v2'},
    'xception': {'size': (299, 299), 'license': 'MIT'},
    'resnet50': {'size': (224, 224), 'license': 'MIT'}
}

# default model
MODEL_NAME = 'inception_resnet_v2'
DEFAULT_MODEL_PATH = 'assets/{}.h5'.format(MODEL_NAME)
MODEL_INPUT_IMG_SIZE = keras_builtin_models[MODEL_NAME]['size']
MODEL_LICENSE = keras_builtin_models[MODEL_NAME]['license']

MODEL_META_DATA = {
    'id': '{}-keras-imagenet'.format(MODEL_NAME.lower()),
    'name': '{} Keras Model'.format(MODEL_NAME),
    'description': '{} Keras model trained on ImageNet'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE),
    'source': 'https://developer.ibm.com/exchanges/models/all/max-inception-resnet-v2/'
}
