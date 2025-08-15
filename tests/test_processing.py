from app.services.processing import mask_banned_words, compute_metadata

def test_mask_banned_words():
    text, found = mask_banned_words("hola foo bar baz", ["foo", "bar"])
    assert found is True
    assert "foo" not in text and "bar" not in text
    assert set(text.split()) != set("hola foo bar baz".split())

def test_compute_metadata():
    wc, cc, ts = compute_metadata("hola mundo")
    assert wc == 2
    assert cc == len("hola mundo")
    assert ts is not None
