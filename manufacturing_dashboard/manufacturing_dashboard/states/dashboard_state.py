import asyncio
import random
from typing import Dict, List, TypedDict

import reflex as rx
from faker import Faker

fake = Faker()


class MetricData(TypedDict):
    parameter: str
    count: int
    sparkline_data: List[Dict[str, int]]
    ooc_percent: float
    pass_fail: bool


class SpcDataPoint(TypedDict):
    name: int
    value: float


class PieChartData(TypedDict):
    name: str
    value: float
    fill: str


class DistributionPoint(TypedDict):
    name: str
    value: int


def _generate_sparkline_data(
    count: int = 20,
) -> List[Dict[str, int]]:
    return [{"uv": fake.random_int(300, 500)} for _ in range(count)]


def _generate_process_metrics(
    num_metrics: int = 4,
) -> List[MetricData]:
    parameters = [
        "DIAMETER",
        "ETCH1",
        "FILM-THICKNESS",
        "ETCH2",
        "LINE-WIDTH",
        "OVERLAY",
        "VOLUME",
    ]
    random.shuffle(parameters)
    metrics = []
    for i in range(num_metrics):
        param = parameters[i % len(parameters)]
        ooc = fake.pyfloat(
            left_digits=1,
            right_digits=1,
            positive=True,
            max_value=10.0,
        )
        metrics.append(
            {
                "parameter": param,
                "count": fake.random_int(40, 60),
                "sparkline_data": _generate_sparkline_data(),
                "ooc_percent": round(ooc, 1),
                "pass_fail": ooc <= 7.0,
            }
        )
    return metrics


def _generate_spc_data(
    num_points: int = 30,
    base_min: float = 0.415,
    base_max: float = 0.428,
    ooc_freq_up: int = 5,
    ooc_amount_up: float = 0.005,
    ooc_freq_down: int = 7,
    ooc_amount_down: float = 0.008,
) -> List[SpcDataPoint]:
    data = []
    for i in range(num_points):
        base_value = fake.pyfloat(
            left_digits=0,
            right_digits=4,
            positive=True,
            min_value=base_min,
            max_value=base_max,
        )
        if random.random() < 0.1:
            base_value += random.uniform(ooc_amount_up * 1.5, ooc_amount_up * 2.5)
        elif random.random() < 0.1:
            base_value -= random.uniform(ooc_amount_down * 1.5, ooc_amount_down * 2.5)
        elif i % ooc_freq_up == 0:
            base_value += random.uniform(ooc_amount_up * 0.5, ooc_amount_up * 1.5)
        elif i % ooc_freq_down == 0:
            base_value -= random.uniform(ooc_amount_down * 0.5, ooc_amount_down * 1.5)
        data.append({"name": i, "value": round(base_value, 4)})
    return data


def _generate_pie_data(
    metrics: List[MetricData],
) -> List[PieChartData]:
    pie_data = []
    colors_fail = [
        "#f87171",
        "#ef4444",
        "#dc2626",
        "#fb923c",
        "#f97316",
    ]
    colors_pass = [
        "#2dd4bf",
        "#14b8a6",
        "#0d9488",
        "#60a5fa",
        "#3b82f6",
        "#a78bfa",
        "#93c5fd",
    ]
    color_index_fail = 0
    color_index_pass = 0
    for metric in metrics:
        if metric["ooc_percent"] > 0.1:
            if not metric["pass_fail"]:
                fill_color = colors_fail[color_index_fail % len(colors_fail)]
                color_index_fail += 1
            else:
                fill_color = colors_pass[color_index_pass % len(colors_pass)]
                color_index_pass += 1
            pie_data.append(
                {
                    "name": metric["parameter"],
                    "value": metric["ooc_percent"],
                    "fill": fill_color,
                }
            )
    if not pie_data:
        default_low_ooc = [
            ("Diameter", 0.5),
            ("Etch1", 0.3),
        ]
        for name, value in default_low_ooc:
            pie_data.append(
                {
                    "name": name,
                    "value": value,
                    "fill": colors_pass[color_index_pass % len(colors_pass)],
                }
            )
            color_index_pass += 1
    return pie_data


