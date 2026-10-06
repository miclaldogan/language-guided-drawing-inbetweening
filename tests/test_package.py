"""Verify that the src-layout package is installed in the test environment."""

from importlib.metadata import version
from importlib.util import find_spec


def test_installed_package_is_discoverable():
    assert find_spec("language_guided_drawing_inbetweening") is not None
    assert version("language-guided-drawing-inbetweening")
