from django.urls import path
from . import views

urlpatterns = [
    path("class/addclass/", views.addclass, name='addclass'),
    path("course/addcourse", views.addcourse, name='addcourse'),
    path("course/certif_instructor", views.addcertif_instructor, name='addcertif_instructor'),
    path("course/certif_assistant", views.addcertif_assistant, name='addcertif_assistant'),
    path("venue/addvenue", views.addvenue, name='addvenue'),
]