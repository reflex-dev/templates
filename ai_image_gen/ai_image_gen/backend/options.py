import reflex as rx
import random
from ..components.prompt_list import prompt_list
from ..components.styles_preset import styles_preset


class OptionsState(rx.State):
    dimensions: list[tuple[int, int]] = [
        (1728, 576),
        (1664, 576),
        (1600, 640),
        (1536, 640),
        (1472, 704),
        (1408, 704),
        (1344, 704),
        (1344, 768),
        (1280, 768),
        (1216, 832),
        (1152, 832),
        (1152, 896),
        (1088, 896),
        (1088, 960),
        (1024, 960),
        (1024, 1024),
        (960, 1024),
        (960, 1088),
        (896, 1088),
        (896, 1152),
        (832, 1152),
        (832, 1216),
        (768, 1280),
        (768, 1344),
        (704, 1344),
        (704, 1408),
        (704, 1472),
        (640, 1536),
        (640, 1600),
        (576, 1664),
        (576, 1728),
    ]
    slider_tick: int = len(dimensions) // 2
    selected_dimensions: tuple[int, int] = dimensions[slider_tick]
    hover: bool = False
    styles_preset: dict[str, dict[str, str]] = styles_preset
    selected_style: str = "Cinematic"
    advanced_options_open: bool = False
    # Generation options
    prompt: str = ""
    negative_prompt: str = (
        "deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, text, watermark, signature"
    )
    num_outputs: int = 1
    seed: int = 0
    steps: int = 4
    scheduler: str = "K_EULER"
    guidance_scale: float = 0

    def set_tick(self, value: int):
        self.slider_tick = value[0]
        self.selected_dimensions = self.dimensions[self.slider_tick]

    def set_hover(self, value: bool):
        self.hover = value

    def set_num_outputs(self, value: int):
        self.num_outputs = value[0]

    def set_steps(self, value: int):
        self.steps = value[0]

    def set_guidance_scale(self, value: float):
        self.guidance_scale = value[0]

    def randomize_prompt(self):
        self.prompt = random.choice(prompt_list)

    @rx.var
    def selected_style_prompt(self) -> str:
        if self.selected_style == "":
            return ""
        return self.styles_preset[self.selected_style]["prompt"]

    @rx.var
    def dimensions_str(self) -> str:
        width, height = self.selected_dimensions
        return f"{width} × {height}"
