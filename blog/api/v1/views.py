from django.utils import timezone
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from blog.api.v1.permissions import ArticlePermissions
from blog.api.v1.serializers import ArticleSerializer
from blog.models import Article


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, ArticlePermissions, )
    queryset = Article.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            Q(status=Article.Statuses.PUBLISHED, is_private=False) |
            Q(user=self.request.user)
        )

    def perform_create(self, serializer):
        now = timezone.now()
        serializer.save(
            creation_date=now,
            last_modification_date=now,
            user=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(last_modification_date=timezone.now())
