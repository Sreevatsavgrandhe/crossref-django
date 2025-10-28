from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['doi', 'title', 'authors', 'published_date', 'peer_review', 'raw']
