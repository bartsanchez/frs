import decimal
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .samples.expected_values import (
    COMPONENT_WISE_AVERAGE,
    MOORE_001_FACE_ENCODING,
    SCHUMACHER_003_FACE_ENCODING,
)


class GenerateFaceEncodingViewTests(TestCase):
    def setUp(self):
        self.url = reverse("generate_face_encoding")
        self.images_path = f"{settings.BASE_DIR}/face_encodings/tests/samples"

    def test_generate_face_encoding_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_generate_face_encoding_POST(self):
        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            response = self.client.post(
                self.url,
                data={"upload_file": f},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "OK")
        self.assertEqual(response.json()["face_encoding"], SCHUMACHER_003_FACE_ENCODING)

    def test_generate_face_encoding_POST__no_face(self):
        with Path(f"{self.images_path}/1x1-black.jpg").open("rb") as f:
            response = self.client.post(
                self.url,
                data={"upload_file": f},
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["message"], "No faces found!")

    def test_generate_face_encoding_POST__multiple_faces(self):
        with Path(f"{self.images_path}/Julianne_Moore_0001.jpg").open("rb") as f:
            response = self.client.post(
                self.url,
                data={"upload_file": f},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            "OK - Multiple faces. Returning first",
        )
        self.assertEqual(response.json()["face_encoding"], MOORE_001_FACE_ENCODING)

    def test_generate_face_encoding_POST__no_file(self):
        response = self.client.post(
            self.url,
            data={},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["message"], "No image sent!")


class StatsViewTests(TestCase):
    def setUp(self):
        self.url = reverse("stats")
        self.gfe_url = reverse("generate_face_encoding")
        self.images_path = f"{settings.BASE_DIR}/face_encodings/tests/samples"
        cache.clear()

    def test_generate_face_encoding_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["number_of_images_processed"], 0)

    def test_generate_face_encoding__two_images(self):
        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            first_response = self.client.post(
                self.gfe_url,
                data={"upload_file": f},
            )
        self.assertEqual(first_response.status_code, 200)
        with Path(f"{self.images_path}/Julianne_Moore_0001.jpg").open("rb") as f:
            response = self.client.post(
                self.gfe_url,
                data={"upload_file": f},
            )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["number_of_images_processed"], 2)

    def test_calculate_average_face_encodings(self):
        with Path(f"{self.images_path}/Michael_Schumacher_0003.jpg").open("rb") as f:
            first_response = self.client.post(
                self.gfe_url,
                data={"upload_file": f},
            )
        self.assertEqual(first_response.status_code, 200)
        with Path(f"{self.images_path}/Julianne_Moore_0001.jpg").open("rb") as f:
            response = self.client.post(
                self.gfe_url,
                data={"upload_file": f},
            )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        average_face_encodings = response.json()["average_face_encodings"][0]
        for i in range(128):
            diff_value = decimal.Decimal(average_face_encodings[i]) - decimal.Decimal(
                COMPONENT_WISE_AVERAGE[i],
            )
            self.assertTrue(
                abs(diff_value) < decimal.Decimal("0000000000000000000000000000.1"),
            )
