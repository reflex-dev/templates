import datetime
import random
from typing import List

from retail_analytics_dashboard.models.models import ChartDataPoint


def generate_chart_data(
    start_date_str: str,
    end_date_str: str,
    num_points: int = 30,
    min_val1: int = 50,
    max_val1: int = 200,
    min_val2: int = 30,
    max_val2: int = 150,
) -> List[ChartDataPoint]:
    data: List[ChartDataPoint] = []
    start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y")
    end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y")
    date_delta = (end_date - start_date) / (num_points - 1)
    for i in range(num_points):
        current_date = start_date + date_delta * i
        data.append(
            {
                "date": current_date.strftime("%d/%m/%Y"),
                "value1": random.randint(min_val1, max_val1),
                "value2": random.randint(min_val2, max_val2),
            }
        )
    return data
