from django.test import TestCase
from django.urls import reverse


class GenerateFaceEncodingViewTests(TestCase):
    def setUp(self):
        self.url = reverse("generate_face_encoding")

    def test_generate_face_encoding_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_generate_face_encoding_POST(self):
        response = self.client.post(
            self.url,
            data={},
        )
        self.assertEqual(response.status_code, 200)
