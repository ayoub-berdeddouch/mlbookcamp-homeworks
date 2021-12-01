FROM agrigorev/zoomcamp-cats-dogs-lambda:v2

RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp38-cp38-linux_x86_64.whl
RUN pip install pillow
RUN pip install requests

COPY dogs-cats-model-v3-ab.tflite .
COPY lambda_function.py .

CMD [ "lambda_function.lambda_handler" ]