from poetrify.api import generate_init_cmd


def test_it():
    cmd = generate_init_cmd("Pipfile")
    assert cmd is None
