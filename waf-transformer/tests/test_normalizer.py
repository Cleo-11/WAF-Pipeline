from normalization.normalizer import normalize_text


def test_normalize_text_replaces_dynamic_tokens() -> None:
    text = (
        "user=123 email=alice@example.com ip=192.168.1.10 "
        "uuid=550e8400-e29b-41d4-a716-446655440000"
    )
    out = normalize_text(text)

    assert "<INT>" in out
    assert "<EMAIL>" in out
    assert "<IP>" in out
    assert "<UUID>" in out
