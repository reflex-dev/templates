import reflex as rx

# These imports are needed to register the demo pages.
from .add_nodes_on_edge_drop import add_node_on_edge_drop
from .common import DemoState, demo
from .connection_limit import connection_limit
from .custom_node import custom_node
from .drag_handle import drag_handle
from .intersections import intersections
from .overview import overview

__all__ = [
    "add_node_on_edge_drop",
    "connection_limit",
    "custom_node",
    "drag_handle",
    "intersections",
    "overview",
]


@demo(
    route="/",
    title="Flow Demo",
    description="A collection of examples using React Flow in Reflex.",
)
def index():
    return rx.flex(
        rx.foreach(
            DemoState.pages,
            lambda page: rx.card(
                rx.vstack(
                    rx.link(page.title, href=page.route),
                    rx.text(page.description),
                ),
                width="300px",
            ),
        ),
        wrap="wrap",
        spacing="3",
    )
