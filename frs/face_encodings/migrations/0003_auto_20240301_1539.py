# Generated by Django 5.0.2 on 2024-03-01 15:39

from django.db import migrations


def generate_average_face_encoding_instance(apps, schema_editor):  # noqa: ARG001
    AverageFaceEncodingValue = apps.get_model(
        "face_encodings",
        "AverageFaceEncodingValue",
    )
    AverageFaceEncoding = apps.get_model("face_encodings", "AverageFaceEncoding")

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
        ("face_encodings", "0002_averagefaceencoding_averagefaceencodingvalue"),
    ]

    operations = [migrations.RunPython(generate_average_face_encoding_instance)]
