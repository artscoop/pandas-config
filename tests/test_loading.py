from pathlib import Path

from pytest import fixture
from pandas.configfile import load


@fixture
def ini_path() -> Path:
    """Returns the path to the INI file used for testing."""
    return Path(__file__).parent / "files"


def test_no_crash(ini_path: Path) -> None:
    """Test that loading a configuration file does not crash."""
    for file in ini_path.glob("*.ini"):
        assert load(file) is None
