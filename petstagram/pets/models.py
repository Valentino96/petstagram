from django.db import models
from django.utils.text import slugify


class Pet(models.Model):
    MAX_LENGTH_NAME = 30
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        null=False,
        blank=False,
    )
    personal_photo = models.URLField(
        null=False,
        blank=False,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    # human-readable way to show the id
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        # in order to create the object in the DB first
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.name}')
        # in order to update the slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Id={self.id}, Name={self.name}'
