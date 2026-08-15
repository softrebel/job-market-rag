from app.retrieval.text_normalizer import TextNormalizer


class SkillNormalizer:
    ALIASES: dict[str, str] = {
        # Python
        "python": "python",
        "python3": "python",
        "python 3": "python",
        "پایتون": "python",
        # Django
        "django": "django",
        "جنگو": "django",
        # PostgreSQL
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "postgre": "postgresql",
        # JavaScript
        "javascript": "javascript",
        "js": "javascript",
        "جاوااسکریپت": "javascript",
        # TypeScript
        "typescript": "typescript",
        "ts": "typescript",
        # React
        "react": "react",
        "reactjs": "react",
        # FastAPI
        "fastapi": "fastapi",
        "fast api": "fastapi",
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        normalized = TextNormalizer.normalize(skill)

        return cls.ALIASES.get(
            normalized,
            normalized,
        )

    @classmethod
    def normalize_many(
        cls,
        skills: list[str],
    ) -> set[str]:

        return {cls.normalize(skill) for skill in skills if skill.strip()}