def _generate_distribution_data(
    spc_data: List[SpcDataPoint], num_bins=8
) -> List[DistributionPoint]:
    """Generates histogram-like data from SPC points."""
    if not spc_data:
        return []
    values = [p["value"] for p in spc_data]
    min_val, max_val = (min(values), max(values))
    if min_val == max_val:
        return [{"name": f"{min_val:.3f}", "value": len(values)}]
    bin_width = (max_val - min_val) / num_bins
    bins = [0] * num_bins
    for val in values:
        bin_index = min(int((val - min_val) / bin_width), num_bins - 1)
        if val == max_val:
            bin_index = num_bins - 1
        bins[bin_index] += 1
    dist_data = []
    for i in range(num_bins):
        bin_start = min_val + i * bin_width
        bin_name = f"{bin_start:.3f}"
        dist_data.append({"name": bin_name, "value": bins[i]})
    return dist_data


initial_process_metrics = _generate_process_metrics()
initial_spc_data = _generate_spc_data(base_min=0.415, base_max=0.424)
initial_pie_data = _generate_pie_data(initial_process_metrics)
initial_distribution_data = _generate_distribution_data(initial_spc_data)


class DashboardState(rx.State):
    """Handles the state and logic for the dashboard application."""

    operator_id: str = fake.bothify(text="OP-####")
    time_to_completion: float = 0.0
    is_running: bool = False
    ucl: float = 0.432
    lcl: float = 0.407
    target_mean: float = 0.42
    usl: float = 0.424
    lsl: float = 0.415
    process_metrics: List[MetricData] = initial_process_metrics
    spc_chart_data: List[SpcDataPoint] = initial_spc_data
    pie_data: List[PieChartData] = initial_pie_data
    distribution_data: List[DistributionPoint] = initial_distribution_data

    def _reset_to_initial(self):
        """Resets data to a new initial state."""
        self.process_metrics = _generate_process_metrics()
        self.spc_chart_data = _generate_spc_data(base_min=self.lsl, base_max=self.usl)
        self.pie_data = _generate_pie_data(self.process_metrics)
        self.distribution_data = _generate_distribution_data(self.spc_chart_data)

    @rx.event(background=True)
    async def start_process(self):
        """Simulates starting a process and updating data over time using Faker."""
        async with self:
            if self.is_running:
                return
            self.is_running = True
            self.time_to_completion = 0.0
        update_interval = 0.1
        data_gen_interval = 10
        metrics_update_interval = 30
        for i in range(101):
            async with self:
                self.time_to_completion = float(i)
                if i > 0 and i % data_gen_interval == 0:
                    last_name = (
                        self.spc_chart_data[-1]["name"] if self.spc_chart_data else -1
                    )
                    new_name = last_name + 1
                    new_value_base = fake.pyfloat(
                        left_digits=0,
                        right_digits=4,
                        positive=True,
                        min_value=self.lsl - 0.002,
                        max_value=self.usl + 0.002,
                    )
                    if self.spc_chart_data:
                        drift = random.uniform(-0.001, 0.001)
                        new_value_base = self.spc_chart_data[-1]["value"] + drift
                    if random.random() < 0.08:
                        new_value_base += random.uniform(0.003, 0.008)
                    elif random.random() < 0.08:
                        new_value_base -= random.uniform(0.003, 0.008)
                    new_value = round(
                        max(
                            self.lcl - 0.01,
                            min(
                                self.ucl + 0.01,
                                new_value_base,
                            ),
                        ),
                        4,
                    )
                    new_point: SpcDataPoint = {
                        "name": new_name,
                        "value": new_value,
                    }
                    self.spc_chart_data = ([*self.spc_chart_data, new_point])[-50:]
                    self.distribution_data = _generate_distribution_data(
                        self.spc_chart_data
                    )
                if i > 0 and i % metrics_update_interval == 0:
                    self.process_metrics = _generate_process_metrics()
                    self.pie_data = _generate_pie_data(self.process_metrics)
            await asyncio.sleep(update_interval)
            yield
        async with self:
            self.is_running = False
            self._reset_to_initial()

    @rx.var
    def get_time_stroke_dasharray(self) -> str:
        """Calculates the stroke-dasharray for the time completion circle."""
        percentage = self.time_to_completion
        radius = 40
        circumference = 2 * 3.14159 * radius
        clamped_percentage = max(0, min(percentage, 100))
        dash_length = clamped_percentage / 100 * circumference
        dash_length = max(0, dash_length)
        gap_length = max(0, circumference - dash_length)
        return f"{dash_length:.2f} {gap_length:.2f}"

    @rx.var
    def ooc_points(self) -> List[SpcDataPoint]:
        """Filters SPC data to find points outside control limits (OOC)."""
        ooc = []
        if not self.spc_chart_data:
            return []
        ooc = [
            point
            for point in self.spc_chart_data
            if isinstance(point.get("value"), (int, float))
            and (point["value"] < self.lcl or point["value"] > self.ucl)
        ]

        return ooc
