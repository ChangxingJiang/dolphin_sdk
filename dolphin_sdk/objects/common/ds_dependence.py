"""
海豚任务定义的 task_params 字段中 dependence 属性的类型
"""

import dataclasses
from typing import List, Optional

from dolphin_sdk.objects.common.ds_depend_task import DSDependTask
from dolphin_sdk.objects.enum import DSDependRelation

__all__ = [
    "DSDependence"
]


@dataclasses.dataclass(slots=True)
class DSDependence:
    """海豚任务定义的 task_params 字段中 dependence 属性的类型

    格式：
    {
        "relation": <DSDependRelation>,
        "dependTaskList": [<DSDependTask>, <DSDependTask>, ...]
    }
    """

    relation: Optional[DSDependRelation] = dataclasses.field(kw_only=True, default=None)
    depend_task_list: List[DSDependTask] = dataclasses.field(kw_only=True, default_factory=lambda: [])

    @staticmethod
    def create_by_one_daily_dependent(project_code: int, process_code: int):
        """构造单工作流单日依赖"""
        return DSDependence(
            relation=DSDependRelation.AND,
            depend_task_list=[DSDependTask.create_by_one_daily_dependent(project_code, process_code)],
        )

    @staticmethod
    def from_db_json(json_data: dict) -> "DSDependence":
        if not json_data:
            return DSDependence()
        return DSDependence(
            relation=DSDependRelation.from_db_value(json_data["relation"]),
            depend_task_list=[DSDependTask.from_db_json(item) for item in json_data["dependTaskList"]]
        )

    def to_json(self) -> dict:
        return {
            "relation": self.relation.web_value,
            "dependTaskList": [depend_task.to_json() for depend_task in self.depend_task_list],
        }
