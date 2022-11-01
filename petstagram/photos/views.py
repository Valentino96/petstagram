from django.shortcuts import render, redirect
from django.urls import reverse

from petstagram.common.views import get_user_liked_photos
from petstagram.pets.models import Pet
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from petstagram.photos.models import Photo


def details_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    context = {
        'photo': photo,
        'has_user_liked_photo': get_user_liked_photos(pk),
        'likes_count': photo.photolike_set.count()
    }
    return render(request, 'photos/photo-details-page.html', context)


def get_post_photo_form(request, form, success_url, template_url, pk=None):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(success_url)

    context = {
        'form': form,
        'pk': pk,

    }
    return render(request, template_url, context)


def add_photo(request):
    if request.method == 'GET':
        form = PhotoCreateForm
    else:
        form = PhotoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            return redirect('delete photo', pk=photo.pk)
    context = {
        'form': form
    }
    return render(request, 'photos/photo-add-page.html', context)


def edit_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    return get_post_photo_form(
        request,
        PhotoEditForm(request.POST or None, instance=photo),
        success_url=reverse('index'),
        template_url='photos/photo-edit-page.html',
        pk=pk,
    )


def delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    return get_post_photo_form(
        request,
        PhotoDeleteForm(request.POST or None, instance=photo),
        success_url=reverse('index'),
        template_url='photos/photo-delete-page.html',
        pk=pk
    )

