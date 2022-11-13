from .admin import admin_required
from .auth import login_required

__all__ = (
    "admin_required",
    "login_required",
)
