import platform


def test_pytest():
    version = platform.python_version_tuple()
    assert version[0] == '3' and int(version[1]) >= 6
