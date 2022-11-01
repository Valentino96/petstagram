def megabytes_to_bytes(mb):
    return mb * 1024 * 1024


def apply_likes_count(photo):
    photo.likes_count = photo.photolike_set.count()
    return photo


def apply_user_liked_photos(photo):
    photo.is_liked_by_user = photo.likes_count > 0
    return photo