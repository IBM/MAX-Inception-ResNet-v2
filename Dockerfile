FROM continuumio/miniconda3

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/keras
ARG model_file=inception_resnet_v2.h5

WORKDIR /workspace
RUN mkdir assets
RUN wget -nv ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}

# Python package versions
ARG numpy_version=1.14.1
ARG tf_version=1.5.0
ARG keras_version=2.1.4

RUN pip install --upgrade pip && \
    pip install numpy==${numpy_version} && \
    pip install tensorflow==${tf_version} && \
    pip install Pillow && \
    pip install h5py && \
    pip install keras==${keras_version} && \
    pip install flask-restplus && \
    pip install ipython

COPY . /workspace

EXPOSE 5000

CMD python app.py
