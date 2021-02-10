import ast
import numpy as np
import pandas as pd
from keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image
from .calculVectUser import calcul_vecteur

import os
path = os. getcwd()


# On load le model faceNet pré-etrainé ainsi que l'ensemble de ses poids
#model = load_model("/res/model/model/facenet_keras.h5")
#model.load_weights("/res/model/weights/facenet_keras_weights.h5")


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

    # On return un numpy array
    return np.asarray(ast.literal_eval(vecteur)).astype('float32')


def afficher_deux_images(img1, img2, nom_utilisateur, nom_celebrite='', fs=12):
    f, axarr = plt.subplots(1, 2, figsize=(fs, fs))
    axarr[0].imshow(img1)
    axarr[0].title.set_text(nom_utilisateur)
    axarr[1].imshow(img2)
    axarr[1].title.set_text(nom_celebrite)
    plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
    plt.show()


# On affiche les  célébrités qui ressemblent le plus
def afficher_celebrite(data_frame, path_image_utilisateur, nom_utilisateur, number=3):
    for i in range(number):
        instance = data_frame.iloc[i]
        full_path = instance['file_path']
        full_path = os.path.join(os.getcwd(), 'starapp','backend', full_path)
        nom_celebrite = instance['name']
        try:
            img1 = Image.open(path_image_utilisateur)
            img2 = Image.open(full_path).resize((512, 512))
            afficher_deux_images(img1, img2, nom_utilisateur, nom_celebrite)

        except FileNotFoundError:
            print("L'image n'existe pas : " + full_path)

def celebrity_path_and_name(data_frame):
    instance = data_frame.iloc[0]
    full_path = instance['file_path']
    full_path = os.path.join(os.getcwd(), 'starapp','backend', full_path)
    nom_celebrite = instance['name']
    return full_path, nom_celebrite


def main(path, vect, nom_utilisateur=''):
    path_df = os.path.join(os.getcwd(), 'starapp', 'backend','resources/vectorisation/imdb_metadata_v.csv')
    meta_data = pd.read_csv(path_df)
    meta_data["vecteur"] = meta_data["vecteur"].apply(lambda x: convert_en_string(x))
    meta_data['distance'] = meta_data['vecteur'].apply(lambda x: calculer_distance(x, vect))
    meta_data = meta_data.sort_values(by=['distance'], ascending=True)
    # afficher_celebrite(meta_data, path, nom_utilisateur)
    #return meta_data
    return celebrity_path_and_name(meta_data)

if __name__ == '__main__':
    print('Entrez votre prénom')
    nom = input()
    main("starfinder/starwebsite/media/test.jpg",model =None, nom='')
