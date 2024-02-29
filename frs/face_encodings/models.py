import decimal

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
