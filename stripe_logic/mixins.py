"""Contain project mixins."""
from django.views.generic.base import ContextMixin


class TitleMixin(ContextMixin):
    """Mixin for title displaying."""

    title = ''

    def get_context_data(self, **kwargs):
        """Update context with page title."""
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
