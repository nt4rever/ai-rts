import keras as K
from PIL import Image
from io import BytesIO
from keras.preprocessing import image as k_image
import numpy as np
import requests

target_size = (224, 224)

class_labels = ['dry_asphalt_severe',
                'dry_asphalt_slight',
                'dry_asphalt_smooth',
                'dry_concrete_severe',
                'dry_concrete_slight',
                'dry_concrete_smooth',
                'water_asphalt_severe',
                'water_asphalt_slight',
                'water_asphalt_smooth',
                'water_concrete_severe',
                'water_concrete_slight',
                'water_concrete_smooth',
                'wet_asphalt_severe',
                'wet_asphalt_slight',
                'wet_asphalt_smooth',
                'wet_concrete_severe',
                'wet_concrete_slight',
                'wet_concrete_smooth']


def load_model(path='./store/best_weight.h5'):
    return K.models.load_model(path)


def convert_url_to_image(url: str):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert("RGB")
    image = image.resize(target_size)
    return image


def rts_predict(model, image):

    res = []

    # turn it into a numpy array
    x = k_image.img_to_array(image)

    # expand the shape of the array,
    # a new axis is added at the beginning:
    xs = np.expand_dims(x, axis=0)

    xs = K.applications.resnet50.preprocess_input(xs)

    # evaluate the model to extract the features
    predictions = model.predict(xs)

    # get top 3 class indices
    predicted_classes = np.argsort(predictions[0])[::-1][:3]

    decoded_predictions = [(class_labels[i], predictions[0][i])
                           for i in predicted_classes]
    # Sort predictions by confidence
    decoded_predictions.sort(key=lambda x: x[1], reverse=True)
    # Print the top 3 predictions
    for i, (label, score) in enumerate(decoded_predictions[:3]):
        res.append({"label": label, "score": float(score)})
    return res
