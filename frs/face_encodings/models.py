from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ImageFaceEncoding(models.Model):
    file_hash = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"ImageFaceEncoding(file_hash={self.file_hash})"


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
