"""
海豚任务定义的 task_params 字段中 dependence 属性的类型
"""

import dataclasses
from typing import List

from dolphin_sdk.objects.common.ds_depend_item import DSDependItem
from dolphin_sdk.objects.enum import DSDependRelation

__all__ = [
    "DSDependTask"
]


@dataclasses.dataclass(slots=True)
class DSDependTask:
    """海豚任务定义的 task_params 字段中 dependence 属性中的 dependTaskList 中的依赖任务

    格式：
    {
        "relation": <DSDependRelation>,
        "dependItemList": [<DSDependItem>, <DSDependItem>, ...]
    }
    """

    relation: DSDependRelation = dataclasses.field(kw_only=True)
    depend_item_list: List[DSDependItem] = dataclasses.field(kw_only=True)

    @staticmethod
    def from_db_json(json_data: dict) -> "DSDependTask":
        return DSDependTask(
            relation=DSDependRelation.from_db_value(json_data["relation"]),
            depend_item_list=[DSDependItem.from_db_json(item) for item in json_data["dependItemList"]]
        )

    @staticmethod
    def create_by_one_daily_dependent(project_code: int, process_code: int):
        """构造单工作流单日依赖"""
        return DSDependTask(
            relation=DSDependRelation.AND,
            depend_item_list=[DSDependItem.create_by_daily(project_code, process_code)],
        )

    def to_json(self) -> dict:
        return {
            "relation": self.relation.web_value,
            "dependItemList": [depend_item.to_json() for depend_item in self.depend_item_list],
        }
