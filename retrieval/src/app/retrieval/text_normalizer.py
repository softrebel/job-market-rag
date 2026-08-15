import re


class TextNormalizer:

    _ARABIC_CHARS = str.maketrans(
        {
            "ي": "ی",
            "ى": "ی",
            "ك": "ک",
            "ة": "ه",
            "ۀ": "ه",
        }
    )

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""

        text = text.translate(cls._ARABIC_CHARS)

        # Normalize نیم‌فاصله
        text = text.replace("\u200c", " ")

        # Remove punctuation
        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
            flags=re.UNICODE,
        )

        # Normalize whitespace
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip().lower()

    @classmethod
    def tokenize(cls, text: str) -> set[str]:
        normalized = cls.normalize(text)

        if not normalized:
            return set()

        return set(normalized.split())
