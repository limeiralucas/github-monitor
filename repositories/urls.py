from django.urls import path

from .views import CommitsView, repository_create_view

app_name = 'repositories'

urlpatterns = [
    path('api/commits/', CommitsView.as_view(), name='commits-list'),
    path('api/repositories/', repository_create_view, name='repositories-create'),
]
