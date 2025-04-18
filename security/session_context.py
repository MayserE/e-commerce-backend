import threading

_session_context = threading.local()


def set_current_user(user):
    _session_context.user = user


def get_current_user():
    return getattr(_session_context, 'user', None)


def clear_current_user():
    if hasattr(_session_context, 'user'):
        del _session_context.user
