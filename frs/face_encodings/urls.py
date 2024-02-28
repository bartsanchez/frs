from django.urls import path

from . import views

urlpatterns = [
    path(
        "generate_face_encoding",
        views.generate_face_encoding,
        name="generate_face_encoding",
    ),
]
