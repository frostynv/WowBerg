import signal
import sys
import threading
from abc import ABC, abstractmethod
from wowberg.logger.service import LogService

class Dockerizable(ABC):
    """Marker class to indicate that a class can be used in a Docker container environment. This is used for type checking and to enforce that certain classes are designed with Docker compatibility in mind."""
    
    def __init__(self):
        """Initialize and register shutdown handlers for graceful Docker shutdown."""
        self.register_shutdown_handlers()
    
    def register_shutdown_handlers(self):
        """Register signal handlers for graceful shutdown.
        
        Signal handlers can only be registered from the main thread.
        This method safely registers SIGTERM and SIGINT handlers.
        """
        # Only register signal handlers if we're in the main thread
        if threading.current_thread() is threading.main_thread():
            try:
                # This catches Docker Compose Down (SIGTERM)
                signal.signal(signal.SIGTERM, self._handle_signal)
                # This catches Ctrl+C locally (SIGINT)
                signal.signal(signal.SIGINT, self._handle_signal)
            except Exception as e:
                LogService.log(
                    f"Failed to register signal handlers: {e}",
                    prefix=LogService.LoggingLevels.WARN
                )
        else:

            LogService.log(
                "Not registering signal handlers: not running in main thread",
                prefix=LogService.LoggingLevels.WARN
            )
    
    def _handle_signal(self, signum, frame):
        """Internal signal handler wrapper with error handling."""
        try:
            self._shutdown(signum, frame)
        except Exception as e:
            from wowberg.logger.service import LogService
            LogService.log(
                f"Error during shutdown: {e}",
                prefix=LogService.LoggingLevels.ERROR
            )
            sys.exit(1)
    
    @abstractmethod
    def _shutdown(self, signum, frame):
        pass
        
__all__ = ["Dockerizable"]
