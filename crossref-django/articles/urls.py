from django.urls import path
from .views import get_article_info_by_dois

urlpatterns = [
    path('get-article-info-by-doi', get_article_info_by_dois, name='get-article-info-by-doi'),
]
