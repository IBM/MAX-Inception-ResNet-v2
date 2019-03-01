import pytest
import requests
from PIL import Image
import tempfile


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'Model Asset Exchange Microservice'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'inception_resnet_v2-keras-imagenet'
    assert metadata['name'] == 'inception_resnet_v2 Keras Model'
    assert metadata['description'] == 'inception_resnet_v2 Keras model trained on ImageNet'
    assert metadata['license'] == 'Apache v2'


def _check_predict(r):

    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'
    assert response['predictions'][0]['label_id'] == 'n02123045'
    assert response['predictions'][0]['label'] == 'tabby'
    assert response['predictions'][0]['probability'] > 0.6


def test_predict():

    formats = ['JPEG', 'PNG']
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/cat.jpg'
    jpg = Image.open(file_path)

    for f in formats:
        temp = tempfile.TemporaryFile()
        if f == 'PNG':
            jpg.convert('RGBA').save(temp, f)
        else:
            jpg.save(temp, f)
        temp.seek(0)
        file_form = {'image': (file_path, temp, 'image/{}'.format(f.lower()))}
        r = requests.post(url=model_endpoint, files=file_form)
        _check_predict(r)


def test_invalid_input():

    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/README.md'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400
    response = r.json()
    assert 'input is not a valid image' in response['message']


if __name__ == '__main__':
    pytest.main([__file__])
