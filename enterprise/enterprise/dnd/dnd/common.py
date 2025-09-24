"""Common components used by all demo pages."""

from ...demo import demo_builder

demo, DemoState = demo_builder(
    demo_prefix="/dnd",
    demo_title="Drag and Drop demo",
)
