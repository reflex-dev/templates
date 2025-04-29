import reflex as rx

from admin_dashboard.states.navigation_state import NavigationState


def navigation_item(text: str, href: str) -> rx.Component:
    """Creates a styled navigation link."""
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            NavigationState.current_page == href,
            "px-4 py-2 text-sm font-medium text-white bg-emerald-700 rounded-md shadow-sm whitespace-nowrap sm:whitespace-normal",
            "px-4 py-2 text-sm font-medium text-emerald-100 hover:bg-emerald-600 hover:text-white rounded-md transition-colors duration-150 ease-in-out whitespace-nowrap sm:whitespace-normal",
        ),
    )


def navigation() -> rx.Component:
    """The top navigation bar component."""
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src="https://avatars.githubusercontent.com/u/104714959?s=200&v=4",
                class_name="h-8 w-auto mr-4 max-md:hidden",
                alt="App Logo",
            ),
            navigation_item("Sales Pipeline", "/sales-pipeline"),
            navigation_item("Customer Admin Panel", "/"),
            navigation_item("HR Portal", "/hr-portal"),
            navigation_item(
                "Customer Success Hub",
                "/customer-success-hub",
            ),
            class_name="flex items-center space-x-2 overflow-x-auto w-full",
        ),
        class_name="bg-emerald-800 px-6 py-2 shadow-md sticky top-0 left-0 w-full z-50 h-[56px]",
    )
