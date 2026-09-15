import unittest
from unittest.mock import patch

import numpy as np

from app import app


class FaceMatchServiceTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_compare_requires_both_files(self):
        response = self.client.post("/compare")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "missing_files"})

    @patch("app.face_recognition.load_image_file", side_effect=ValueError)
    def test_compare_rejects_invalid_images(self, _load_image_file):
        response = self.client.post(
            "/compare",
            data={
                "profile_photo": (self._file(), "profile.jpg"),
                "selfie": (self._file(), "selfie.jpg"),
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "invalid_image"})

    @patch("app.face_recognition.face_encodings", return_value=[])
    @patch("app.face_recognition.load_image_file", return_value=np.zeros((2, 2, 3)))
    def test_compare_reports_no_profile_face(self, _load_image_file, _face_encodings):
        response = self.client.post(
            "/compare",
            data={
                "profile_photo": (self._file(), "profile.jpg"),
                "selfie": (self._file(), "selfie.jpg"),
            },
        )

        self.assertEqual(response.get_json(), {"error": "no_face_detected_in_profile_photo"})

    @patch("app.face_recognition.face_encodings", side_effect=[[np.zeros(128)], []])
    @patch("app.face_recognition.load_image_file", return_value=np.zeros((2, 2, 3)))
    def test_compare_reports_no_selfie_face(self, _load_image_file, _face_encodings):
        response = self.client.post(
            "/compare",
            data={
                "profile_photo": (self._file(), "profile.jpg"),
                "selfie": (self._file(), "selfie.jpg"),
            },
        )

        self.assertEqual(response.get_json(), {"error": "no_face_detected_in_selfie"})

    @patch("app.face_recognition.face_distance", return_value=np.array([0.42]))
    @patch("app.face_recognition.face_encodings", side_effect=[[np.zeros(128)], [np.ones(128)]])
    @patch("app.face_recognition.load_image_file", return_value=np.zeros((2, 2, 3)))
    def test_compare_returns_float_distance(
        self, _load_image_file, _face_encodings, _face_distance
    ):
        response = self.client.post(
            "/compare",
            data={
                "profile_photo": (self._file(), "profile.jpg"),
                "selfie": (self._file(), "selfie.jpg"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"distance": 0.42})

    @staticmethod
    def _file():
        import io

        return io.BytesIO(b"test-image")


if __name__ == "__main__":
    unittest.main()
