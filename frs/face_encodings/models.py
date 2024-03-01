import decimal

from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction


class ImageFaceEncoding(models.Model):
    file_hash = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"ImageFaceEncoding(file_hash={self.file_hash})"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.full_clean()

    async def get_face_encoding(self):
        face_encoding_values = self.faceencodingvalue_set.order_by("index")
        return [
            [float(decimal.Decimal(fev.value)) async for fev in face_encoding_values],
        ]

    async def insert_face_encoding(self, face_encoding):
        for i, value in enumerate(face_encoding):
            fev = FaceEncodingValue(image=self, index=i, value=value)
            await sync_to_async(fev.save)()
        return await sync_to_async(self.faceencodingvalue_set.count)()


class FaceEncodingValue(models.Model):
    image = models.ForeignKey(ImageFaceEncoding, on_delete=models.CASCADE)
    index = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)],
    )
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = ["index", "image"]

    def __str__(self):
        return f"FaceEncodingValue(image={self.image}, index={self.index})"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.full_clean()

    def clean(self):
        try:
            decimal.Decimal(self.value)
        except decimal.InvalidOperation as exc:
            raise ValidationError({"value": "Not a decimal number."}) from exc


class AverageFaceEncoding(models.Model):
    number_of_images_processed = models.PositiveIntegerField()

    def __str__(self):
        return "AverageFaceEncoding()"

    def get_face_encoding(self):
        face_encoding_values = self.averagefaceencodingvalue_set.order_by("index")
        if self.number_of_images_processed == 0:
            return list(range(128))
        return [
            [
                float(
                    decimal.Decimal(fev.value)
                    / decimal.Decimal(self.number_of_images_processed),
                )
                for fev in face_encoding_values
            ],
        ]

    @transaction.atomic
    def update_average_face_encodings(self, image_face_encoding):
        self.number_of_images_processed += 1
        self.save()
        for i in range(128):
            added_value = image_face_encoding.faceencodingvalue_set.get(index=i).value
            value = self.averagefaceencodingvalue_set.get(index=i).value
            new_value = decimal.Decimal(added_value) + decimal.Decimal(value)
            self.averagefaceencodingvalue_set.filter(index=i).update(
                value=str(new_value),
            )


class AverageFaceEncodingValue(models.Model):
    average_face_encoding = models.ForeignKey(
        AverageFaceEncoding,
        on_delete=models.CASCADE,
    )
    index = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(0), MaxValueValidator(127)],
    )
    value = models.CharField(max_length=256)

    def __str__(self):
        return f"AverageFaceEncodingValue(index={self.index})"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.full_clean()
