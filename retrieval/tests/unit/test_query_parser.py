from app.query.parser import QueryParser


def test_parse_city():

    parser = QueryParser()

    result = parser.parse("Senior Python Developer در تهران")

    assert result.semantic_query == ("Senior Python Developer")

    assert result.filters.city == ["تهران"]


def test_parse_experience():

    parser = QueryParser()

    result = parser.parse("Python Developer با حداقل 3 سال سابقه")

    assert result.filters.experience_min == 3


def test_parse_city_and_experience():

    parser = QueryParser()

    result = parser.parse("Senior Python Developer در تهران با حداقل 3 سال سابقه")

    assert result.semantic_query == ("Senior Python Developer")

    assert result.filters.city == ["تهران"]

    assert result.filters.experience_min == 3
