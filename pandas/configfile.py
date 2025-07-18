from ast import literal_eval
from configparser import ConfigParser
from os import PathLike
from pathlib import Path

import pandas as pd

DEFAULT_FILE: str = ".pandas.ini"  # Default file name to look for


def load(path: PathLike | str = None, encoding: str = "utf-8"):
    """
    Load pandas configuration from an INI file and set pandas options accordingly.

    This function reads a configuration file in INI format and sets pandas options
    based on the sections and values defined in the file. If no path is provided,
    it looks for a '.pandas.ini' file in the current directory.

    See Also:
        [Pandas documentation](https://pandas.pydata.org/docs/reference/api/pandas.describe_option.html#pandas-describe-option) for more details

    Args:
        path (PathLike, str, optional): Path to the configuration file. Defaults to None,
            which will use '.pandas.ini' in the current directory.
        encoding (str, optional): The encoding to use when reading the configuration
            file. Defaults to "utf-8".

    Example:
        A configuration file might look like the following:

        ```ini
        [display]
        ; Maximum number of columns to be printed in a DataFrame
        width = 200

        ; What to display if the DataFrame is too large. "truncate" or "info"
        large_repr = "info"
        ; Maximum number of characters to be printed in a column
        max_colwidth = 25
        ; Minimum number of rows to be printed
        min_rows = 20
        ; Maximum number of rows to be printed
        max_rows = 200
        ; Default precision for floating point output
        precision = 3

        [display.html]
        border = 4
        ```

        Usages of the function may look like the following:

        >>> load()  # Loads from default .pandas.ini
        >>> load("custom_config.ini")  # Loads from specified file
        >>> load(encoding="latin-1")  # Loads with specific encoding

    Note:
        The values in the configuration file must be valid Python literals
        that can be evaluated using ast.literal_eval().
        Options that are not valid for pandas will be ignored.
    """
    final_path = path or DEFAULT_FILE
    config = ConfigParser()
    files = config.read(final_path, encoding=encoding)
    if not files:
        print(f"No configuration file found at {final_path}. (at {Path.cwd()})")
    for section in config.sections():
        for option in config.options(section):
            # Convert from string to Python type
            try:
                evaluation = literal_eval(config.get(section, option))
                pd.set_option(f"{section}.{option}", evaluation)
            except pd.errors.OptionError:
                print(f"Invalid option. Skipping {section}.{option}={evaluation}")
            except ValueError:
                print(f"Invalid literal value. Skipping {section}.{option}={evaluation}")
