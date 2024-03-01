import decimal
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from face_encodings import models


class DBAccessForExistingDataTests(TestCase):
    def setUp(self):
        self.url = reverse("generate_face_encoding")
        self.images_path = f"{settings.BASE_DIR}/face_encodings/tests/samples"

    @mock.patch("face_encodings.views.cache.get", return_value=[])
    def test_generate_face_encoding__get_from_db(self, cache_get_mock):
        image_face_encoding = models.ImageFaceEncoding(
            file_hash="9300d3c14e83f9dca75e135363b4a29297a4654f521b321240b0466780c27bed",
        )
        image_face_encoding.save()
        for i in range(128):
            models.FaceEncodingValue(image=image_face_encoding, index=i, value=i).save()

        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            first_response = self.client.post(
                self.url,
                data={"upload_file": f},
            )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.json()["message"], "OK")
        self.assertEqual(
            first_response.json()["face_encoding"],
            [float(decimal.Decimal(i)) for i in range(128)],
        )

        cache_get_mock.assert_called_once()
