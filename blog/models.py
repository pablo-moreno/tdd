from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    class Statuses(models.TextChoices):
        DRAFT = 'DRF', _('Draft')
        PUBLISHED = 'PUB', _('Published')

    text = models.CharField(max_length=280)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_created=True, blank=True)
    last_modification_date = models.DateTimeField(auto_created=True, blank=True)
    status = models.CharField(max_length=3, choices=Statuses.choices, default=Statuses.DRAFT)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ('-creation_date', )
