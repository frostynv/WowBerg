"""Logger encapsulation using Python's logging module.

Supports external configuration for stream handling and multi-purpose logging.
Configuration is loaded from logging_config.yaml in the project root.
"""

from __future__ import annotations

import logging
import logging.config
import os
from pathlib import Path
from typing import ClassVar, Optional
import yaml


class LogService:
    """Thin encapsulation of Python's logger.
    
    Forwards logging calls to named logger instances.
    Configuration is loaded from an external YAML/JSON config file
    to support runtime stream and level adjustments.
    """

    _instance: ClassVar[LogService | None] = None
    _app_name: str = os.getenv("APP_CODE", "wowberg")
    
    class ErrorLevels:
        """Standard log level names matching Python logging levels."""
        TEST = "DEBUG"
        INFO = "INFO"
        WARN = "WARNING"
        CRITICAL = "CRITICAL"

    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize the logger with configuration from file.
        
        Args:
            config_path: Path to logging config file. If None, uses default
                        'logging_config.yaml' from project root.
        """
        if not hasattr(self, '_initialized'):
            self._root_logger = logging.getLogger("wowberg")
            # Defer config loading to avoid circular imports
            self._load_config(config_path or os.getenv("LOG_CONFIG_PATH", None))
            self._initialized = True
    
    @staticmethod
    def _load_config(config_path: str | None = None) -> None:
        """Load logging configuration from file.
        
        Args:
            config_path: Path to the config file (YAML or JSON). If None, 
                        defaults to 'logging_config.yaml' in project root.
        """
        _app_name = os.getenv("APP_CODE", "wowberg")
        
        if config_path is None:
            config_path = str(Path(__file__).parent.parent / "logging_config.yaml")
        
        config_file = Path(config_path)
        
        
        if not config_file.exists():
            # Fallback to basic configuration if file not found
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] {%(levelname)s} %(name)s: %(message)s",
            )
            return
        
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
            logging.config.dictConfig(config)
        except (ImportError, yaml.YAMLError) as e:
            # Fallback if pyyaml not available or YAML parsing fails
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] {%(levelname)s} %(name)s: %(message)s",
            )
    
    @staticmethod
    def _get_logging_level(level_name: str) -> int:
        """Convert level name to Python logging level.
        
        Args:
            level_name: Level name (DEBUG, INFO, WARNING, CRITICAL).
        
        Returns:
            Python logging level integer.
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "CRITICAL": logging.CRITICAL,
            "TEST": logging.DEBUG,
        }
        return level_map.get(level_name.upper(), logging.INFO)

    def get_logger(self, name: str) -> logging.Logger:
        """Get a child logger for a specific purpose.
        
        Args:
            name: Logger name (e.g., 'auction', 'blizzard'). Will be prefixed
                 with 'wowberg.'.
        
        Returns:
            A named logger instance configured via config file.
            Note: Logger instances are cached by Python's logging module.
        """
        return logging.getLogger(f"wowberg.{name}")

    @classmethod
    def log(cls, message: str, prefix: str = "INFO", handler: Optional[str] = None, args: Optional[dict] = None) -> None:
        """Log a message at the specified level to the specified logger.
        
        Ensures the singleton LogService is initialized before logging.
        
        Args:
            message: The log message.
            prefix: Log level name (INFO, WARNING, etc.). Defaults to INFO.
            handler: Logger suffix (e.g., '', 'auction', 'blizzard'). 
                    Empty string defaults to root 'wowberg' logger.
            args: Additional arguments to include in the log message.
        """
        # Ensure singleton is initialized
        instance = cls()
        
        level = cls._get_logging_level(prefix)
        logger_key = f"{cls._app_name}.{handler}" if handler else cls._app_name
        target_logger = logging.getLogger(logger_key)
        target_logger.log(level, message)

    def debug(self, message: str) -> None:
        """Log a debug-level message to the root logger."""
        self._root_logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info-level message to the root logger."""
        self._root_logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning-level message to the root logger."""
        self._root_logger.warning(message)

    def critical(self, message: str) -> None:
        """Log a critical-level message to the root logger."""
        self._root_logger.critical(message)


__all__ = ["LogService"]
