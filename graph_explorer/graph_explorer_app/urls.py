from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("save-workspace/", views.save_workspace, name="save_workspace"),
    path("select-workspace/", views.select_workspace, name="select_workspace"),
    path("select-visualizer/", views.select_visualizer, name="select_visualizer"),

]