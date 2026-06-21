
import logging
from datetime import datetime
import zoneinfo

class ConsoleFormatter(logging.Formatter):
    """Custom formatter for console logs with color coding based on log level."""

    COLOR_CODES = {
        logging.DEBUG: "\033[94m",      # Blue
        logging.INFO: "\033[38;5;28m",  # Green
        logging.WARNING: "\033[93m",    # Yellow
        logging.ERROR: "\033[91m",      # Red
        logging.CRITICAL: "\033[95m",   # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with color based on level."""
        color = self.COLOR_CODES.get(record.levelno, self.RESET)
        asctime = self.formatTime(record, self.datefmt)
        sub = getattr(record, "sub", None)
        if sub:
            args_str = self._format_args(sub)
            sub = f"\n\t| {args_str}"
        else:
            sub = ""
        return f"[{datetime.strptime(asctime, '%Y-%m-%d %H:%M:%S').astimezone(zoneinfo.ZoneInfo('America/New_York'))}] {color}[{record.name}]{self.RESET} : {record.msg}{sub}{self.RESET}"

    @staticmethod
    def _format_args(args: dict) -> str:
        """Format args dictionary into pipe-separated string."""
        if not args:
            return ""
        return "\n\t| ".join(f"{k}: {v}" for k, v in args.items())

__all__ = ["ConsoleFormatter"]