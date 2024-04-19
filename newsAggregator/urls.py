from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.login, name='login'),
    path('api/logout', views.logout, name='logout'),
    path('api/stories', views.modify_story, name='modify_story'),
    path('api/stories/<int:story_key>', views.delete_story, name='delete_story'),
    path('api/directory', views.directory, name='directory'),
]
