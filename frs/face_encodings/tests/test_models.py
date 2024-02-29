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
