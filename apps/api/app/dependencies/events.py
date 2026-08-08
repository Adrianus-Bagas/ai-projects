from app.events.bus import EventBus


def get_event_bus() -> EventBus:
    return EventBus()