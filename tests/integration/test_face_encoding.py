import decimal
import time
from pathlib import Path

import requests

from .samples.expected_values import (
    COMPONENT_WISE_AVERAGE,
    MOORE_001_FACE_ENCODING,
    SCHUMACHER_003_FACE_ENCODING,
)

BASE_URL = "http://load-balancer"
STATS_URL = f"{BASE_URL}/stats"
FACE_ENCODING_URL = f"{BASE_URL}/face_encoding"
GFE_URL = f"{BASE_URL}/generate_face_encoding"


def test_zero_processed_images_at_first():
    r = requests.get(STATS_URL, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["number_of_images_processed"] == 0


def test_sample_schumacher_face_encoding():
    with Path("./samples/Michael_Schumacher_0003.jpg").open("rb") as f:
        files = {"upload_file": f}
        r = requests.post(GFE_URL, data={}, files=files, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["message"] == "OK"
    assert r.json()["face_encoding"] == SCHUMACHER_003_FACE_ENCODING


def test_one_processed_images_later():
    time.sleep(3)
    r = requests.get(STATS_URL, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["number_of_images_processed"] == 1


def test_get_schumacher_face_encoding():
    with Path("./samples/Michael_Schumacher_0003.jpg").open("rb") as f:
        files = {"upload_file": f}
        r = requests.post(GFE_URL, data={}, files=files, timeout=5)
    assert r.status_code == requests.codes.ok

    file_hash = r.json()["file_hash"]

    r = requests.get(f"{FACE_ENCODING_URL}/{file_hash}", timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["message"] == "OK"
    assert r.json()["face_encoding"] == SCHUMACHER_003_FACE_ENCODING


def test_still_one_processed_images():
    time.sleep(3)
    r = requests.get(STATS_URL, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["number_of_images_processed"] == 1


def test_sample_julianne_moore_face_encoding():
    with Path("./samples/Julianne_Moore_0001.jpg").open("rb") as f:
        files = {"upload_file": f}
        r = requests.post(GFE_URL, data={}, files=files, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["message"] == "OK - Multiple faces. Returning first"
    assert r.json()["face_encoding"] == MOORE_001_FACE_ENCODING


def test_two_processed_images_now():
    time.sleep(3)
    r = requests.get(STATS_URL, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["number_of_images_processed"] == 2  # noqa: PLR2004

    average_face_encodings = r.json()["average_face_encodings"][0]
    for i in range(128):
        diff_value = decimal.Decimal(average_face_encodings[i]) - decimal.Decimal(
            COMPONENT_WISE_AVERAGE[i],
        )
        assert abs(diff_value) < decimal.Decimal("0000000000000000000000000000.1")
