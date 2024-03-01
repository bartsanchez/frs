import time
from pathlib import Path

import requests

from .samples.expected_values import SCHUMACHER_003_FACE_ENCODING

BASE_URL = "http://frs:8000"
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
