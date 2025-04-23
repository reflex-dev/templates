import asyncio
import math
import random
import statistics
from collections import Counter, defaultdict
from typing import Dict, List, TypedDict

import reflex as rx
from faker import Faker

from business_analytics_dashboard.models.employee import Employee

fake = Faker()


class DepartmentData(TypedDict):
    name: str
    value: int


class AverageSalaryData(TypedDict):
    department: str
    average_salary: float


class DashboardState(rx.State):
    """State for the dashboard."""

    employees: List[Employee] = []
    search_query: str = ""
    selected_department: str = "All"
    loading: bool = False
    _base_department_colors: list[str] = [
        "#FF6347",
        "#4CAF50",
        "#FFEB3B",
        "#2196F3",
        "#9C27B0",
        "#FFC107",
        "#8BC34A",
        "#FF9800",
        "#F44336",
        "#00BCD4",
    ]
    current_page: int = 1
    items_per_page: int = 10

    @rx.event(background=True)
    async def fetch_dashboard_data(self):
        """Generate fake data for the dashboard."""
        async with self:
            self.loading = True
            self.current_page = 1
        await asyncio.sleep(0.5)
        await self._generate_fake_data()
        async with self:
            self.loading = False

    async def _generate_fake_data(self):
        """Helper method to generate fake employee data."""
        departments = [
            "Sales",
            "Marketing",
            "Engineering",
            "Support",
            "HR",
            "Finance",
            "Product",
            "Design",
            "Operations",
            "Legal",
        ]
        employees_data = []
        for i in range(1, 101):
            first_name = fake.first_name()
            last_name = fake.last_name()
            department = random.choice(departments)
            employees_data.append(
                Employee(
                    employee_id=1000 + i,
                    first_name=first_name,
                    last_name=last_name,
                    email=fake.email(),
                    department=department,
                    salary=random.randint(50000, 150000),
                    projects_closed=random.randint(0, 20),
                    pending_projects=random.randint(0, 5),
                )
            )
        async with self:
            self.employees = employees_data

    @rx.var
    def available_departments(self) -> list[str]:
        """Get a sorted list of unique departments including 'All'."""
        if not self.employees:
            return ["All"]
        departments = sorted({emp["department"] for emp in self.employees})
        return ["All", *departments]

    @rx.var
    def departments_for_filter(self) -> list[str]:
        """Get a sorted list of unique departments excluding 'All'."""
        return [dept for dept in self.available_departments if dept != "All"]

    @rx.var
    def department_color_map(self) -> Dict[str, str]:
        """Maps each department to a consistent color."""
        departments = self.departments_for_filter
        color_map = {}
        num_colors = len(self._base_department_colors)
        for i, dept in enumerate(departments):
            color_map[dept] = self._base_department_colors[i % num_colors]
        return color_map

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
                or (search_lower in str(emp["salary"]))
                or (search_lower in str(emp["projects_closed"]))
                or (search_lower in str(emp["pending_projects"]))
            ]
        return filtered

    @rx.var
    def total_pages(self) -> int:
        """Calculate the total number of pages based on filtered employees."""
        return math.ceil(len(self.filtered_employees) / self.items_per_page)

    @rx.var
    def paginated_employees(self) -> List[Employee]:
        """Get the employees for the current page."""
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.filtered_employees[start_index:end_index]

    @rx.var
    def department_distribution(
        self,
    ) -> List[DepartmentData]:
        """Calculate the distribution of employees by department based on filters."""
        target_employees = self.filtered_employees
        if not target_employees:
            return []
        dept_counts = Counter((emp["department"] for emp in target_employees))
        return [
            DepartmentData(name=dept, value=count)
            for dept, count in dept_counts.items()
        ]

    @rx.var
    def average_salary_by_department(
        self,
    ) -> list[AverageSalaryData]:
        """Calculate the average salary for each department, considering filters."""
        if not self.employees:
            return []
        dept_salaries = defaultdict(list)
        for emp in self.employees:
            dept_salaries[emp["department"]].append(emp["salary"])
        avg_salaries = []
        for dept in self.departments_for_filter:
            salaries = dept_salaries.get(dept, [])
            if salaries:
                avg_salary = statistics.mean(salaries)
                avg_salaries.append(
                    AverageSalaryData(
                        department=dept,
                        average_salary=round(avg_salary, 2),
                    )
                )
            else:
                pass
        if self.selected_department != "All":
            avg_salaries = [
                item
                for item in avg_salaries
                if item["department"] == self.selected_department
            ]
        return avg_salaries

    @rx.event
    def set_search_query(self, value: str):
        """Set the search query and reset to page 1."""
        self.search_query = value
        self.current_page = 1

    @rx.event
    def set_selected_department(self, department: str):
        """Set the selected department and reset to page 1."""
        self.selected_department = department
        self.current_page = 1

    @rx.event
    def previous_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def go_to_page(self, page_num: int):
        """Go to a specific page number."""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
