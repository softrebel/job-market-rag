from app.retrieval.text_normalizer import (
    TextNormalizer,
)


def test_normalize_arabic_characters():

    result = TextNormalizer.normalize("برنامه‌نویسی پایتون و كدنویسی")

    assert result == ("برنامه نویسی پایتون و کدنویسی")


def test_normalize_english():

    result = TextNormalizer.normalize("Senior Python Developer")

    assert result == ("senior python developer")


def test_tokenize():

    result = TextNormalizer.tokenize("Python Django Backend")

    assert result == {
        "python",
        "django",
        "backend",
    }
