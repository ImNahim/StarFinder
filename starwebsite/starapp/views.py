from django.shortcuts import render
from .forms import *
import starapp

import time
import os

from keras.models import load_model
from .backend import main, calculVectUser
from .models import Model


def merge_star(request):
    current_save = saveById(request)
    if (not current_save or not current_save.star_face or current_save.merge_face):
        return index(request)

    path = os.path.abspath(starapp.__path__[0]).replace('\\starapp','')
    img_url = current_save.star_face.face_Img.url.replace('/','\\')
    abs_path = path + img_url
    print(abs_path)

    print('mergeStar called')
    face = Face()

    # face.face_Img = mergeStar()
    face.face_Img = 'harrymacrontter.jpg' # supprimer et remplacer par la ligne du dessus
    time.sleep(5) # supprimer

    face.save()
    print('mergeStar returned')

    current_save.merge_face = face
    current_save.save()
    return index(request, current_save.id)


def find_star(request):
    current_save = saveById(request)
    if (not current_save or current_save.star_face):
        return index(request)

    path = os.path.abspath(starapp.__path__[0]).replace('\\starapp','')
    img_url = current_save.your_face.face_Img.url.replace('/','\\')
    abs_path = path + img_url
    print(abs_path)

    print('findStar called')
    face = Face()

    image_adapter = calculVectUser.preprocess(abs_path)
    vect_embedding = Model.predict(image_adapter)[0]
    print(vect_embedding)

    face.face_Img, star_name = main.main(abs_path, vect_embedding)
    face.save()
    print('findStar returned')
    print(face.face_Img)

    current_save.star_face = face
    current_save.star_name = star_name
    current_save.save()
    return index(request, current_save.id)

def index_reset(request):
    request.session['current_save_id'] = None
    return index(request)

def saveById(request, save_id=None):
    if not save_id:
        try:
            save_id = request.session['current_save_id']
        except (KeyError):
            return None
    try:
        return Save.objects.get(id=save_id)
    except (KeyError, Save.DoesNotExist):
        return None

def index(request, save_id=None):
    # get hisoric of matches
    context = {}
    try:
        historic = Save.objects.all().order_by('-id')
        context['historic'] = historic
    except (KeyError, Save.DoesNotExist):
        historic = None

    # when uploading image
    if request.method == 'POST':
        form = FaceForm(request.POST, request.FILES)
        if form.is_valid():
            face = form.save()
            current_save = Save(your_face=face)
            current_save.save()
            request.session['current_save_id'] = current_save.id
            context['save'] = current_save
            return render(request, 'index.html', context)

    if request.method == 'GET':
        if save_id:
            current_save = saveById(request, save_id)
            if current_save:
                print("save found")
                request.session['current_save_id'] = save_id
            else:
                current_save = saveById(request)
        else:
            current_save = saveById(request)

        if current_save:
            context['save'] = current_save
            if current_save.your_face:
                return render(request, 'index.html', context)

    context['form'] = FaceForm()
    return render(request, 'index.html', context)
