from app.container import (
    get_embedder,
    get_qdrant_client,
)


def test_embedder_is_singleton():

    first = get_embedder()
    second = get_embedder()

    assert first is second


def test_qdrant_client_is_singleton():

    first = get_qdrant_client()
    second = get_qdrant_client()

    assert first is second
