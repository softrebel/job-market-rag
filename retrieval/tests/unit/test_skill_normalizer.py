from app.retrieval.skill_normalizer import (
    SkillNormalizer,
)


def test_python_aliases():

    assert SkillNormalizer.normalize("Python") == "python"

    assert SkillNormalizer.normalize("PYTHON") == "python"

    assert SkillNormalizer.normalize("Python3") == "python"

    assert SkillNormalizer.normalize("پایتون") == "python"


def test_postgresql_aliases():

    assert SkillNormalizer.normalize("Postgres") == "postgresql"

    assert SkillNormalizer.normalize("PostgreSQL") == "postgresql"


def test_javascript_aliases():

    assert SkillNormalizer.normalize("JS") == "javascript"

    assert SkillNormalizer.normalize("JavaScript") == "javascript"


def test_normalize_many():

    result = SkillNormalizer.normalize_many(
        [
            "Python",
            "PYTHON",
            "Python3",
            "Django",
        ]
    )

    assert result == {
        "python",
        "django",
    }
