from django.urls import path
from . import views

urlpatterns = [
    path('input_images/',views.upload, name='upload'),
path('photo_wake_up/',views.download, name='download')
]