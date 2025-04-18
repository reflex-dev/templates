import reflex as rx


def section_wrapper(title: str, *children, **props) -> rx.Component:
    """A styled container for dashboard sections."""
    return rx.el.div(
        rx.el.h2(
            title,
            class_name="text-xs uppercase text-cyan-500 tracking-wider font-semibold mb-3",
        ),
        rx.el.div(*children),
        class_name="bg-gradient-to-br from-blue-900/30 to-black/30 p-4 rounded-lg border border-blue-800/50 shadow-lg",
        **props,
    )
