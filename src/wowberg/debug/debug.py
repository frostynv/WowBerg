from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import ClassVar, Protocol, Union, runtime_checkable


@runtime_checkable
class _WritableStream(Protocol):
    def write(self, message: str) -> object:
        ...


StreamSink = Union[_WritableStream, Callable[[str], object]]


class DebugInterface:
    """Concrete base that provides one shared Debugger instance across subclasses."""

    _debugger: ClassVar[Debugger | None] = None
    
    class ErrorLevels:
        TEST = "[TEST]"
        INFO = "[INFO]"
        WARN = "[WARNING]"
        CRITICAL = "[ERROR]"

    @property
    def debugger(self) -> Debugger:
        """Return the shared Debugger instance available to this class."""
        return self._create_debug()

    @classmethod
    def _create_debug(cls, streams: Iterable[StreamSink] | None = None) -> Debugger:
        """Create or return the shared Debug instance for all DebugAvailable classes."""
        if cls._debugger is None:
            cls._debugger = Debugger(streams=streams)
            return cls._debugger

        if streams is not None:
            cls._debugger.set_streams(streams)
        return cls._debugger


class Debugger:
    """Debugger utility class for broadcasting messages to multiple sinks."""

    def __init__(self, streams: Iterable[StreamSink] | None = None) -> None:
        # Initialize with default to standard print if no streams
        self._streams = list(streams) if streams is not None else [print]


    def log(self, message: str, prefix: str = "[DEBUG]") -> None:
        """Broadcast a formatted medossage to every configured sink."""
        # Format the message with the prefix
        formatted_message = f"{prefix} {message}"
        
        # Write the formatted message to each stream
        for stream in self._streams:
            if callable(stream) and not isinstance(stream, _WritableStream):
                stream(formatted_message)
                continue
            stream.write(f"{formatted_message}\n")
            flush = getattr(stream, "flush", None)
            if callable(flush):
                flush()

    ## Stream management methods

    def set_streams(self, streams: Iterable[StreamSink]) -> None:
        """Replace output sinks for this debug instance."""
        self._streams = list(streams)

    @property
    def streams(self) -> list[StreamSink]:
        """Return the current list of output sinks."""
        return self._streams
    
    def add_stream(self, stream: StreamSink) -> None:
        """Register an additional sink for future messages."""
        self._streams.append(stream)

    def remove_stream(self, stream: StreamSink) -> None:
        """Remove a sink if it is currently registered."""
        self._streams.remove(stream)

    def clear_streams(self) -> None:
        """Remove all sinks."""
        self._streams.clear()

__all__ = ["DebugInterface"]