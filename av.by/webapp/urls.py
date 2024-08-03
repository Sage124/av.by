from django.urls import path
from rest_framework import routers
from .views import *

urlpatterns = [
    path('v1/cars/retrieve/', CarRetrieveListView.as_view()),
    path('v1/cars/retrieve/<int:pk>', CarRetrieveView.as_view()),
    path('v1/cars/retrieve_own/', CarRetrieveOwn.as_view()),
    path('v1/cars/create/', CarCreateView.as_view()),
    path('v1/cars/update/<int:pk>', CarUpdateView.as_view()),
]
