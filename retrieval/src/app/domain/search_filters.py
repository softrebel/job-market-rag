from pydantic import BaseModel, Field


class SearchFilters(BaseModel):
    city: list[str] = Field(default_factory=list)
    source: list[str] = Field(default_factory=list)
    company: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)

    employment_type: list[str] = Field(default_factory=list)

    gender: list[str] = Field(default_factory=list)

    experience_min: int | None = None
    experience_max: int | None = None

    def merge(self, other: "SearchFilters") -> "SearchFilters":
        return SearchFilters(
            city=self.city + other.city,
            source=self.source + other.source,
            company=self.company + other.company,
            skills=self.skills + other.skills,
            categories=self.categories + other.categories,
            employment_type=(self.employment_type + other.employment_type),
            gender=self.gender + other.gender,
            experience_min=(
                other.experience_min
                if other.experience_min is not None
                else self.experience_min
            ),
            experience_max=(
                other.experience_max
                if other.experience_max is not None
                else self.experience_max
            ),
        )
