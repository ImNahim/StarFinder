from django.shortcuts import render
from .forms import FaceForm
from .models import *
import starapp

import os
import time
import base64
import requests

from .backend import main

def save_img_from_base64_string(base64_string, path):
    message_bytes = base64.b64decode(base64_string)
    with open(path, "wb") as fh:
        fh.write(message_bytes)

def get_base64_img(path):
  with open(path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    return encoded_string



def merge_star(request):
    current_save = saveById(request)
    if (not current_save or not current_save.star_face or current_save.merge_face):
        return index(request)

    path = os.path.abspath(starapp.__path__[0]).replace('\\starapp','')
    your_face_url = current_save.your_face.face_Img.url.replace('/','\\')
    star_face_url = current_save.star_face.face_Img.url.replace('/','\\')

    print('mergeStar called')
    face = Face()

    server_url = 'https://26fbaaa206de.ngrok.io'

    data = {
        'your_face': str(get_base64_img(path + your_face_url)),
        'star_face': str(get_base64_img(path + star_face_url))
    }

    response = requests.post(server_url, data=data)

    if (response.status_code != 200):
        print('Error !', response.status_code)
        face.face_Img = 'harrymacrontter.jpg'
    else:
        print('images uploaded successfuly !')

        response_morph = 'Not yet'
        i = 0
        while (response_morph == 'Not yet'):
            i += 5
            time.sleep(5)
            print('Not yet', i)
            response = requests.get(server_url)
            if (response.status_code != 200):
                print('Error !', response.status_code)
                face.face_Img = 'harrymacrontter.jpg'
                response_morph = None
            else:
                response_morph = response.json()['morph']

        if (response_morph):
            morph_rel_path = "morph" + str(current_save.id) + ".png"
            save_img_from_base64_string(response[2:-1], path + "\\media\\" + morph_rel_path)
            print('morphing image received !')
            face.face_Img = morph_rel_path

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

    face.face_Img, star_name = main.main(abs_path)
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
