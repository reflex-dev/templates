"""Common components used by all map demo pages."""

from ...demo import demo_builder

demo, DemoState = demo_builder(
    demo_prefix="/map",
    demo_title="Map Demos",
)
