import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.flow.types import Edge, Node

from .common import demo

initial_nodes: list[Node] = [
    {
        "id": "2",
        "type": "dragHandleNode",
        "dragHandle": ".drag-handle__custom",
        "position": {"x": 200, "y": 200},
    },
]

initial_edges: list[Edge] = []


@rx.memo
def drag_handle_node():
    return rx.fragment(
        rxe.flow.handle(
            type="target",
            position="left",
        ),
        rx.el.div(
            "Only draggable here → ",
            rx.el.span(class_name="drag-handle__custom"),
            class_name="drag-handle__label",
        ),
        rxe.flow.handle(
            type="source",
            position="right",
        ),
    )


@demo(
    route="/nodes/drag-handle",
    title="Drag Handle Demo",
    description="A demo of a node with a drag handle.",
)
def drag_handle():
    return rx.box(
        rxe.flow(
            rxe.flow.background(),
            default_nodes=initial_nodes,
            default_edges=initial_edges,
            node_types={"dragHandleNode": drag_handle_node},
            color_mode="light",
            fit_view=True,
        ),
        height="100vh",
        width="100vw",
    )
