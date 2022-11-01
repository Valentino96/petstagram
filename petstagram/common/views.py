from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import PhotoCommentForm, SearchPhotosForm
from petstagram.common.models import PhotoLike
from petstagram.core.utils import apply_likes_count, apply_user_liked_photos
from petstagram.photos.models import Photo


def index(request):
    search_form = SearchPhotosForm(request.GET)
    search_pattern = None

    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['pet_name']
    photos = Photo.objects.all()
    if search_pattern:
        photos = photos.filter(tagged_pets__name__icontains=search_pattern)
    photos = [apply_likes_count(photo) for photo in photos]
    photos = [apply_user_liked_photos(photo) for photo in photos]

    context = {
        'photos': photos,
        'comment_form': PhotoCommentForm(),
        'search_form' : search_form,
    }
    return render(request, 'common/home-page.html', context)


def get_user_liked_photos(photo_id):
    photo_likes = PhotoLike.objects.filter(photo_id=photo_id)
    return photo_likes


def like_photo(request, photo_id):
    user_liked_photos = get_user_liked_photos(photo_id)
    if user_liked_photos:
        user_liked_photos.delete()
    else:
        photo_like = PhotoLike(
            photo_id=photo_id,
        )
        photo_like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#photo-{photo_id}')


def share_photo(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))
    return redirect(request.META['HTTP_REFERER'] + f'#photo-{photo_id}')


def comment_photo(request, photo_id):
    photo = Photo.objects.filter(pk=photo_id).get()

    form = PhotoCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        photo.photocomment_set.add(comment)
        photo.save()

    return redirect('index')
