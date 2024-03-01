from pathlib import Path
from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse


class GenerateFaceEncodingViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("generate_face_encoding")
        self.images_path = f"{settings.BASE_DIR}/face_encodings/tests/samples"

    def tearDown(self):
        cache.clear()

    @mock.patch(
        "face_recognition.face_encodings",
        return_value=[list(range(128))],
    )
    def test_generate_face_encoding__dont_process_twice(self, face_encoding_mock):
        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            first_response = self.client.post(
                self.url,
                data={"upload_file": f},
            )

        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            second_response = self.client.post(
                self.url,
                data={"upload_file": f},
            )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.json()["message"], "OK")
        self.assertEqual(
            first_response.json()["face_encoding"],
            list(range(128)),
        )

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.json()["message"], "OK")
        self.assertEqual(
            second_response.json()["face_encoding"],
            list(range(128)),
        )

        face_encoding_mock.assert_called_once()
        self.assertEqual(face_encoding_mock.call_count, 1)
