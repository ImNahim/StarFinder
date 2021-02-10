import numpy as np
from numpy import asarray
from PIL import Image
import cv2
from mtcnn.mtcnn import MTCNN


def prendre_photo():
    video_capture_object = cv2.VideoCapture(0)
    result = True
    print("Entrez votre Nom :")
    name = input()
    path = name + ".jpg"
    while result:
        ret, frame = video_capture_object.read()
        cv2.imshow('frame', frame)
        cv2.imwrite(path, frame)
        result = False
    cv2.waitKey(0)
    video_capture_object.release()
    cv2.destroyAllWindows()
    return path


def open_image(path):
    try:
        image = Image.open(path)
        image = image.convert('RGB')
        #image.show()
        return asarray(image)
    except FileNotFoundError:
        print("path : " + path + "n'existe pas")


def detecter_visage(path):
    image = open_image(path)
    # On va utiliser mtcnn pour détecter le visage seulement
    detector = MTCNN()
    # On resize l'image pour qu'elle soit compatible avec le réseau ResNet
    detections = detector.detect_faces(image)
    x1, y1, width, height = detections[0]['box']
    dw = round(width * 0) + 20
    dh = round(height * 0) + 20
    x2, y2 = x1 + width + dw, y1 + height + dh
    face = image[y1:y2, x1:x2]
    return face


def adapter_image(face, dimension=(160, 160)):
    face = Image.fromarray(face)
    face = face.resize(dimension)
    return asarray(face)

def preprocess(path):
    detecteur = detecter_visage(path)
    image_adapter = adapter_image(detecteur)
    image_adapter = image_adapter.astype('float32')
    mean, std = image_adapter.mean(), image_adapter.std()
    image_adapter = (image_adapter - mean) / std
    image_adapter = np.expand_dims(image_adapter, axis=0)
    return image_adapter


def calcul_vecteur(path, model):
    image_adapter = preprocess(path)
    vecteur = model.predict(image_adapter)
    return vecteur[0]
