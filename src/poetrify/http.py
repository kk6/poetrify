import requests


def fetch_package_json(package_name):
    """
    Fetch package json from PyPI API
    :param str package_name: Package name
    :return: Dict of package's JSON
    :rtype: dict

    """
    r = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    r.raise_for_status()
    return r.json()
