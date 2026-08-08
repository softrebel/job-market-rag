import re
# from hazm import Normalizer

# _normalizer = Normalizer()


def clean_text(raw_text: str) -> str:
    # text = _normalizer.normalize(raw_text)
    text = raw_text.replace("ي", "ی")
    text = text.replace("ى", "ی")
    text = text.replace("ك", "ک")

    text = re.sub(r"\s+", " ", text)

    return text.strip()
