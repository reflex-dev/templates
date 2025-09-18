import reflex as rx

from . import add_nodes_on_edge_drop
from . import connection_limit
from . import custom_node
from . import drag_handle
from . import intersections
from . import overview

flow_pages = [
    {
        "title": "Add Node on Edge Drop Demo",
        "route": "/flow/nodes/add-node-on-edge-drop",
    },
    {"title": "Connection Limit Demo", "route": "/flow/nodes/connection-limit"},
    {"title": "Custom Node Demo", "route": "/flow/nodes/custom-node"},
    {"title": "Drag Handle Demo", "route": "/flow/nodes/drag-handle"},
    {"title": "Intersections", "route": "/flow/nodes/intersections"},
    {"title": "Feature Overview", "route": "/flow/overview"},
]


@rx.page(route="/flow", title="Flow Demo")
def index():
    return rx.flex(
        rx.foreach(
            flow_pages,
            lambda page: rx.card(
                rx.vstack(
                    rx.link(page["title"], href=page["route"]),
                ),
                width="300px",
            ),
        ),
        wrap="wrap",
        spacing="3",
    )
