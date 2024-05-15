from streaming_app.models import Genre


def create_genre(genre_name):
    try:
        genre_created, created = Genre.objects.get_or_create(name=genre_name.strip())
        return genre_created
    except Genre.DoesNotExist:
        return None