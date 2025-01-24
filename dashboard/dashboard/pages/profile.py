"""The profile page."""

import dataclasses

import reflex as rx
from email_validator import EmailNotValidError, validate_email

from ..components.profile_input import profile_input
from ..templates import template


@dataclasses.dataclass
class Profile:
    name: str = ""
    email: str = ""
    notifications: bool = True

    def __post_init__(self):
        if self.email:
            validate_email(self.email)


class ProfileState(rx.State):
    profile: Profile = Profile(name="Admin", email="", notifications=True)
    error_msg: str = ""

    def handle_submit(self, form_data: dict):
        try:
            self.profile = Profile(**form_data)
        except EmailNotValidError as e:
            self.error_msg = str(e)
            return
        self.error_msg = ""
        return rx.toast.success("Profile updated successfully", position="top-center")

    def toggle_notifications(self):
        self.profile.notifications = not self.profile.notifications


@template(route="/profile", title="Profile")
def profile() -> rx.Component:
    """The profile page.

    Returns:
        The UI for the profile page.

    """
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("square-user-round"),
                    rx.heading("Personal information", size="5"),
                    align="center",
                ),
                rx.text("Update your personal information.", size="3"),
                width="100%",
            ),
            rx.form.root(
                rx.vstack(
                    profile_input(
                        "Name",
                        "name",
                        "Admin",
                        "text",
                        "user",
                        ProfileState.profile.name,
                    ),
                    profile_input(
                        "Email",
                        "email",
                        "user@reflex.dev",
                        "text",
                        "mail",
                        ProfileState.profile.email,
                        ProfileState.error_msg,
                    ),
                    rx.button("Update", type="submit", width="100%"),
                    width="100%",
                    spacing="5",
                ),
                on_submit=ProfileState.handle_submit,
                reset_on_submit=True,
                width="100%",
                max_width="325px",
            ),
            width="100%",
            spacing="4",
            flex_direction=["column", "column", "row"],
        ),
        rx.divider(),
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon("bell"),
                    rx.heading("Notifications", size="5"),
                    align="center",
                ),
                rx.text("Manage your notification settings.", size="3"),
            ),
            rx.checkbox(
                "Receive product updates",
                size="3",
                checked=ProfileState.profile.notifications,
                on_change=ProfileState.toggle_notifications(),
            ),
            width="100%",
            spacing="4",
            justify="between",
            flex_direction=["column", "column", "row"],
        ),
        spacing="6",
        width="100%",
        max_width="800px",
    )
