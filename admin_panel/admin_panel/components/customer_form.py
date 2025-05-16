import reflex as rx

from admin_panel.states.customer_state import CustomerState


def customer_edit_form() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h2(
                rx.cond(
                    CustomerState.form_customer_id == 0,
                    "Add New User",
                    "Edit User",
                ),
                class_name="text-lg sm:text-xl font-semibold mb-4 sm:mb-6 text-gray-800",
            ),
            rx.el.form(
                rx.el.input(
                    type="hidden",
                    name="customer_id",
                    default_value=CustomerState.form_customer_id.to_string(),
                    key=rx.cond(
                        CustomerState.form_customer_id == 0,
                        "customer_id-new-form",
                        CustomerState.form_customer_id.to_string() + "_cust_id_form",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "First Name:",
                        html_for="form_first_name_input",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        id="form_first_name_input",
                        name="first_name",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        placeholder="Enter first name",
                        default_value=CustomerState.form_first_name,
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_first_name-new-form",
                            CustomerState.form_customer_id.to_string() + "_fn_form",
                        ),
                    ),
                    class_name="mb-3 sm:mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Last Name:",
                        html_for="form_last_name_input",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        id="form_last_name_input",
                        name="last_name",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        placeholder="Enter last name",
                        default_value=CustomerState.form_last_name,
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_last_name-new-form",
                            CustomerState.form_customer_id.to_string() + "_ln_form",
                        ),
                    ),
                    class_name="mb-3 sm:mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email:",
                        html_for="form_email_input",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        id="form_email_input",
                        name="email",
                        type="email",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        placeholder="Enter email",
                        default_value=CustomerState.form_email,
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_email-new-form",
                            CustomerState.form_customer_id.to_string() + "_email_form",
                        ),
                    ),
                    class_name="mb-3 sm:mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Tag:",
                        html_for="form_tags_input",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        id="form_tags_input",
                        name="tags",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        placeholder="Enter a single tag",
                        default_value=CustomerState.form_tags,
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_tags-new-form",
                            CustomerState.form_customer_id.to_string() + "_tags_form",
                        ),
                    ),
                    class_name="mb-3 sm:mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Role:",
                        html_for="form_role_select",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.foreach(
                            CustomerState.available_roles,
                            lambda role: rx.el.option(role, value=role),
                        ),
                        id="form_role_select",
                        name="role",
                        value=CustomerState.form_role,
                        on_change=CustomerState.set_form_role,
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_role-new-form",
                            CustomerState.form_customer_id.to_string() + "_role_form",
                        ),
                    ),
                    class_name="mb-3 sm:mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Status:",
                        html_for="form_status_select",
                        class_name="block text-xs sm:text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.foreach(
                            CustomerState.customer_statuses,
                            lambda status: rx.el.option(status, value=status),
                        ),
                        id="form_status_select",
                        name="status",
                        value=CustomerState.form_status,
                        on_change=CustomerState.set_form_status,
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-xs sm:text-sm",
                        key=rx.cond(
                            CustomerState.form_customer_id == 0,
                            "form_status-new-form",
                            CustomerState.form_customer_id.to_string() + "_status_form",
                        ),
                    ),
                    class_name="mb-4 sm:mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=CustomerState.toggle_edit_dialog,
                        class_name="mr-2 sm:mr-3 px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                    ),
                    rx.el.button(
                        rx.cond(
                            CustomerState.form_customer_id == 0,
                            "Add User",
                            "Save Changes",
                        ),
                        type="submit",
                        class_name="px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                    ),
                    class_name="flex justify-end pt-1 sm:pt-2",
                ),
                on_submit=CustomerState.handle_edit_customer,
                reset_on_submit=False,
                class_name="space-y-3 sm:space-y-4",
            ),
            class_name="bg-white p-4 sm:p-6 rounded-lg shadow-xl w-full max-w-md mx-auto",
        ),
        open=CustomerState.show_edit_dialog,
        data_state=rx.cond(CustomerState.show_edit_dialog, "open", "closed"),
        class_name="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50 data-[state=open]:flex items-center justify-center p-2 sm:p-4 h-screen w-screen",
    )
