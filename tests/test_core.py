from poetrify.core import generate_init_cmd


def test_it():
    cmd = generate_init_cmd()
    assert cmd is None