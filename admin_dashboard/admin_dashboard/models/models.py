from datetime import datetime
from typing import (
    Dict,
    List,
    Optional,
    TypedDict,
    Union,
)


class CustomerData(TypedDict):
    id: int
    customer_name: str
    next_renewal: str
    revenue: float
    licenses: int
    active_licenses: int
    active_license_growth: int
    license_growth: int
    industry: str
    platform: str
    usage_history: List[Dict[str, Union[str, int]]]
    next_renewal_date: Optional[datetime]
