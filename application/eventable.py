from typing import Callable, Any, Dict, List


class Eventable:
    """Base class that allows registering and firing events."""

    def __init__(self):
        self._event_listeners: Dict[str, List[Callable]] = {}

    def register_event(self, event_name: str, callback: Callable) -> None:
        """Register a callback for an event.

        Args:
            event_name: The name of the event to listen for
            callback: The function to call when the event fires
        """
        if event_name not in self._event_listeners:
            self._event_listeners[event_name] = []
        self._event_listeners[event_name].append(callback)

    def unregister_event(self, event_name: str, callback: Callable) -> None:
        """Unregister a callback from an event.

        Args:
            event_name: The name of the event
            callback: The callback to remove
        """
        if event_name in self._event_listeners:
            try:
                self._event_listeners[event_name].remove(callback)
            except ValueError:
                pass

    def fire_event(self, event_name: str, *args, **kwargs) -> None:
        """Fire an event, calling all registered callbacks.

        Args:
            event_name: The name of the event to fire
            *args: Positional arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
        """
        if event_name in self._event_listeners:
            for callback in self._event_listeners[event_name]:
                callback(*args, **kwargs)

    def get_event_listeners(self, event_name: str) -> List[Callable]:
        """Get all callbacks registered for an event.

        Args:
            event_name: The name of the event

        Returns:
            List of callbacks registered for the event
        """
        return self._event_listeners.get(event_name, [])
