#!/usr/bin/env python
# coding: utf-8
import numpy as np
import tflite_runtime.interpreter as tflite
#import tensorflow.lite as tflite
from io import BytesIO
from urllib import request

from PIL import Image

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def process_img(X):
    # img to Array
    x = np.array(X,dtype='float32')
    
    x = x.reshape((1,) + x.shape)
    x = x/255
    
    return x



interpreter = tflite.Interpreter(model_path='cats-dogs-v2.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']



#url = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Pug_600.jpg'
def predict(url):
    
    X  = prepare_image(download_image(url),(150,150))
    X  = process_img(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    proba = preds[0].tolist()
    label = "Dog" if preds[0][0] >= 0.5 else "Cat"
    print('Prediction is {} , with a probability of {} %'.format(label,proba*100))
    return  proba, label

#print('Prediction is = {}'.format(predict(url)))

def lambda_handler(event, context):
    url = event['url']
    result, label = predict(url)
    return label,result