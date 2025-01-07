import reflex as rx

sidebar_width = ["100%", "100%", "100%", "375px", "450px"]
border = f"1.5px solid {rx.color('gray', 5, True)}"
content_max_width = "1280px"
sidebar_bg = rx.color("gray", 2)
content_bg_color = rx.color("gray", 1)

image_style = {
    "decoding": "auto",
    "loading": "eager",
    "vertical_align": "middle",
    "object_fit": "contain",
    "width": "auto",
}

image_height = ["400px", "500px", "650px", "850px"]

image_props = {
    "style": image_style,
    "width": "100%",
    "height": image_height,
}

button_props = {
    "size": "2",
    "cursor": "pointer",
    "variant": "outline",
}

box_shadow = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto+Flex:wght@400;500;600;700;800&display=swap",
    "react-zoom.css",
]

base_style = {
    "font_family": "Roboto Flex",
    rx.icon: {
        "stroke_width": "1.75px",
    },
}
