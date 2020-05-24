import sys
import numpy as np
import tensorflow

from google.cloud import storage
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
from PIL import Image
from tensorflow.keras.models import load_model

# Model is global variable so it doesn't have to be reloaded every time
model = None

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def classify(filepath):
    global model
    class_names = ['RichardRodgersTheatre', 'AlHirschfeldTheatre', 'WalterKerrTheatre', 'GershwinTheatre', 
                   'MusicBoxTheatre', 'LyricTheatre', 'WinterGardenTheatre', 'ShubertTheatre', 
                   'AugustWilsonTheatre', 'St.JamesTheatre', 'BrooksAtkinsonTheatre', 'BroadhurstTheatre', 
                   'ImperialTheatre', 'BroadwayTheatre-53rdStreet', 'GeraldSchoenfeldTheatre', 
                   'PalaceTheatre(Broadway)', 'MajesticTheatre', 'LyceumTheatre(Broadway)', 'NewAmsterdamTheatre', 
                   "EugeneO'NeillTheatre"]

    # Model load which only happens during cold starts
    if model is None:
        download_blob('broadwayclassifier', 'LeNet5.10.h5', '/tmp/LeNet5.10.h5')
        model = load_model('/tmp/LeNet5.10.h5')
    
    download_blob('broadwayclassifier', filepath, '/tmp/' + filepath)

    image = np.array(tensorflow.keras.preprocessing.image.load_img('/tmp/' + filepath, target_size=(150,150)))

    class_num = np.argmax(model.predict(tensorflow.reshape(image, [-1, 150, 150, 3])))
    prediction = class_names[class_num]

    print("Image is "+prediction)
    
    return prediction

# [START functions_classify_image]
def classify_image(request):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # TODO: classify image from request
    return (classify(request.content), 200, headers)
# [END functions_classify_image]
