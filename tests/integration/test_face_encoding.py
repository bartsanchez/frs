from pathlib import Path

import requests

from .samples.expected_values import SCHUMACHER_003_FACE_ENCODING

BASE_URL = "http://frs:8000"
URL = f"{BASE_URL}/generate_face_encoding"


def test_sample_schumacher_face_encoding():
    with Path("./samples/Michael_Schumacher_0003.jpg").open("rb") as f:
        files = {"upload_file": f}
        r = requests.post(URL, data={}, files=files, timeout=5)

    assert r.status_code == requests.codes.ok
    assert r.json()["message"] == "OK"
    assert r.json()["face_encoding"] == SCHUMACHER_003_FACE_ENCODING
