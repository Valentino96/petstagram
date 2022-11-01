from django import forms
from django.core.exceptions import ValidationError

from petstagram.common.models import PhotoLike, PhotoComment
from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('publication_date',)


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'photo')


class PhotoDeleteForm(PhotoBaseForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__disable_fields()

    def __disable_fields(self):
        for name, field in self.fields.items():
            # field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        if commit:
            self.instance.tagged_pets.clear()
            PhotoLike.objects.filter(photo_id=self.instance.pk).delete()
            PhotoComment.objects.filter(photo_id=self.instance.pk).delete()
            self.instance.delete()

        return self.instance

