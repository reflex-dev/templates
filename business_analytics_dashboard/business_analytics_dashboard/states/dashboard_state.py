from collections import Counter
from typing import List, TypedDict

import reflex as rx
from sqlalchemy import text

from business_analytics_dashboard.models.employee import Employee


class DepartmentData(TypedDict):
    name: str
    value: int


class DashboardState(rx.State):
    """State for the dashboard."""

    employees: List[Employee] = []
    search_query: str = ""
    selected_department: str = "All"
    loading: bool = False
    loading_revenue: bool = False
    total_expense_amount: float = 0.0
    average_expense_amount: float = 0.0
    department_colors: list[str] = [
        "#2B79D1",
        "#2469B3",
        "#1E5AA1",
        "#3D8EE1",
        "#61A9E4",
        "#8BC34A",
        "#CDDC39",
        "#FFEB3B",
        "#FFC107",
        "#FF9800",
    ]

    @rx.event(background=True)
    async def fetch_dashboard_data(self):
        """Fetch all necessary data for the dashboard."""
        async with self:
            self.loading = True
            self.loading_revenue = True
        yield DashboardState.fetch_employees
        yield DashboardState.fetch_total_expense_amount
        yield DashboardState.fetch_average_expense_amount

    @rx.event(background=True)
    async def fetch_employees(self):
        """Fetch employees from the database."""
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "\n                        SELECT employee_id, first_name, last_name, email, department\n                        FROM employees\n                        "
                    )
                )
                rows = result.fetchall()
                employees_data = [
                    Employee(
                        employee_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        email=row[3],
                        department=row[4],
                    )
                    for row in rows
                ]
                async with self:
                    self.employees = employees_data
        except Exception:
            async with self:
                self.employees = []
        finally:
            async with self:
                self.loading = False

    @rx.event(background=True)
    async def fetch_total_expense_amount(self):
        """Fetch total expense amount from the database."""
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "\n                        SELECT SUM(total_amount)\n                        FROM expense_reports\n                        "
                    )
                )
                total_amount_decimal = result.scalar_one_or_none()
                async with self:
                    self.total_expense_amount = (
                        float(total_amount_decimal) if total_amount_decimal else 0.0
                    )
        except Exception:
            async with self:
                self.total_expense_amount = 0.0
        finally:
            async with self:
                if not self.loading:
                    self.loading_revenue = False

    @rx.event(background=True)
    async def fetch_average_expense_amount(self):
        """Fetch average expense amount from the database."""
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "\n                        SELECT AVG(total_amount)\n                        FROM expense_reports\n                        "
                    )
                )
                avg_amount_decimal = result.scalar_one_or_none()
                async with self:
                    self.average_expense_amount = (
                        float(avg_amount_decimal) if avg_amount_decimal else 0.0
                    )
        except Exception:
            async with self:
                self.average_expense_amount = 0.0
        finally:
            async with self:
                self.loading_revenue = False

    @rx.var
    def available_departments(self) -> list[str]:
        """Get a sorted list of unique departments."""
        if not self.employees:
            return ["All"]
        departments = sorted({emp["department"] for emp in self.employees})
        return ["All", *departments]

    @rx.var
    def filtered_employees(self) -> List[Employee]:
        """Filter employees based on search query and selected department."""
        filtered = self.employees
        if self.selected_department != "All":
            filtered = [
                emp for emp in filtered if emp["department"] == self.selected_department
            ]
        if self.search_query:
            search_lower = self.search_query.lower()
            filtered = [
                emp
                for emp in filtered
                if search_lower in emp["first_name"].lower()
                or search_lower in emp["last_name"].lower()
                or search_lower in emp["email"].lower()
                or (search_lower in emp["department"].lower())
            ]
        return filtered

    @rx.var
    def department_distribution(
        self,
    ) -> List[DepartmentData]:
        """Calculate the distribution of employees for the selected department or all."""
        if not self.employees:
            return []
        target_employees = self.employees
        if self.selected_department != "All":
            target_employees = [
                emp
                for emp in self.employees
                if emp["department"] == self.selected_department
            ]
        if not target_employees:
            return []
        dept_counts = Counter((emp["department"] for emp in target_employees))
        return [
            DepartmentData(name=dept, value=count)
            for dept, count in dept_counts.items()
        ]

    @rx.var
    def formatted_total_expense(self) -> str:
        """Format the total expense amount as a string."""
        return f"{self.total_expense_amount:,.2f}"

    @rx.var
    def formatted_average_expense(self) -> str:
        """Format the average expense amount as a string."""
        return f"{self.average_expense_amount:,.2f}"

    @rx.event
    def set_search_query(self, value: str):
        """Set the search query."""
        self.search_query = value

    @rx.event
    def set_selected_department(self, department: str):
        """Set the selected department."""
        self.selected_department = department
