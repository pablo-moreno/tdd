from rest_framework.routers import DefaultRouter
from blog.api.v1.views import ArticleViewSet

router = DefaultRouter()
router.register('', ArticleViewSet)

urlpatterns = router.urls
