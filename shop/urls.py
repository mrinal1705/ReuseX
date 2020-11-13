from django.contrib import admin
from django.urls import path, include
from shop import views



urlpatterns = [
    path('', views.index, name="shophome"),
    path("products/<int:myid>", views.productview, name="Productview"),
    

]