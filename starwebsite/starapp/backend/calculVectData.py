from keras.models import load_model
import pandas as pd
import numpy as np
from numpy import asarray
from PIL import Image
from vgg_model import loadVggFaceModel

# On utilise le model faceNet : https://github.com/nyoki-mtl/keras-facenet


# On load le model faceNet ainsi que l'ensemble de ses poids
#model = load_model("resources/model/model/facenet_keras.h5")
#model.load_weights("resources/model/weights/facenet_keras_weights.h5")

# On load le model VggFace ainsi que l'ensemble de ses poids
model = loadVggFaceModel()
model.load_weights("resources/model/weights/vgg_face_weights.h5")
print(model.summary())

# On load le fichier qui contient les metadata de nos images
meta_data_imdb = pd.read_csv("resources/vectorisation/imdb_metadata.csv")
# meta_data_wiki = pd.read_csv("resources/vectorisation/wiki_metadata.csv")


def open_image(path):
    image = Image.open(path)
    image = image.convert('RGB')
    return asarray(image)


# On définit une fonction qui adapte nos images à l'entrée du réseau faceNet
def transformer_image(image, dimensions=(224, 224)):
    image = Image.fromarray(image)
    image = image.resize(dimensions)
    return asarray(image)


i = 0
# On calcule la représentation des images avec faceNet
def calculer_vecteur(path):
    image = open_image(path)
    image_adapter = transformer_image(image)
    mean, std = image_adapter.mean(), image_adapter.std()
    image_adapter = (image_adapter - mean) / std
    image_adapter = np.expand_dims(image_adapter, axis=0)
    vecteur = model.predict(image_adapter)
    global i
    i += 1
    print(i)
    return vecteur[0].tolist()


meta_data_imdb['vecteur'] = meta_data_imdb.file_path.apply(lambda x: calculer_vecteur(x))
meta_data_imdb.to_csv("resources/vectorisation/imdb_metadata_vgg.csv")
