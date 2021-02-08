from django.shortcuts import render
from .forms import *
import starapp

import time
import os

def find_star(request):
    current_save = saveById(request)
    if (not current_save):
        return index(request)

    path = os.path.abspath(starapp.__path__[0]).replace('\\starapp','')
    img_url = current_save.your_face.face_Img.url.replace('/','\\')
    abs_path = path + img_url
    print(abs_path)

    # appeller fonction lente
    print('findStar called')
    face = Face()
    # face.face_Img = findStar()
    face.face_Img = 'cat_hokusai_tCakvVH.png' # supprimer et remplacer par la ligne du dessus
    time.sleep(5) # supprimer
    face.save()
    print('findStar returned')

    current_save.star_face = face
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
