from django.urls import path
from . import views

#list of url path associated with views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('visited', views.places_visited, name='places_visited'),
    path('was_visited', views.place_was_visited, name='place_was_visited'),
    path('place/<int:place_pk>', views.place_details, name ='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
]