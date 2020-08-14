from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
     path('create',views.create,name="create"),
     path('search',views.search,name='search'),
     path('random',views.rand,name='random'),
     path('edit',views.edit,name='edit'),
    path("<str:title>",views.view,name="title"),
   
]
