from django.core.exceptions import ValidationError
from django.test import TestCase

from face_encodings import models


class ImageFaceEncodingTests(TestCase):
    def test_image_face_encoding(self):
        self.assertEqual(models.ImageFaceEncoding.objects.count(), 0)

        image_face_encoding = models.ImageFaceEncoding(file_hash="foo")
        image_face_encoding.save()

        self.assertEqual(models.ImageFaceEncoding.objects.count(), 1)

        image_face_encoding = models.ImageFaceEncoding.objects.get()
        self.assertEqual(image_face_encoding.file_hash, "foo")
        self.assertEqual(str(image_face_encoding), "ImageFaceEncoding(file_hash=foo)")


class FaceEncodingValueTests(TestCase):
    def setUp(self):
        self.image_face_encoding = models.ImageFaceEncoding(file_hash="foo")
        self.image_face_encoding.save()

    def test_face_encoding_value(self):
        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

        face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=3,
            value="-0.1",
        )
        face_encoding_value.save()

        self.assertEqual(models.FaceEncodingValue.objects.count(), 1)

        face_encoding_value = models.FaceEncodingValue.objects.get()
        self.assertEqual(face_encoding_value.image.file_hash, "foo")
        self.assertEqual(face_encoding_value.index, 3)
        self.assertEqual(face_encoding_value.value, "-0.1")

    def test_face_encoding_value__two_entries(self):
        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

        face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=3,
            value="-0.1",
        )
        face_encoding_value.save()

        another_face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=7,
            value="1.42",
        )
        another_face_encoding_value.save()

        self.assertEqual(models.FaceEncodingValue.objects.count(), 2)

    def test_face_encoding_value__index_low(self):
        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

        face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=-1,
            value="1.42",
        )
        with self.assertRaises(ValidationError) as exc:
            face_encoding_value.save()
        self.assertEqual(
            str(exc.exception),
            "{'index': ['Ensure this value is greater than or equal to 0.']}",
        )

        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

    def test_face_encoding_value__index_high(self):
        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

        face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=128,
            value="1.42",
        )
        with self.assertRaises(ValidationError) as exc:
            face_encoding_value.save()
        self.assertEqual(
            str(exc.exception),
            "{'index': ['Ensure this value is less than or equal to 127.']}",
        )

        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

    def test_face_encoding_value__value_not_decimal(self):
        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)

        face_encoding_value = models.FaceEncodingValue(
            image=self.image_face_encoding,
            index=25,
            value="a",
        )
        with self.assertRaises(ValidationError) as exc:
            face_encoding_value.save()
        self.assertEqual(str(exc.exception), "{'value': ['Not a decimal number.']}")

        self.assertEqual(models.FaceEncodingValue.objects.count(), 0)
