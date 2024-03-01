import decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction


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
