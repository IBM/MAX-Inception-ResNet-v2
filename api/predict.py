from core.model import ModelWrapper, _read_image
from flask_restplus import fields
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True, help="An image file (RGB/HWC)")


label_prediction = MAX_API.model('LabelPrediction', {
    'label_id': fields.String(required=False, description='Class label identifier'),
    'label': fields.String(required=True, description='Class label'),
    'probability': fields.Float(required=True, description='Predicted probability for the class label')
})


predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction), description='Predicted class labels and probabilities')
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        input_data = args['image'].read()
        image = _read_image(input_data)
        preds = self.model_wrapper._predict(image)

        # Modify this code if the schema is changed
        label_preds = [{'label_id': p[0], 'label': p[1], 'probability': p[2]} for p in [x for x in preds]]
        result['predictions'] = label_preds
        result['status'] = 'ok'

        return result
