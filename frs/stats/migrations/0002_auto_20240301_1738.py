# Generated by Django 5.0.2 on 2024-03-01 17:38
from django.db import migrations


def generate_average_face_encoding_instance(apps, schema_editor):  # noqa: ARG001
    AverageFaceEncodingValue = apps.get_model(
        "stats",
        "AverageFaceEncodingValue",
    )
    AverageFaceEncoding = apps.get_model("stats", "AverageFaceEncoding")

    average_face_encoding = AverageFaceEncoding(number_of_images_processed=0)
    average_face_encoding.save()

    for i in range(128):
        ave = AverageFaceEncodingValue(
            average_face_encoding=average_face_encoding,
            index=i,
            value=0,
        )
        ave.save()


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0001_initial"),
    ]

    operations = [migrations.RunPython(generate_average_face_encoding_instance)]
