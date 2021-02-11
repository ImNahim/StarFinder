import ast
import numpy as np
import pandas as pd
import os

from .calculVectUser import calcul_vecteur

from keras.models import load_model

model = load_model(os.path.join(os.getcwd(), 'starapp/backend/resources/model/model','facenet_keras.h5'))
model.load_weights(os.path.join(os.getcwd(), 'starapp/backend/resources/model/weights','facenet_keras_weights.h5'))

# On calcule la similarité cosinus pour le vecteur représentant l'utilisateur et les vecteurs de la dataset
def calculer_distance(vecteur_dataset, vecteur_utilisateur):
    try:
        produit_vect = np.matmul(np.transpose(vecteur_dataset), vecteur_utilisateur)
        norme_data = np.sum(np.multiply(vecteur_dataset, vecteur_dataset))
        norme_uti = np.sum(np.multiply(vecteur_utilisateur, vecteur_utilisateur))
        return 1 - (produit_vect / (np.sqrt(norme_data) * np.sqrt(norme_uti)))
    except:
        return 2  # on retourne une grande valeur le cas échéant


# Convertir les vecteurs en numpy array
def convert_en_string(vecteur):
    vecteur = vecteur.replace('\n', '').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ',' ').replace('[ ', '[').replace(' ]', ']').replace(' ', ', ')
    return np.asarray(ast.literal_eval(vecteur)).astype('float32')

def celebrity_path_and_name(data_frame):
    instance = data_frame.iloc[0]
    path = instance['file_path']
    nom_celebrite = instance['name']
    return path, nom_celebrite


def main(path):
    vect_embedding = calcul_vecteur(path, model)
    print(vect_embedding)

    path_df = os.path.join(os.getcwd(), 'starapp', 'backend','resources/vectorisation/imdb_metadata_v.csv')
    meta_data = pd.read_csv(path_df)
    meta_data["vecteur"] = meta_data["vecteur"].apply(lambda x: convert_en_string(x))
    meta_data['distance'] = meta_data['vecteur'].apply(lambda x: calculer_distance(x, vect_embedding))
    meta_data = meta_data.sort_values(by=['distance'], ascending=True)
    return celebrity_path_and_name(meta_data)
