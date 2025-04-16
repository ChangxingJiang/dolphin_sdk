"""
任务在工作流视图中的位置
"""

import dataclasses
import json
from typing import List

from dolphin_sdk.objects.base import ObjectBase

__all__ = [
    "DSLocation",
    "create_ds_location_list_from_db_value"
]


@dataclasses.dataclass(slots=True)
class DSLocation(ObjectBase):
    task_code: int = dataclasses.field(kw_only=True)
    x: float = dataclasses.field(kw_only=True)
    y: float = dataclasses.field(kw_only=True)

    def to_json(self) -> dict:
        return {
            "taskCode": self.task_code,
            "x": self.x,
            "y": self.y
        }


def create_ds_location_list_from_db_value(db_value: str) -> List[DSLocation]:
    """根据数据库中 t_ds_process_definition.locations 字段的值，构造 DSLocation 对象的列表"""
    json_value = json.loads(db_value)
    return [DSLocation(
        task_code=json_item["taskCode"],
        x=float(json_item["x"]),
        y=float(json_item["y"]),
    ) for json_item in json_value if "taskCode" in json_item]
