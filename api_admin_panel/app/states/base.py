import reflex as rx


class BaseState(rx.State):

    query_component_toggle: str = "none"

    def toggle_query(self):
        self.query_component_toggle = (
            "flex" if self.query_component_toggle == "none" else "none"
        )
