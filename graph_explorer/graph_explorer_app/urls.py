from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("save-workspace/", views.save_workspace, name="save_workspace"),
    path("select-workspace/", views.select_workspace, name="select_workspace"),
    path("select-visualizer/", views.select_visualizer, name="select_visualizer"),
    path("apply-filter/", views.apply_filter, name="apply_filter"),
    path("remove-filter/", views.remove_filter, name="remove_filter"),
    path("apply-search/", views.apply_search, name="apply_search"),
    path("remove-search/", views.remove_search, name="remove_search"),
]