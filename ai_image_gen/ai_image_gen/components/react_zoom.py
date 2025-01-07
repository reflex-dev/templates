"""Reflex custom component ImageZoom."""

# Imported from https://github.com/picklelo/reflex-image-zoom

import reflex as rx


class ImageZoom(rx.Component):
    """ImageZoom component."""

    # The React library to wrap.
    library = "react-medium-image-zoom"

    # The React component tag.
    tag = "Zoom"

    # If the tag is the default export from the module, you must set is_default = True.
    # This is normally used when components don't have curly braces around them when importing.
    is_default = True


image_zoom = ImageZoom.create
