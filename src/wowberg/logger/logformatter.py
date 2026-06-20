
import logging

class ConsoleFormatter(logging.Formatter):
    """Custom formatter for console logs with color coding based on log level."""

    COLOR_CODES = {
        logging.DEBUG: "\033[94m",      # Blue
        logging.INFO: "\033[92m",       # Green
        logging.WARNING: "\033[93m",    # Yellow
        logging.ERROR: "\033[91m",      # Red
        logging.CRITICAL: "\033[95m",   # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with color based on level."""
        color = self.COLOR_CODES.get(record.levelno, self.RESET)
        args_str = self._format_args(record.args) if record.args else ""
        suffix = f" | {args_str}" if args_str else ""
        return f"{color}[{record.asctime}] [{record.name} - {record.levelname}] : {record.message}{suffix}{self.RESET}"

    @staticmethod
    def _format_args(args: dict) -> str:
        """Format args dictionary into pipe-separated string."""
        if not args:
            return ""
        return " | ".join(f"{k}: {v}" for k, v in args.items())

__all__ = ["ConsoleFormatter"]