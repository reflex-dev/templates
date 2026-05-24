"""Common components used by all flow demo pages."""

from ...demo import demo_builder

demo, DemoState = demo_builder(
    demo_prefix="/flow",
    demo_title="Flow Demo",
)
