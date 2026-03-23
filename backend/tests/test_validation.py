import unittest

from app.exceptions import ValidationException
from app.utils.file_validation import validate_image_size
from app.utils.language import validate_language_pair


class ValidationHelpersTests(unittest.TestCase):
    def test_validate_language_pair_normalizes_languages(self) -> None:
        source_language, target_language = validate_language_pair(" RU ", "en")

        self.assertEqual(source_language, "ru")
        self.assertEqual(target_language, "en")

    def test_validate_language_pair_rejects_equal_languages(self) -> None:
        with self.assertRaises(ValidationException):
            validate_language_pair("ru", "ru")

    def test_validate_language_pair_rejects_unsupported_language(self) -> None:
        with self.assertRaises(ValidationException):
            validate_language_pair("de", "en")

    def test_validate_image_size_accepts_small_payload(self) -> None:
        validate_image_size(b"12345", max_size_mb=1)

    def test_validate_image_size_rejects_large_payload(self) -> None:
        with self.assertRaises(ValidationException):
            validate_image_size(b"x" * (1024 * 1024 + 1), max_size_mb=1)


if __name__ == "__main__":
    unittest.main()
