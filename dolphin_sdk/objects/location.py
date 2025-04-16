"""
任务在工作流视图中的位置
"""

import dataclasses

from dolphin_sdk.objects.base import ObjectBase


@dataclasses.dataclass(slots=True)
class Location(ObjectBase):
    task_code: int = dataclasses.field(kw_only=True)
    x: float = dataclasses.field(kw_only=True)
    y: float = dataclasses.field(kw_only=True)

    def to_json(self) -> dict:
        return {
            "taskCode": self.task_code,
            "x": self.x,
            "y": self.y
        }
