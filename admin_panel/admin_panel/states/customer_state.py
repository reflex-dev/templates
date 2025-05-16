import datetime
import math
import random
from typing import List, Set, TypedDict
from typing import Optional as TypingOptional

import pandas as pd
import reflex as rx


class CustomerData(TypedDict):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone: TypingOptional[str]
    status: str
    avatar_url: str
    role: str
    tags: List[str]
    created_at: str
    updated_at: str
    selected: bool


class CustomerState(rx.State):
    _all_customers_data: List[CustomerData] = []
    loading: bool = False
    error_message: str = ""
    show_edit_dialog: bool = False
    form_customer_id: int = 0
    form_first_name: str = ""
    form_last_name: str = ""
    form_email: str = ""
    form_status: str = "Active"
    form_tags: str = ""
    form_role: str = ""
    customer_statuses: List[str] = [
        "Active",
        "Onboarding",
        "Inactive",
        "Pending",
        "Suspended",
    ]
    all_selected: bool = False
    available_roles: List[str] = [
        "Administrator",
        "Accounting",
        "Product Designer",
        "Human Resources",
        "Devops",
        "Hiring Manager",
        "Customer Success",
    ]
    available_tags: List[str] = [
        "Collaboration",
        "Leadership",
        "Innovation",
        "Creativity",
        "Feedback",
        "Coaching",
        "Mentoring",
        "Delegation",
    ]
    sort_column: str = "name"
    sort_order: str = "asc"
    current_page: int = 1
    items_per_page: int = 10
    total_db_customers: int = 0
    _target_customer_email_for_tags: str | None = None
    _target_customer_tag_str: str | None = None
    _target_customer_role: str | None = None
    _next_customer_id: int = 1
    search_query: str = ""

    @rx.var
    def total_users(self) -> int:
        return len(self._processed_customers)

    @rx.var
    def total_pages(self) -> int:
        num_items = len(self._processed_customers)
        if (
            self.items_per_page <= 0
        ):  # Guard against division by zero or invalid items_per_page
            return 0
        if num_items == 0:
            return 0
        return math.ceil(num_items / self.items_per_page)

    @rx.var
    def _processed_customers(self) -> List[CustomerData]:
        data_to_process = list(
            self._all_customers_data
        )  # Make a copy to avoid modifying the original list if needed elsewhere

        # Apply search filter
        if self.search_query and self.search_query.strip():
            query_lower = self.search_query.lower().strip()
            data_to_process = [
                c
                for c in data_to_process
                if query_lower
                in f"{c.get('first_name', '')} {c.get('last_name', '')}".lower()
            ]

        # Apply sorting
        def get_sort_value(customer_data_item: CustomerData):
            if self.sort_column == "name":
                first = customer_data_item.get("first_name", "")
                last = customer_data_item.get("last_name", "")
                return (first.lower(), last.lower())

            sort_val = customer_data_item.get(self.sort_column)
            if isinstance(sort_val, str):
                return sort_val.lower()
            return sort_val

        sorted_data = sorted(
            data_to_process,
            key=get_sort_value,
            reverse=self.sort_order == "desc",
        )
        return sorted_data

    @rx.var
    def customers(self) -> List[CustomerData]:
        data_for_page = self._processed_customers
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return data_for_page[start_index:end_index]

    def _parse_tags_string(self, tags_str: str | None) -> List[str]:
        if not tags_str:
            return []
        tag_names_from_input = [
            name.strip() for name in tags_str.split(",") if name.strip()
        ]
        unique_tags: List[str] = []
        seen_tags: Set[str] = set()
        for tag in tag_names_from_input:
            if tag not in seen_tags:
                unique_tags.append(tag)
                seen_tags.add(tag)
        return unique_tags

    def _format_tags_list_to_string(self, tags_list: List[str]) -> str:
        return ", ".join(tags_list)

    @rx.event
    def sort_by_column(self, column_name: str):
        if self.sort_column == column_name:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column_name
            self.sort_order = "asc"
        self.current_page = 1

    @rx.event
    async def fetch_customers(self):
        self.loading = True
        self.error_message = ""
        self.all_selected = False
        target_email = self._target_customer_email_for_tags
        target_tag_str = self._target_customer_tag_str
        target_role = self._target_customer_role
        self._target_customer_email_for_tags = None
        self._target_customer_tag_str = None
        self._target_customer_role = None

        if not self._all_customers_data:
            fake_customers_temp: List[CustomerData] = []
            first_names = [
                "John",
                "Jane",
                "Alice",
                "Bob",
                "Charlie",
                "David",
                "Eve",
                "Fiona",
                "George",
                "Hannah",
            ]
            last_names = [
                "Doe",
                "Smith",
                "Johnson",
                "Brown",
                "Williams",
                "Jones",
                "Davis",
                "Miller",
                "Wilson",
                "Moore",
            ]
            for _ in range(25):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@example.com"
                created_at = datetime.datetime.now() - datetime.timedelta(
                    days=random.randint(0, 365)
                )
                updated_at = created_at + datetime.timedelta(
                    days=random.randint(0, (datetime.datetime.now() - created_at).days)
                )

                tags = []
                if self.available_tags and random.random() > 0.3:
                    num_tags = random.randint(1, min(3, len(self.available_tags)))
                    tags = random.sample(self.available_tags, num_tags)

                role = (
                    random.choice(self.available_roles)
                    if self.available_roles
                    else "N/A"
                )

                if target_email and email == target_email:
                    if target_tag_str is not None:
                        tags = self._parse_tags_string(target_tag_str)
                    if target_role is not None:
                        role = target_role

                fake_customers_temp.append(
                    CustomerData(
                        customer_id=self._next_customer_id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=(
                            f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"
                            if random.random() > 0.2
                            else None
                        ),
                        status=random.choice(self.customer_statuses),
                        avatar_url="/favicon.ico",
                        role=role,
                        tags=tags,
                        created_at=created_at.isoformat(),
                        updated_at=updated_at.isoformat(),
                        selected=False,
                    )
                )
                self._next_customer_id += 1
            self._all_customers_data = fake_customers_temp
        else:
            if target_email:
                for i, cust in enumerate(self._all_customers_data):
                    if cust["email"] == target_email:
                        if target_tag_str is not None:
                            self._all_customers_data[i]["tags"] = (
                                self._parse_tags_string(target_tag_str)
                            )
                        if target_role is not None:
                            self._all_customers_data[i]["role"] = target_role
                        break

        self.total_db_customers = len(self._all_customers_data)
        if self.current_page > self.total_pages and self.total_pages > 0:
            self.current_page = self.total_pages
        elif self.current_page < 1:
            self.current_page = 1
        self.loading = False
        self.error_message = ""

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def select_customer_for_edit(self, customer: CustomerData):
        self.form_customer_id = customer["customer_id"]
        self.form_first_name = customer["first_name"]
        self.form_last_name = customer["last_name"]
        self.form_email = customer["email"]
        self.form_status = (
            customer["status"]
            if customer["status"] in self.customer_statuses
            else "Active"
        )
        self.form_tags = self._format_tags_list_to_string(customer["tags"])
        self.form_role = (
            customer["role"]
            if customer["role"] in self.available_roles
            else (self.available_roles[0] if self.available_roles else "")
        )
        self.show_edit_dialog = True
        self.error_message = ""

    @rx.event
    def prepare_add_customer(self):
        self._reset_form_fields()
        self.show_edit_dialog = True
        self.error_message = ""

    @rx.event
    def toggle_edit_dialog(self):
        self.show_edit_dialog = not self.show_edit_dialog
        if not self.show_edit_dialog:
            self._reset_form_fields()
        self.error_message = ""

    def _reset_form_fields(self):
        self.form_customer_id = 0
        self.form_first_name = ""
        self.form_last_name = ""
        self.form_email = ""
        self.form_status = "Active"
        self.form_tags = ""
        self.form_role = self.available_roles[0] if self.available_roles else ""

    @rx.event
    async def handle_edit_customer(self, form_data: dict):
        customer_id_str = form_data.get("customer_id", "0")
        try:
            customer_id = int(customer_id_str)
        except ValueError:
            async with self:
                self.error_message = "Invalid Customer ID."
            return

        is_add_operation = customer_id == 0
        first_name = form_data.get("first_name", "").strip()
        last_name = form_data.get("last_name", "").strip()
        email_from_form = form_data.get("email", "").strip()
        status = form_data.get("status", self.form_status).strip()
        tags_str_from_form = form_data.get("tags", "")
        role_from_form = form_data.get("role", self.form_role).strip()

        if not first_name or not last_name or not email_from_form:
            self.error_message = "First name, last name, and email are required."
            return

        self.error_message = ""
        for cust in self._all_customers_data:
            if cust["email"] == email_from_form and (
                is_add_operation or cust["customer_id"] != customer_id
            ):
                self.error_message = f"Email '{email_from_form}' already exists."
                return

        if is_add_operation:
            new_customer = CustomerData(
                customer_id=self._next_customer_id,
                first_name=first_name,
                last_name=last_name,
                email=email_from_form,
                phone=form_data.get("phone"),
                status=status,
                avatar_url="/favicon.ico",
                role=role_from_form,
                tags=self._parse_tags_string(tags_str_from_form),
                created_at=datetime.datetime.now().isoformat(),
                updated_at=datetime.datetime.now().isoformat(),
                selected=False,
            )
            self._all_customers_data.append(new_customer)
            self._next_customer_id += 1
            toast_message = "User added successfully!"
        else:
            customer_found = False
            for i, cust in enumerate(self._all_customers_data):
                if cust["customer_id"] == customer_id:
                    self._all_customers_data[i]["first_name"] = first_name
                    self._all_customers_data[i]["last_name"] = last_name
                    self._all_customers_data[i]["email"] = email_from_form
                    self._all_customers_data[i]["status"] = status
                    self._all_customers_data[i]["role"] = role_from_form
                    self._all_customers_data[i]["tags"] = self._parse_tags_string(
                        tags_str_from_form
                    )
                    self._all_customers_data[i]["updated_at"] = (
                        datetime.datetime.now().isoformat()
                    )
                    customer_found = True
                    break
            if not customer_found:
                self.error_message = f"Customer with ID {customer_id} not found."
                return
            toast_message = "User updated successfully!"

        self._target_customer_email_for_tags = email_from_form
        self._target_customer_tag_str = tags_str_from_form
        self._target_customer_role = role_from_form

        self.show_edit_dialog = False
        self._reset_form_fields()
        self.total_db_customers = len(self._all_customers_data)

        yield CustomerState.fetch_customers
        yield rx.toast(toast_message, duration=3000)

    @rx.event
    def set_form_status(self, status: str):
        self.form_status = status

    @rx.event
    def set_form_tags(self, tags: str):
        self.form_tags = tags

    @rx.event
    def set_form_role(self, role: str):
        self.form_role = role

    @rx.event
    def toggle_select_all(self):
        self.all_selected = not self.all_selected
        for i in range(len(self._all_customers_data)):
            self._all_customers_data[i]["selected"] = self.all_selected

    @rx.event
    def toggle_select_customer(self, customer_id: int):
        all_are_selected_after_toggle = True
        found = False
        for i in range(len(self._all_customers_data)):
            if self._all_customers_data[i]["customer_id"] == customer_id:
                self._all_customers_data[i]["selected"] = not self._all_customers_data[
                    i
                ]["selected"]
                found = True
            if not self._all_customers_data[i]["selected"]:
                all_are_selected_after_toggle = False
        if found:
            self.all_selected = all_are_selected_after_toggle

    @rx.event(background=True)
    async def download_csv(self):
        async with self:
            if not self._all_customers_data:
                self.error_message = "No customer data available to download. Please fetch customers first."
                yield rx.toast(
                    "No customer data to download.",
                    duration=3000,
                )
                return
            self.loading = True
            self.error_message = ""
        try:
            df_export_data = []
            for cust_data_item in self._all_customers_data:
                tags_str_repr = ", ".join(cust_data_item["tags"])
                df_export_data.append(
                    {
                        "ID": cust_data_item["customer_id"],
                        "First Name": cust_data_item["first_name"],
                        "Last Name": cust_data_item["last_name"],
                        "Email": cust_data_item["email"],
                        "Phone": cust_data_item.get("phone", ""),
                        "Status": cust_data_item["status"],
                        "Role": cust_data_item["role"],
                        "Tags": tags_str_repr,
                        "Created At": cust_data_item["created_at"],
                        "Updated At": cust_data_item["updated_at"],
                    }
                )
            if not df_export_data:
                async with self:
                    self.error_message = "No customers to download."
                yield rx.toast(
                    "No customer data available to download.",
                    duration=3000,
                )
                return
            df = pd.DataFrame(df_export_data)
            csv_data = df.to_csv(index=False)
            filename = (
                f"customers_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            yield rx.download(data=csv_data, filename=filename)
            yield rx.toast("CSV download started.", duration=3000)
        except Exception as e:
            async with self:
                self.error_message = f"Failed to download CSV: {e!s}"
            yield rx.toast(
                f"Error downloading CSV: {e!s}",
                duration=5000,
            )
        finally:
            async with self:
                self.loading = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1
