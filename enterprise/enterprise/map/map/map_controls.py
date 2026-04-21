"""Map demo showcasing different map controls."""

import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng

from .common import demo


class ControlsState(rx.State):
    """State class for the map controls demo."""

    pass


@demo(
    route="/map-controls",
    title="Map Controls",
    description="Demonstrates different map controls including zoom, scale, attribution, and layers.",
)
def map_controls() -> rx.Component:
    # Create coordinates for map center
    london = latlng(lat=51.505, lng=-0.09)
    map_id = "map-controls-demo"

    return rx.vstack(
        rx.heading("Map Controls Demo"),
        rx.text("This map demonstrates different controls available in Leaflet."),
        rxe.map(
            # Basic tile layer
            rxe.map.tile_layer(
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            ),
            # Add ZoomControl
            rxe.map.zoom_control(
                position="topright",
            ),
            # # Add ScaleControl
            rxe.map.scale_control(
                position="bottomleft",
            ),
            # # Add AttributionControl
            rxe.map.attribution_control(
                position="topleft",
            ),
            # Map settings
            id=map_id,
            zoom=13,
            center=london,
            zoom_control=False,  # Disable default zoom control
            attribution_control=False,  # Disable default attribution control
            width="100%",
            height="50vh",
        ),
        rx.vstack(
            rx.text("Available Controls:"),
            rx.unordered_list(
                rx.list_item("Zoom Control - Located at topright (default is topleft)"),
                rx.list_item("Scale Control - Located at bottom-left (default is off)"),
                rx.list_item(
                    "Attribution Control - Located at topleft (default is bottom-right)"
                ),
            ),
            align_items="flex-start",
            spacing="2",
            width="100%",
        ),
        width="100%",
        padding="1em",
    )
