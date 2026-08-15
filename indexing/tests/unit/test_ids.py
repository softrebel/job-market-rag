from app.utils.ids import make_chunk_id


def test_chunk_id_is_deterministic():

    first = make_chunk_id(
        job_id="1",
        chunk_index=0,
        content_hash="abc",
    )

    second = make_chunk_id(
        job_id="1",
        chunk_index=0,
        content_hash="abc",
    )

    assert first == second


def test_different_chunks_have_different_ids():

    first = make_chunk_id(
        job_id="1",
        chunk_index=0,
        content_hash="abc",
    )

    second = make_chunk_id(
        job_id="1",
        chunk_index=1,
        content_hash="abc",
    )

    assert first != second


def test_changed_content_creates_new_id():

    first = make_chunk_id(
        job_id="1",
        chunk_index=0,
        content_hash="abc",
    )

    second = make_chunk_id(
        job_id="1",
        chunk_index=0,
        content_hash="xyz",
    )

    assert first != second
