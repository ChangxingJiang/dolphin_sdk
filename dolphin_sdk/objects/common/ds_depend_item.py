"""
海豚任务定义的 task_params 字段中 dependence 属性中的 dependItemList 中的依赖任务
"""

import dataclasses
from typing import Optional

from dolphin_sdk.objects.base import ObjectBase

__all__ = [
    "DSDependItem"
]


@dataclasses.dataclass(slots=True)
class DSDependItem(ObjectBase):
    """海豚任务定义的 task_params 字段中 dependence 属性中的 dependItemList 中的依赖任务"""

    project_code: int = dataclasses.field(kw_only=True)  # projectCode
    definition_code: int = dataclasses.field(kw_only=True)  # definitionCode
    dep_task_code: int = dataclasses.field(kw_only=True)  # depTaskCode
    cycle: str = dataclasses.field(kw_only=True)  # day
    data_value: str = dataclasses.field(kw_only=True)  # dataValue
    state: Optional[int] = dataclasses.field(kw_only=True)  # state

    @staticmethod
    def from_db_json(json_data: dict) -> "DSDependItem":
        return DSDependItem(
            project_code=json_data.get("projectCode"),
            definition_code=json_data.get("definitionCode"),
            dep_task_code=json_data.get("depTaskCode"),
            cycle=json_data.get("cycle"),
            data_value=json_data.get("dateValue"),
            state=json_data.get("state")
        )

    @staticmethod
    def create_by_daily(project_code: int, process_code: int) -> "DSDependItem":
        """构造当日依赖"""
        return DSDependItem(
            project_code=project_code,
            definition_code=process_code,
            dep_task_code=0,
            cycle="day",
            data_value="today",
            state=None
        )

    def to_json(self) -> dict:
        return {
            "projectCode": self.project_code,
            "definitionCode": self.definition_code,
            "depTaskCode": self.dep_task_code,
            "cycle": self.cycle,
            "dateValue": self.data_value,
            "state": self.state
        }
