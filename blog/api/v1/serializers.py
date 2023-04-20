from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = ('user', 'last_modification_date', 'creation_date')
        fields = '__all__'
