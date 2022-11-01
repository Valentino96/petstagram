from django.shortcuts import render, redirect

from petstagram.core.utils import apply_user_liked_photos, apply_likes_count
from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.pets.utils import get_pet_by_name_and_username


def details_pet(request, pet_slug, username):
    pet = get_pet_by_name_and_username(pet_slug, username)
    photos = [apply_likes_count(photo) for photo in pet.photo_set.all()]
    photos = [apply_user_liked_photos(photo) for photo in photos]
    context = {
        'pet': pet,
        'photos_count': pet.photo_set.count(),
        'pet_photo': photos
    }
    return render(request, 'pets/pet-details-page.html', context)


def add_pet(request):
    if request.method == 'GET':
        form = PetCreateForm()
    else:
        form = PetCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('details user', pk=1)
    context = {
        'form': form,
    }
    return render(request, 'pets/pet-add-page.html', context)


def edit_pet(request, username, pet_slug):
    pet = Pet.objects.filter(pet_slug=pet_slug).get()
    if request.method == 'GET':
        form = PetEditForm(instance=pet)
    else:
        form = PetEditForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('details pet', username=username, pet_slug=pet_slug)
    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
    }
    return render(request, 'pets/pet-edit-page.html', context)


def delete_pet(request, username, pet_slug):
    pet = Pet.objects.filter(pet_slug=pet_slug).get()
    if request.method == 'GET':
        form = PetDeleteForm(instance=pet)
    else:
        form = PetEditForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('details user', pk=1)
    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
    }
    return render(request, 'pets/pet-delete-page.html', context)

