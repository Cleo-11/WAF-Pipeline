from parsing.log_parser import parse_access_log_line


def test_parse_access_log_line_apache_style() -> None:
    line = (
        '127.0.0.1 - - [12/Mar/2026:08:41:22 +0000] '
        '"GET /api/users/123?email=test@example.com HTTP/1.1" 200 512 "-" "curl/8.6.0"'
    )
    entry = parse_access_log_line(line)

    assert entry is not None
    assert entry.method == "GET"
    assert entry.path.startswith("/api/users/123")
    assert entry.status == 200
