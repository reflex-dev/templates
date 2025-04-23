import reflex as rx


class NavigationState(rx.State):
    """State for managing navigation."""

    @rx.var
    def current_page(self) -> str:
        """Get the current page route."""
        return self.router.page.path
