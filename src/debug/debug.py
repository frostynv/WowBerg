from __future__ import annotations

from collections.abc import Callable, Iterable
import string
from typing import Protocol, Union, runtime_checkable


@runtime_checkable
class _WritableStream(Protocol):
    def write(self, message: str) -> object:
        ...


StreamSink = Union[_WritableStream, Callable[[str], object]]


class Debug:
    """Debug utility class for broadcasting messages to multiple sinks."""

    _instance: Debug | None = None

    def __new__(cls, streams: Iterable[StreamSink] | None = None) -> Debug:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._streams = []
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, streams: Iterable[StreamSink] | None = None) -> None:
        if self._initialized:
            return

        self._streams = list(streams) if streams is not None else [print]
        self._initialized = True

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

    def log(self, message: str, prefix: str = "[DEBUG]") -> None:
        """Broadcast a formatted message to every configured sink."""
        formatted_message = f"{prefix} {message}"

        for stream in self._streams:
            if callable(stream) and not isinstance(stream, _WritableStream):
                stream(formatted_message)
                continue

            stream.write(f"{formatted_message}\n")
            flush = getattr(stream, "flush", None)
            if callable(flush):
                flush()

def create_debug(streams: Iterable[StreamSink] | None = None) -> Debug:
    """Factory for a configurable debug printer."""
    return Debug(streams=streams)


__all__ = ["Debug", "create_debug"]