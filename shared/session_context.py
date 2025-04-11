import threading


_session_context = threading.local()

def set_current_user(user):
    """Guarda el usuario actual en el contexto del hilo (request)."""
    _session_context.user = user

def get_current_user():
    """Obtiene el usuario actual desde el contexto del hilo."""
    return getattr(_session_context, 'user', None)

def clear_current_user():
    """Limpia el contexto del hilo después del request."""
    if hasattr(_session_context, 'user'):
        del _session_context.user