from django.shortcuts import render
from .forms import *



def index_reset(request):
    request.session['current_save'] = None
    return index(request)

def index(request, save_id=None):
    def saveById():
        mid = save_id
        if not mid:
            try:
                mid = request.session['current_save']
            except (KeyError):
                return None
        try:
            return Save.objects.get(id=mid)
        except (KeyError, Save.DoesNotExist):
            return None

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
            print('image successfully uploaded')
            current_save = Save(your_face=face)
            current_save.save()
            print('save successfully created')
            request.session['current_save'] = current_save.id
            context['save'] = current_save
            return render(request, 'index.html', context)

    if request.method == 'GET':
        if save_id:
            current_save = saveById()
            if current_save:
                print("save found")
                request.session['current_save'] = save_id
            else:
                current_save = saveById()
        else:
            current_save = saveById()

        if current_save:
            context['save'] = current_save
            if current_save.your_face:
                return render(request, 'index.html', context)

    context['form'] = FaceForm()
    return render(request, 'index.html', context)
