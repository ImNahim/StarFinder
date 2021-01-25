from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:save_id>', views.index, name='save'),
    path('reset', views.index_reset, name='reset'),
    path('book/<int:book_id>', views.book_by_id, name='book_by_id'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)