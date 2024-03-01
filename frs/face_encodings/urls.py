from django.urls import path

from . import views

urlpatterns = [
    path(
        "generate_face_encoding",
        views.generate_face_encoding,
        name="generate_face_encoding",
    ),
    path(
        r"face_encoding/<str:file_hash>",
        views.face_encoding,
        name="face_encoding",
    ),
    path(
        "stats",
        views.stats,
        name="stats",
    ),
]
