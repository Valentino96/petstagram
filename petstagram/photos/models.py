from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_file_less_than_5mb


class Photo(models.Model):
    photo = models.ImageField(
        upload_to='pet_photos/',
        null=False,
        blank=True,
        validators=[validate_file_less_than_5mb]
    )
    description = models.TextField(
        max_length=300,
        validators=[MinLengthValidator(10)],
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    publication_date = models.DateField(
        auto_now=True,
        null=False,
        blank=False,
    )
    tagged_pets = models.ManyToManyField(
        Pet,
        blank=True
    )

