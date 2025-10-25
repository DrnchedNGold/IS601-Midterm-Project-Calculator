# Calculator Config

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

# Load any settings from a .env file if one exists
# This lets us configure the calculator without changing code
load_dotenv()


def get_project_root() -> Path:
    """
    Figures out where the project's root directory is.

    This function walks up the directory tree from this file's location to find
    the project root. We need this to set up default paths for logs and history.

    Returns:
        Path: The project's root directory
    """
    # Start with where this file is located
    current_file = Path(__file__)
    # Go up two levels (from app/calculator_config.py to the project root)
    return current_file.parent.parent


@dataclass
class CalculatorConfig:
    """
    Manages all the calculator's configuration settings.

    Using a config class like this keeps all settings in one place and makes it
    easy to change behavior without modifying the core calculator code.
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    ):
        """
        Sets up the configuration with sensible defaults and environment variables.

        Each parameter can be set three ways (in order of priority):
        1. Passed directly to this constructor
        2. Set via an environment variable
        3. Use the built-in default

        Args:
            base_dir: Where to store calculator files (defaults to project root)
            max_history_size: How many calculations to keep in history (default 1000)
            auto_save: Whether to automatically save history (default True)
            precision: How many decimal places to use (default 10)
            max_input_value: Largest number we'll accept (default 1e999)
            default_encoding: Text encoding for files (default utf-8)
        """
        # Figure out where the project is located
        project_root = get_project_root()
        # Set base directory - use what's passed in, then check environment, finally default to project root
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        # How many history entries we'll keep before deleting old ones
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )

        # Whether to automatically save history after each calculation
        # Environment variable can be 'true', 'false', '1', or '0'
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        # How many decimal places to show in results
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        # Maximum size for input numbers to prevent overflow issues
        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        # Text encoding for reading/writing files
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        """
        Returns:
            Path: Directory for log files
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        """
        Returns:
            Path: Directory for history files
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """
        Returns:
            Path: Full path to the history file
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()

    @property
    def log_file(self) -> Path:
        """
        Returns:
            Path: Full path to the log file
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
        """
        Checks that all configuration values make sense.

        Raises:
            ConfigurationError: If any setting has an invalid value
        """
        # Make sure history size is a positive number
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        
        # Make sure precision is a positive number
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        
        # Make sure max input value is positive
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")