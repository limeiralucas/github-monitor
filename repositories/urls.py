from django.urls import path

from .views import CommitsView, RepositoriesView

app_name = 'repositories'

urlpatterns = [
    path('api/commits/', CommitsView.as_view(), name='commits-list'),
    path('api/repositories/', RepositoriesView.as_view(), name='repositories-create'),
]
