from django.db import models

from petstagram.photos.models import Photo


class PhotoComment(models.Model):
    text = models.CharField(
        max_length=300,
        null=False,
        blank=False,

    )
    publication_date_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )


class PhotoLike(models.Model):
    photo = models.ForeignKey(
        Photo,
        on_delete=models.RESTRICT,
        blank=True,
        null=False,
    )

