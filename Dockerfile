FROM codait/max-base:v1.1.1

ARG model_bucket=http://max-assets.s3.us.cloud-object-storage.appdomain.cloud/keras
ARG model_file=inception_resnet_v2.h5

WORKDIR /workspace

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

# check file integrity
RUN md5sum -c md5sums.txt

EXPOSE 5000

CMD python app.py
