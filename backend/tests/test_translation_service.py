import unittest

from app.exceptions import TranslationException
from app.services.translation_service import build_translation_payload, extract_translated_text


class TranslationServiceHelpersTests(unittest.TestCase):
    def test_build_translation_payload_contains_expected_keys(self) -> None:
        payload = build_translation_payload("hello", "en", "ru")

        self.assertEqual(payload["sourceLanguageCode"], "en")
        self.assertEqual(payload["targetLanguageCode"], "ru")
        self.assertEqual(payload["texts"], ["hello"])
        self.assertIn("folderId", payload)

    def test_extract_translated_text_returns_first_translation(self) -> None:
        translated_text = extract_translated_text({"translations": [{"text": "Привет"}]})

        self.assertEqual(translated_text, "Привет")

    def test_extract_translated_text_raises_on_missing_translations(self) -> None:
        with self.assertRaises(TranslationException):
            extract_translated_text({})


if __name__ == "__main__":
    unittest.main()
