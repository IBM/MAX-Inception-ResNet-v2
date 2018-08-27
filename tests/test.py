import pytest
import requests


def test_response():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/cat.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'
    assert response['predictions'][0]['label_id'] == 'n02123045'
    assert response['predictions'][0]['label'] == 'tabby'
    assert response['predictions'][0]['probability'] > 0.6


if __name__ == '__main__':
    pytest.main([__file__])
